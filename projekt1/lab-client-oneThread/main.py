import heapq
import multiprocessing
import statistics
import threading
import time
from contextlib import asynccontextmanager
from multiprocessing import Queue

from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import logging
import uvicorn

logging.basicConfig(handlers=[
    logging.StreamHandler()
],
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Parkingi i ich parametry (takie same jak w treści zadania i na serwerze)
PARKINGS = ['P1', 'P2', 'P3', 'P4', 'P5']
CAPACITY = {'P1': 20, 'P2': 35, 'P3': 15, 'P4': 50, 'P5': 10}   # liczba miejsc
RATE = {'P1': 0.10, 'P2': 0.08, 'P3': 0.15, 'P4': 0.05, 'P5': 0.25}  # zł za minutę postoju
MINUTES_PER_DAY = 24 * 60

AGGREGATE_TYPES = ['ENTRIES', 'REJECTED', 'MAX_OCCUPANCY', 'REVENUE', 'AVG_STAY', 'MEDIAN_STAY']

# Help - indeks wartości w obrębie jednego dnia: P1_ENTRIES -> 0, P1_REJECTED -> 1, ..., P5_MEDIAN_STAY -> 29
Help = {f'{p}_{a}': i * len(AGGREGATE_TYPES) + j
        for i, p in enumerate(PARKINGS) for j, a in enumerate(AGGREGATE_TYPES)}


class ParkingEvent(BaseModel):
    parking: str   # P1 ... P5
    ticket: int    # numer biletu
    day: int       # dzień wjazdu, od 0
    enter: int     # minuta wjazdu liczona od początku dnia day (0..1439)
    exit: int      # minuta wyjazdu liczona od początku dnia day (>= 1440 - wyjazd w kolejnym dniu)


SERVER_IP = 'localhost'
SERVER_PORT = 5678

CLIENT_IP = 'localhost'
CLIENT_PORT = 6780

INDEKS = 12


def function(queue: Queue, n_events: int):
    start = time.perf_counter()
    global result
    result = [0] * len(Help) * 5000  # 30 wartości na dzień, maksymalnie 5000 dni
    global n_days
    n_days = 0

    # przetwarzanie w jednym osobnym wątku - w docelowym rozwiązaniu musisz zastosować multiprocessing.Process
    worker = threading.Thread(target=process, args=(queue, n_events))
    worker.start()
    worker.join()

    # wypisanie wyniku w formie w której serwer jej oczekuje
    # wynik zapisany jest w tablicy po 30 indeksów na dzień w kolejności ze słownika Help
    wynik = []
    for dd in range(0, n_days):
        dzien = {'day': dd}
        for name, idx in Help.items():
            dzien[name] = result[dd * len(Help) + idx]
        wynik.append(dzien)

    logging.info(f'Obliczenia zakończone w {time.perf_counter() - start:.3f} s, wysyłam wynik ({len(wynik)} dni)')
    res = requests.post(f"http://{SERVER_IP}:{SERVER_PORT}/results",
                        json={"ip_addr": CLIENT_IP, "port": CLIENT_PORT, "indeks": INDEKS, "aggregates": wynik})
    print_verdict(res)


def process(queue: Queue, n_events: int):
    global result
    global n_days

    inside = {p: [] for p in PARKINGS}  # kopiec (heapq) minut wyjazdu aut stojących na parkingu,
                                        # liczonych od początku dnia 0
    stays = {p: [] for p in PARKINGS}   # czasy postoju aut wpuszczonych w bieżącym dniu
    day = -1

    # pobieramy dokładnie n_events elementów - queue.empty() w multiprocessing nie jest wiarygodne
    # (może zwrócić True zanim wszystkie dane trafią do kolejki)
    # zgłoszenia przychodzą w kolejności (dzień, minuta wjazdu, numer biletu)
    for _ in range(n_events):
        e = queue.get()

        while day < e.day:  # zaczyna się nowy dzień
            if day >= 0:
                finish_day(day, stays)
            day += 1
            start_day(day, inside)

        base = e.day * len(Help)
        result[base + Help.get(e.parking + '_ENTRIES')] += 1

        heap = inside[e.parking]
        now = e.day * MINUTES_PER_DAY + e.enter
        # auta z wyjazdem w tej minucie lub wcześniej zwalniają miejsca
        while heap and heap[0] <= now:
            heapq.heappop(heap)

        if len(heap) < CAPACITY[e.parking]:
            heapq.heappush(heap, e.day * MINUTES_PER_DAY + e.exit)
            stay = e.exit - e.enter
            result[base + Help.get(e.parking + '_REVENUE')] += stay * RATE[e.parking]  # liczone do dnia wjazdu
            stays[e.parking].append(stay)
            idx = base + Help.get(e.parking + '_MAX_OCCUPANCY')
            result[idx] = max(result[idx], len(heap))
        else:
            result[base + Help.get(e.parking + '_REJECTED')] += 1  # parking pełny - auto odjeżdża

    if day >= 0:
        finish_day(day, stays)
    n_days = day + 1


def start_day(day, inside):
    # o 00:00 na parkingach stoją auta, które zostały z poprzednich dni
    midnight = day * MINUTES_PER_DAY
    for p in PARKINGS:
        heap = inside[p]
        while heap and heap[0] <= midnight:
            heapq.heappop(heap)
        result[day * len(Help) + Help.get(p + '_MAX_OCCUPANCY')] = len(heap)


def finish_day(day, stays):
    # zaokrąglenie przychodu oraz średnia i mediana postojów aut wpuszczonych w danym dniu
    base = day * len(Help)
    for p in PARKINGS:
        result[base + Help.get(p + '_REVENUE')] = round(result[base + Help.get(p + '_REVENUE')], 2)
        s = stays[p]
        result[base + Help.get(p + '_AVG_STAY')] = round(sum(s) / len(s), 2) if s else 0
        result[base + Help.get(p + '_MEDIAN_STAY')] = statistics.median(s) if s else 0
        stays[p] = []


# ---------------------------------------------------------------------------
# Komunikacja z serwerem - nie zmieniać
# ---------------------------------------------------------------------------

def print_verdict(res):
    if res.status_code != 200:
        logging.error(f'Serwer odrzucił wynik ({res.status_code}): {res.text[:300]}')
        return
    v = res.json()
    speedup = f", przyspieszenie względem wzorca x{v['speedup']:.2f}" if v.get('speedup') else ''
    processing = f" (przetwarzanie {v['processing']:.3f} s)" if v.get('processing') is not None else ''
    logging.info(f"WERDYKT SERWERA: {v['score']}/{v['total']} poprawnych, "
                 f"czas {v['duration']:.3f} s{processing}{speedup}")
    if v['missing_days']:
        logging.warning(f"Brakujące dni w wyniku: {v['missing_days'][:20]}")
    if v['extra_days']:
        logging.warning(f"Nadmiarowe dni w wyniku: {v['extra_days'][:20]}")
    if v['differences_count']:
        logging.warning(f"Różnice względem wzorca ({v['differences_count']}, pokazano {len(v['differences'])}):")
        for d in v['differences']:
            logging.warning(f"  dzień {d['day']:>4} {d['field']:<17} klient {d['client']:>10} "
                            f"wzorzec {d['expected']:>10} różnica {d['diff']:+}")


def register():
    """Rejestracja na serwerze - ponawiana, dopóki serwer nie odpowie."""
    while True:
        try:
            res = requests.post(f"http://{SERVER_IP}:{SERVER_PORT}/clients/handshake",
                                json={"ip_addr": CLIENT_IP, "port": CLIENT_PORT, "indeks": INDEKS}, timeout=5)
            if res.status_code == 201:
                logging.info(f'Zarejestrowano na serwerze {SERVER_IP}:{SERVER_PORT} jako {INDEKS}. Czekam na dane...')
                return
            logging.error(f'Serwer odrzucił rejestrację ({res.status_code}): {res.text}')
        except requests.RequestException:
            logging.warning(f'Serwer {SERVER_IP}:{SERVER_PORT} niedostępny - ponowna próba za 3 s')
        time.sleep(3)


@asynccontextmanager
async def lifespan(app):
    threading.Thread(target=register, daemon=True).start()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/parking-data", status_code=201)
async def create_parking_data(parking_events: List[ParkingEvent]):
    queue = multiprocessing.Queue()
    for el in parking_events:
        queue.put(el)
    logging.info(f'Otrzymano {len(parking_events)} zdarzeń - przetwarzanie')
    res = threading.Thread(target=function, args=(queue, len(parking_events)), daemon=True)
    res.start()


if __name__ == '__main__':
    # klient działa w terminalu: python main.py
    uvicorn.run(app, host=CLIENT_IP, port=CLIENT_PORT, log_level='warning')
