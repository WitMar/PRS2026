import asyncio
import concurrent.futures
import json
import logging
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import List, Optional

import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, ValidationError

from app import constants, parking, compare, state
from app.data_models import client_handshake, result

APP_DIR = Path(__file__).resolve().parent / 'app'
for d in ('logs', 'payloads', 'results'):
    (APP_DIR / d).mkdir(exist_ok=True)

logging.basicConfig(handlers=[
    logging.FileHandler(APP_DIR / "logs" / "app.log"),
    logging.StreamHandler()
],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# endpoint klienta, na który serwer wysyła zdarzenia
CLIENT_DATA_PATH = '/parking-data'

app = FastAPI(title="Serwer parkingów - PRS projekt 1")
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")


# ---------------------------------------------------------------------------
# Endpointy używane przez klientów (protokół projektu)
# ---------------------------------------------------------------------------

@app.post("/clients/handshake", status_code=201)
def handshake(client: client_handshake.ClientHandshake, request: Request):
    source_ip = request.client.host if request.client else None
    with state.lock:
        old = state.clients.get(client.indeks)
        if old is None:
            state.clients[client.indeks] = state.new_client(client.indeks, client.ip_addr, client.port)
            summary = f"rejestracja {client.ip_addr}:{client.port}"
        else:
            old.update(ip_addr=client.ip_addr, port=client.port)
            summary = f"ponowna rejestracja {client.ip_addr}:{client.port}"
        state.clients[client.indeks]['source_ip'] = source_ip
        if source_ip and client.ip_addr in ('localhost', '127.0.0.1') and source_ip not in ('127.0.0.1', '::1'):
            summary += f" - UWAGA: zgłoszenie z {source_ip}, a klient podał adres lokalny"
        n = len(state.clients)
    state.add_message('in', 'handshake', '/clients/handshake', client.indeks, 201,
                      client.model_dump(), summary)
    logging.info(f"Registered client {client.indeks} ({client.ip_addr}:{client.port})! # available clients: {n}")
    return {"registered": client.indeks, "clients": n}


@app.post("/results", openapi_extra={"requestBody": {"content": {"application/json": {
    "schema": result.Result.model_json_schema()}}, "required": True}})
async def submit_result(request: Request):
    raw = await request.body()
    # moment odebrania CAŁEGO wyniku - przed walidacją i jakimkolwiek czekaniem
    result_pc, received_at = time.perf_counter(), time.time()
    try:
        res = result.Result.model_validate_json(raw)
    except ValidationError as e:
        raise RequestValidationError(e.errors(include_url=False))
    body = res.model_dump()
    with state.lock:
        c = state.clients.get(res.indeks)
        run_id = c and c['run']
        sent_pc = c and c['_sent_pc']
        ready = state.reference_ready.get(run_id)
    if not run_id or not sent_pc or ready is None:
        state.add_message('in', 'result', '/results', res.indeks, 409, body,
                          'wynik od klienta, któremu nie wysłano danych')
        raise HTTPException(status_code=409, detail="No data was sent to this client")

    duration = result_pc - sent_pc
    with state.lock:
        c.update(received_at=received_at, duration=duration)
        if not ready.is_set():
            c['status'] = 'waiting_reference'
        state.touch()
    # czekamy (bez blokowania wątków serwera) na potwierdzenie odbioru danych i na wzorzec
    for _ in range(20):
        if c['_ack_pc'] is not None:
            break
        await asyncio.sleep(0.05)
    while not ready.is_set():
        await asyncio.sleep(0.2)

    with state.lock:
        reference = state.references.get(run_id)
        run = next((r for r in state.runs if r['id'] == run_id), None)
        still_current = c['run'] == run_id
        ack_pc = c['_ack_pc']
    if reference is None or run is None or not still_current:
        state.add_message('in', 'result', '/results', res.indeks, 503, body,
                          'brak wyniku programu wzorcowego (usunięty eksperyment lub błąd wzorca)')
        raise HTTPException(status_code=503, detail="Reference result is not available")

    # czas przetwarzania: od potwierdzenia odbioru danych do odebrania wyniku
    # wynik przed potwierdzeniem = klient liczył już w trakcie odbioru (przed odpowiedzią 201)
    result_before_ack = ack_pc is None or ack_pc > result_pc
    processing = None if result_before_ack else result_pc - ack_pc

    ok, total, details, extra, differences = compare.compare(reference, body['aggregates'])
    ref_time = run.get('reference_time')
    ref_processing = run.get('reference_processing')
    if processing and ref_processing:
        speedup = ref_processing / processing
    else:
        speedup = ref_time / duration if ref_time and duration > 0 else None
    with state.lock:
        c.update(status='done', speedup=speedup, processing=processing, result_before_ack=result_before_ack,
                 score=ok, total=total, n_differences=len(differences), _comparison=details)
        entry = {'run': run_id, 'variant': c['variant'], 'duration': duration, 'processing': processing,
                 'transfer': c['transfer'], 'speedup': speedup, 'score': ok, 'total': total,
                 'events': c['events']}
        if c['history'] and c['history'][-1]['run'] == run_id:
            c['history'][-1] = entry
        else:
            c['history'].append(entry)
        state.totals['results'] += 1
        state.touch()

    compare.save_result_file(res.indeks, c['sent_at'], received_at, duration, processing, ref_time,
                             ref_processing, reference, len(body['aggregates']), ok, total, details,
                             extra, differences)
    state.add_message('in', 'result', '/results', res.indeks, 200, body,
                      f"wynik {ok}/{total}, czas {duration:.3f} s"
                      + (f" (przetwarzanie {processing:.3f} s)" if processing is not None else "")
                      + (f", przyspieszenie ×{speedup:.2f}" if speedup else "")
                      + (f", {len(differences)} różnic" if differences else ""))
    logging.info(f"Client {res.indeks}: {ok}/{total} correct, {duration:.3f}s. Saved into results/{res.indeks}.txt")
    return {"score": ok, "total": total, "duration": duration, "processing": processing,
            "transfer": c['transfer'], "reference_time": ref_processing or ref_time,
            "speedup": speedup, "missing_days": [r['day'] for r in details if r['missing']],
            "extra_days": extra, "differences": differences[:50],
            "differences_count": len(differences)}


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    # błędny format JSON od klienta - pokazujemy go w panelu, żeby łatwiej było szukać błędu
    errors = exc.errors()
    state.add_message('in', 'invalid', request.url.path, None, 422,
                      {'errors': json.loads(json.dumps(errors, default=str))[:20]},
                      f"niepoprawne dane: {len(errors)} błędów walidacji")
    return await request_validation_exception_handler(request, exc)


# --- endpointy zgodne z poprzednią wersją serwera ---

@app.get("/clients")
def get_clients():
    with state.lock:
        return {"clients": [{'ip_addr': c['ip_addr'], 'port': c['port'], 'indeks': c['indeks']}
                            for c in state.clients.values()]}


@app.get("/start")
def legacy_start():
    v = next(v for v in constants.VARIANTS if v['id'] == constants.DEFAULT_VARIANT)
    error = start_run(v['days'], v['cars_per_10_spots'], None, 'GET /start', v['id'])
    return {error or "sending"}


# ---------------------------------------------------------------------------
# Wysyłanie danych do klientów
# ---------------------------------------------------------------------------

def start_run(days, cars_per_10_spots, targets, source, variant=None):
    """Zwraca None gdy rozpoczęto wysyłanie albo komunikat błędu."""
    with state.lock:
        if state.busy:
            return "already sending"
        targets = [i for i in (targets or list(state.clients)) if i in state.clients]
        if not targets:
            logging.info("No clients registered")
            return "no clients registered"
        state.busy = True
        run = {'id': state.next_run_id(), 'started_at': time.time(), 'variant': variant, 'days': days,
               'cars_per_10_spots': cars_per_10_spots, 'clients': targets, 'source': source}
        state.runs.append(run)
        state.touch()
    state.add_message('in', 'start', source, None, 200, run,
                      f"start #{run['id']} ({variant or 'własne parametry'}): {len(targets)} klientów, {days} dni")
    threading.Thread(target=send_run, args=(run,), daemon=True).start()
    return None


def send_run(run):
    """Generuje JEDEN zestaw danych dla eksperymentu i wysyła go do wszystkich klientów."""
    logging.info(f"Starting sending data (run {run['id']})")
    try:
        with state.lock:
            for indeks in run['clients']:
                c = state.clients.get(indeks)
                if c:
                    c.update(status='preparing', run=run['id'], variant=run['variant'], events=None,
                             sent_at=None, received_at=None, duration=None, score=None, total=None,
                             error=None, speedup=None, n_differences=None, _comparison=None,
                             transfer=None, processing=None, result_before_ack=False,
                             _sent_pc=None, _ack_pc=None)
            state.touch()

        events = parking.generate_events(run['days'], run['cars_per_10_spots'])
        # serializacja przed pomiarem czasu - do czasu klienta liczy się tylko przesył i obliczenia
        payload = json.dumps(events).encode()
        compare.save_payload(run['id'], payload)
        with state.lock:
            run['events'] = len(events)
            state.reference_ready[run['id']] = threading.Event()
            state.touch()
        threading.Thread(target=run_reference, args=(run,), daemon=True).start()

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(send_to_client, run, indeks, events, payload)
                       for indeks in run['clients']]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.exception(f"Error: {e}")
    finally:
        with state.lock:
            state.busy = False
            state.touch()
    logging.info("Finished sending data")


