# Parkingi i ich parametry - STAŁE ZNANE TAKŻE KLIENTOWI (podane w treści zadania)
PARKINGS = ['P1', 'P2', 'P3', 'P4', 'P5']

# maksymalna liczba aut jednocześnie na parkingu
CAPACITY = {'P1': 20, 'P2': 35, 'P3': 15, 'P4': 50, 'P5': 10}

# stawka w zł za każdą minutę postoju
RATE = {'P1': 0.10, 'P2': 0.08, 'P3': 0.15, 'P4': 0.05, 'P5': 0.25}

# wartości liczone przez klienta dla każdego dnia i parkingu
AGGREGATE_TYPES = ['ENTRIES', 'REJECTED', 'MAX_OCCUPANCY', 'REVENUE', 'AVG_STAY', 'MEDIAN_STAY']

# pola pojedynczego dnia w odpowiedzi klienta, np. P1_ENTRIES, ..., P5_MEDIAN_STAY (30 pól)
AGGREGATES = [f'{p}_{a}' for p in PARKINGS for a in AGGREGATE_TYPES]

MINUTES_PER_DAY = 24 * 60

# odsetek aut zostających na noc (postój 10-40 godzin)
OVERNIGHT_SHARE = 0.08

# --- domyślne parametry generowania (można je zmienić w panelu serwera) ---

# liczba dni, dla których generowane są zdarzenia (dni numerowane od 0)
DAYS = 5

# średnia liczba aut na dzień przypadająca na 10 miejsc parkingowych
# (P1 o pojemności 20 dostanie średnio 2 * CARS_PER_10_SPOTS aut dziennie)
CARS_PER_10_SPOTS = 36

# tolerancja przy porównywaniu wyników (REVENUE jest liczbą zmiennoprzecinkową)
TOLERANCE = 0.01

# --- gotowe warianty eksperymentów (przyciski w panelu) ---
# poziom obciążenia CARS_PER_10_SPOTS wyznacza odsetek odrzuceń:
#   25 -> ok. 0%, 36 -> ok. 5%, 60 -> ok. 25% odrzuconych wjazdów
# liczba dni dobrana tak, by klient jednowątkowy liczył ok. 1 s / 10 s / 1 min
SIZES = [('S', 'mały', '~1 s'), ('M', 'średni', '~10 s'), ('L', 'duży', '~1 min')]
REJECTION_LEVELS = [('1', 'mało odrzuceń', 25, '~0%'),
                    ('2', 'średnio odrzuceń', 36, '~5%'),
                    ('3', 'dużo odrzuceń', 60, '~25%')]
VARIANT_DAYS = {
    'S1': 62, 'S2': 45, 'S3': 26,
    'M1': 510, 'M2': 355, 'M3': 212,
    'L1': 2700, 'L2': 1870, 'L3': 1110,
}
VARIANTS = [
    {'id': f'{s}{r}', 'size': size_name, 'expected_time': t, 'rejections': rej_name,
     'rejection_rate': rate, 'days': VARIANT_DAYS[f'{s}{r}'], 'cars_per_10_spots': cars}
    for s, size_name, t in SIZES
    for r, rej_name, cars, rate in REJECTION_LEVELS
]
MAX_DAYS = 5000

# wariant uruchamiany przez stary endpoint GET /start
DEFAULT_VARIANT = 'S2'
