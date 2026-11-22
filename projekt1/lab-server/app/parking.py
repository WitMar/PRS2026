"""Generowanie zdarzeń parkingowych."""
import random

import app.constants as constants


def generate_events(days, cars_per_10_spots, seed=None):
    """Zwraca listę zgłoszeń wjazdu w kolejności zgłoszeń (chronologicznie).

    Zgłoszenie: {parking, ticket, day, enter, exit} - przy wjeździe auto podaje od razu
    planowany wyjazd. enter i exit to minuty liczone od początku dnia wjazdu (day),
    exit >= 1440 oznacza wyjazd w kolejnym dniu (auto zostaje na noc).
    Generator NIE uwzględnia pojemności - to klient musi zasymulować,
    które auta zostaną odbite od pełnego parkingu.
    """
    rnd = random.Random(seed)
    events = []
    ticket = rnd.randint(1000, 9000)

    for day in range(days):
        for parking in constants.PARKINGS:
            mean = cars_per_10_spots * constants.CAPACITY[parking] / 10
            n_cars = max(1, round(mean * rnd.uniform(0.6, 1.3)))
            for _ in range(n_cars):
                ticket += 1
                enter = _arrival_minute(rnd)
                if rnd.random() < constants.OVERNIGHT_SHARE:
                    stay = rnd.randint(10 * 60, 40 * 60)  # postój przez noc
                else:
                    stay = int(rnd.expovariate(1 / 100)) + 5
                events.append({'parking': parking, 'ticket': ticket, 'day': day,
                               'enter': enter, 'exit': enter + stay})

    # kolejność zgłoszeń: dzień, minuta wjazdu, numer biletu
    events.sort(key=lambda e: (e['day'], e['enter'], e['ticket']))
    return events


def _arrival_minute(rnd):
    # szczyt poranny, popołudniowy i ruch w ciągu całego dnia
    r = rnd.random()
    if r < 0.35:
        m = rnd.gauss(8.5 * 60, 50)
    elif r < 0.6:
        m = rnd.gauss(16.5 * 60, 70)
    else:
        m = rnd.uniform(6 * 60, 22 * 60)
    return int(min(max(m, 0), constants.MINUTES_PER_DAY - 2))
