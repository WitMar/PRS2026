"""Porównanie wyniku klienta z wynikiem referencyjnym i zapis do app/results/."""
import json
from pathlib import Path

import app.constants as constants

APP_DIR = Path(__file__).resolve().parent


def compare(reference, aggregates):
    """Zwraca (poprawne, wszystkie, szczegóły per dzień, nadmiarowe dni, lista różnic)."""
    client_days = {a['day']: a for a in aggregates}
    ok = total = 0
    details = []
    differences = []
    for ref in reference:
        cli = client_days.get(ref['day'])
        row = {'day': ref['day'], 'missing': cli is None, 'values': {}}
        for name in constants.AGGREGATES:
            expected = ref[name]
            client_value = None if cli is None else cli[name]
            good = client_value is not None and abs(client_value - expected) < constants.TOLERANCE
            diff = None if client_value is None else round(client_value - expected, 4)
            ok += good
            total += 1
            row['values'][name] = {'client': client_value, 'server': expected, 'diff': diff, 'ok': good}
            if not good and cli is not None:
                differences.append({'day': ref['day'], 'field': name, 'client': client_value,
                                    'expected': expected, 'diff': diff})
        details.append(row)
    extra = sorted(set(client_days) - {r['day'] for r in reference})
    return ok, total, details, extra, differences


KEEP_PAYLOADS = 5  # tyle ostatnich eksperymentów trzyma pełne dane na dysku


def payload_paths(run_id):
    return (APP_DIR / "payloads" / f"run_{run_id}.json",
            APP_DIR / "payloads" / f"run_{run_id}_aggregates.json")


def save_payload(run_id, payload):
    with open(payload_paths(run_id)[0], "wb") as f:
        f.write(payload)
    remove_payload(run_id - KEEP_PAYLOADS, aggregates=False)


def remove_payload(run_id, aggregates=True):
    (APP_DIR / "payloads" / f"run_{run_id}.json").unlink(missing_ok=True)
    if aggregates:
        (APP_DIR / "payloads" / f"run_{run_id}_aggregates.json").unlink(missing_ok=True)


def save_result_file(indeks, sent_at, received_at, duration, processing, ref_time, ref_processing,
                     reference, received_days, ok, total, details, extra, differences):
    with open(APP_DIR / "results" / f"{indeks}.txt", "w") as f:
        f.write(f"Last data point was sent at {sent_at}, got client response at {received_at}, "
                f"diff: {duration}s\n")
        if processing is not None:
            f.write(f"Processing time (data acknowledged -> result received): {processing:.3f}s\n")
        else:
            f.write("Processing time: n/a (result arrived before data acknowledgement)\n")
        if ref_time:
            f.write(f"Sequential reference program: {ref_time:.3f}s total, {ref_processing:.3f}s processing\n")
        f.write(f"# days for which data aggregates were generated: {len(reference)}\n")
        f.write(f"# days received from client: {received_days}\n")
        missing = [r['day'] for r in details if r['missing']]
        if missing:
            f.write(f"# days missing in client response: {missing}\n")
        if extra:
            f.write(f"# unexpected days from client: {extra}\n")
        f.write(f"\nDifferences ({len(differences)}):\n")
        for d in differences:
            f.write(f"day {d['day']} {d['field']}: client {d['client']} != expected {d['expected']} (diff {d['diff']:+})\n")
        f.write(f"\nSummary : {ok}/{total}\n")