def run_reference(run):
    """Uruchamia wzorcowy program sekwencyjny (app/reference.py) jako osobny proces."""
    run_id = run['id']
    with state.lock:
        run['reference_status'] = 'running'
        state.touch()
    payload_path, out_path = compare.payload_paths(run_id)
    try:
        proc = subprocess.run([sys.executable, '-m', 'app.reference', str(payload_path), str(out_path)],
                              cwd=Path(__file__).resolve().parent, capture_output=True, text=True, timeout=3600)
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip().splitlines()[-1] if proc.stderr else f"exit {proc.returncode}")
        info = json.loads(proc.stdout.strip().splitlines()[-1])
        with open(out_path) as f:
            reference = json.load(f)
        with state.lock:
            state.references[run_id] = reference
            run.update(reference_status='done', reference_time=info['duration'],
                       reference_processing=info['processing'])
            state.touch()
        logging.info(f"Reference program for run {run_id}: {info['duration']:.3f}s "
                     f"(processing {info['processing']:.3f}s)")
    except Exception as e:
        logging.exception("Reference program failed")
        with state.lock:
            run.update(reference_status='error', reference_error=str(e)[:300])
            state.touch()
    finally:
        state.reference_ready[run_id].set()


def send_to_client(run, indeks, events, payload):
    with state.lock:
        c = state.clients.get(indeks)
        if c is None or c['run'] != run['id']:  # klienta lub eksperyment usunięto w międzyczasie
            return
        c.update(status='sending', events=len(events))
        url = f"http://{c['ip_addr']}:{c['port']}{CLIENT_DATA_PATH}"
        state.touch()

    msg = state.add_message('out', 'data', url, indeks, None, events,
                            f"{len(events)} zdarzeń, {run['days']} dni")
    with state.lock:
        # czasy mierzone zegarem monotonicznym serwera (perf_counter), time.time() tylko do wyświetlania
        c['sent_at'] = time.time()
        c['_sent_pc'] = time.perf_counter()
        state.totals['events_sent'] += len(events)
    try:
        response = requests.post(url, data=payload, headers={'Content-Type': 'application/json'},
                                 timeout=(3, 600))
        ack_pc = time.perf_counter()  # klient odebrał i zakolejkował dane (odpowiedź 201)
        with state.lock:
            if c['run'] == run['id']:
                c['_ack_pc'] = ack_pc
                c['transfer'] = ack_pc - c['_sent_pc']
        status = response.status_code
        error = None if status < 400 else f"klient odpowiedział {status}: {response.text[:200]}"
    except requests.RequestException as e:
        status, error = 0, f"brak połączenia z klientem: {e.__class__.__name__}"
    state.update_message(msg, status=status)

    with state.lock:
        if c['run'] != run['id']:
            pass
        elif error:
            c.update(status='error', error=error)
        elif c['status'] == 'sending':  # wynik mógł już dotrzeć
            c['status'] = 'processing'
        state.touch()
    if error:
        logging.error(f"Client {indeks}: {error}")


