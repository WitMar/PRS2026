"""Wzorcowy program SEKWENCYJNY.

Serwer uruchamia go jako osobny proces dla każdego eksperymentu:

    python -m app.reference app/payloads/run_1.json app/payloads/run_1_aggregates.json

Program liczy wynik tak samo jak jednowątkowy klient-wzorzec (kolejka multiprocessing,
jedna pętla po wszystkich zgłoszeniach), więc jego czas jest punktem odniesienia dla klientów studentów,
a jego wynik służy do sprawdzenia poprawności ich odpowiedzi.
Na standardowe wyjście wypisuje JSON {"duration": s, "processing": s, "days": n, "events": n}:
duration liczony od parsowania JSON, processing od chwili, gdy dane są już w kolejce
(odpowiednik czasu klienta od potwierdzenia odbioru danych do wysłania wyniku).
"""
import heapq
import json
import multiprocessing
import statistics
import sys
import time
from multiprocessing import Queue
from typing import List

from pydantic import BaseModel, TypeAdapter

from app.constants import PARKINGS, CAPACITY, RATE, AGGREGATE_TYPES, MINUTES_PER_DAY

Help = {f'{p}_{a}': i * len(AGGREGATE_TYPES) + j
        for i, p in enumerate(PARKINGS) for j, a in enumerate(AGGREGATE_TYPES)}


class ParkingEvent(BaseModel):
    parking: str
    ticket: int
    day: int
    enter: int  # minuta wjazdu liczona od początku dnia day
    exit: int   # minuta wyjazdu liczona od początku dnia day (>= 1440 - kolejny dzień)


def process(queue: Queue, n_events, result):
    """Jedna pętla po wszystkich zgłoszeniach w kolejności przyjścia - liczy wszystkie wartości.

    Auto jest na parkingu w minutach [wjazd, wyjazd); wyjazd w minucie t zwalnia miejsce
    dla wjazdu w tej samej minucie. Postój i przychód liczą się do dnia wjazdu.
    Zwraca liczbę dni.
    """
    inside = {p: [] for p in PARKINGS}  # kopiec minut wyjazdu (od początku dnia 0)
    stays = {p: [] for p in PARKINGS}   # postoje aut wpuszczonych w bieżącym dniu
    day = -1
    for _ in range(n_events):
        e = queue.get()
        while day < e.day:
            if day >= 0:
                finish_day(day, stays, result)
            day += 1
            start_day(day, inside, result)

        base = e.day * len(Help)
        result[base + Help[e.parking + '_ENTRIES']] += 1
        heap = inside[e.parking]
        now = e.day * MINUTES_PER_DAY + e.enter
        while heap and heap[0] <= now:
            heapq.heappop(heap)
        if len(heap) < CAPACITY[e.parking]:
            heapq.heappush(heap, e.day * MINUTES_PER_DAY + e.exit)
            stay = e.exit - e.enter
            result[base + Help[e.parking + '_REVENUE']] += stay * RATE[e.parking]
            stays[e.parking].append(stay)
            idx = base + Help[e.parking + '_MAX_OCCUPANCY']
            result[idx] = max(result[idx], len(heap))
        else:
            result[base + Help[e.parking + '_REJECTED']] += 1
    if day >= 0:
        finish_day(day, stays, result)
    return day + 1


def start_day(day, inside, result):
    # auta, które zostały z poprzednich dni, liczą się do zajętości od 00:00
    midnight = day * MINUTES_PER_DAY
    for p in PARKINGS:
        heap = inside[p]
        while heap and heap[0] <= midnight:
            heapq.heappop(heap)
        result[day * len(Help) + Help[p + '_MAX_OCCUPANCY']] = len(heap)


def finish_day(day, stays, result):
    base = day * len(Help)
    for p in PARKINGS:
        result[base + Help[p + '_REVENUE']] = round(result[base + Help[p + '_REVENUE']], 2)
        s = stays[p]
        result[base + Help[p + '_AVG_STAY']] = round(sum(s) / len(s), 2) if s else 0
        result[base + Help[p + '_MEDIAN_STAY']] = statistics.median(s) if s else 0
        stays[p] = []


def compute(raw_json):
    events = TypeAdapter(List[ParkingEvent]).validate_json(raw_json)
    queue = multiprocessing.Queue()
    for el in events:
        queue.put(el)
    queued = time.perf_counter()  # odpowiednik momentu, w którym klient odsyła 201

    result = [0] * len(Help) * 5000
    n_days = process(queue, len(events), result)

    aggregates = []
    for dd in range(n_days):
        row = {'day': dd}
        for name, idx in Help.items():
            row[name] = result[dd * len(Help) + idx]
        aggregates.append(row)
    return aggregates, len(events), queued


def main(payload_path, out_path):
    with open(payload_path, 'rb') as f:
        raw = f.read()
    start = time.perf_counter()
    aggregates, n_events, queued = compute(raw)
    end = time.perf_counter()
    duration, processing = end - start, end - queued
    with open(out_path, 'w') as f:
        json.dump(aggregates, f, indent=1)
    print(json.dumps({'duration': duration, 'processing': processing,
                      'days': len(aggregates), 'events': n_events}))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