# ---------------------------------------------------------------------------
# Panel WWW
# ---------------------------------------------------------------------------

class StartRequest(BaseModel):
    variant: Optional[str] = None  # id gotowego wariantu, np. 'M2' - nadpisuje days i cars_per_10_spots
    days: int = Field(constants.DAYS, ge=1, le=constants.MAX_DAYS)
    cars_per_10_spots: int = Field(constants.CARS_PER_10_SPOTS, ge=1, le=1000)
    clients: Optional[List[int]] = None


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(APP_DIR / "static" / "index.html")


def server_addresses():
    """Adresy IP serwera w sieci lokalnej (bez wysyłania czegokolwiek w sieć)."""
    ips = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('10.255.255.255', 1))  # UDP connect nie wysyła pakietów - tylko wybiera interfejs
            ips.append(s.getsockname()[0])
    except OSError:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if ip not in ips and not ip.startswith('127.'):
                ips.append(ip)
    except OSError:
        pass
    return ips


@app.get("/api/network")
def get_network(request: Request):
    bound_host, bound_port = request.scope.get('server') or (None, None)
    return {'addresses': server_addresses(), 'port': bound_port, 'bound_host': bound_host,
            'local_only': bound_host in ('127.0.0.1', 'localhost', '::1'),
            'hostname': socket.gethostname()}


@app.get("/api/config")
def get_config():
    return {'parkings': constants.PARKINGS, 'capacity': constants.CAPACITY, 'rate': constants.RATE,
            'aggregate_types': constants.AGGREGATE_TYPES, 'days': constants.DAYS,
            'cars_per_10_spots': constants.CARS_PER_10_SPOTS, 'client_path': CLIENT_DATA_PATH,
            'variants': constants.VARIANTS, 'max_days': constants.MAX_DAYS}


@app.get("/api/state")
def get_state():
    return state.snapshot()


@app.post("/api/start")
def api_start(req: StartRequest):
    days, cars = req.days, req.cars_per_10_spots
    if req.variant is not None:
        variant = next((v for v in constants.VARIANTS if v['id'] == req.variant), None)
        if variant is None:
            raise HTTPException(status_code=404, detail="Unknown variant")
        days, cars = variant['days'], variant['cars_per_10_spots']
    error = start_run(days, cars, req.clients, 'panel', req.variant)
    if error:
        raise HTTPException(status_code=409, detail=error)
    return {"status": "sending"}


@app.delete("/api/clients/{indeks}")
def api_remove_client(indeks: int):
    with state.lock:
        if state.clients.pop(indeks, None) is None:
            raise HTTPException(status_code=404, detail="Unknown client")
        state.touch()
    return {"removed": indeks}


@app.delete("/api/runs/{run_id}")
def api_remove_run(run_id: int):
    """Usuwa eksperyment z historii i rankingu (np. gdy coś poszło nie tak)."""
    with state.lock:
        if not any(r['id'] == run_id for r in state.runs):
            raise HTTPException(status_code=404, detail="Unknown run")
        state.runs[:] = [r for r in state.runs if r['id'] != run_id]
        state.references.pop(run_id, None)
        compare.remove_payload(run_id)
        for c in state.clients.values():
            c['history'] = [h for h in c['history'] if h['run'] != run_id]
            if c['run'] == run_id:
                c.update(status='registered', run=None, variant=None, events=0, sent_at=None,
                         received_at=None, duration=None, score=None, total=None, error=None,
                         speedup=None, n_differences=None, _comparison=None,
                         transfer=None, processing=None, result_before_ack=False,
                         _sent_pc=None, _ack_pc=None)
        state.touch()
    state.add_message('in', 'start', f'/api/runs/{run_id}', None, 200, None, f"usunięto eksperyment #{run_id}")
    return {"removed": run_id}


@app.get("/api/clients/{indeks}/comparison")
def api_comparison(indeks: int):
    with state.lock:
        c = state.clients.get(indeks)
        if c is None:
            raise HTTPException(status_code=404, detail="Unknown client")
        run = next((r for r in state.runs if r['id'] == c['run']), None)
        return {'client': state.public_client(c), 'run': run,
                'reference': state.references.get(c['run']), 'comparison': c['_comparison']}


@app.get("/api/messages/{msg_id}")
def api_message(msg_id: int):
    with state.lock:
        if msg_id not in state.message_bodies:
            raise HTTPException(status_code=404, detail="Message no longer stored")
        return {'body': state.message_bodies[msg_id]}


@app.delete("/api/messages")
def api_clear_messages():
    state.clear_messages()
    return {"cleared": True}


@app.get("/api/stream")
async def api_stream(request: Request, last_id: int = 0):
    """Server-Sent Events: nowe komunikaty i zmiany stanu na żywo."""
    async def events():
        last_version, last_msg, last_beat = -1, last_id, time.time()
        while not await request.is_disconnected():
            msgs = state.messages_since(last_msg)
            if msgs:
                last_msg = msgs[-1]['id']
                yield f"event: messages\ndata: {json.dumps(msgs)}\n\n"
            if state.version != last_version:
                snap = state.snapshot()
                last_version = snap['version']
                yield f"event: state\ndata: {json.dumps(snap)}\n\n"
            elif time.time() - last_beat > 15:
                last_beat = time.time()
                yield ": keep-alive\n\n"
            await asyncio.sleep(0.3)

    return StreamingResponse(events(), media_type="text/event-stream",
                             headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})
