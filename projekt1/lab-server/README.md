# Serwer parkingów

Serwer generuje zdarzenia wjazdów i wyjazdów z 5 parkingów, wysyła je klientom
(studentom), odbiera wyniki i porównuje je z wynikiem referencyjnym. Wszystko
jest widoczne na żywo w panelu WWW.

## Panel WWW

`http://localhost:5678/`, a w nim:

- **9 gotowych eksperymentów** (rozmiar danych × poziom odrzuceń). Rozmiary to
  mały (~1 s), średni (~10 s) i duży (~1 min) dla klienta jednowątkowego.
  Poziomy odrzuceń to ok. 0%, 5% i 25%. Warianty są zdefiniowane w `app/constants.py`
  (`VARIANTS`). Tryb ręczny z własnymi parametrami jest schowany pod
  „Tryb ręczny”.
- W jednym eksperymencie wszyscy klienci dostają te same dane, a każdy
  eksperyment ma nowe, losowe dane.
- lista klientów ze statusem, czasem (licznik na żywo), poprawnością i szczegółami
  (lista różnic, porównanie każdej wartości ze wzorcem, historia czasów),
- **ranking studentów**: najlepszy poprawny czas w każdym wariancie, liczba
  rozwiązanych wariantów i średnia strata do najszybszego,
- lista eksperymentów; nieudany eksperyment można **usunąć**, co kasuje też
  jego wyniki z rankingu,
- podgląd wszystkich komunikatów (handshake, dane, wyniki, błędy walidacji JSON)
  z możliwością rozwinięcia treści.

## Protokół

- `POST /clients/handshake` `{ip_addr, port, indeks}` rejestruje klienta,
- serwer wysyła `POST http://klient:port/parking-data` z listą zdarzeń
  `{parking, ticket, day, enter, exit}` w kolejności zgłoszeń (exit liczony od początku dnia wjazdu, może być >= 1440),
- `POST /results` `{ip_addr, port, indeks, aggregates: [{day, P1_ENTRIES, P1_REJECTED, P1_MAX_OCCUPANCY, P1_REVENUE, P1_AVG_STAY, P1_MEDIAN_STAY, ..., P5_MEDIAN_STAY}]}`,
- `GET /start` (zgodność ze starą wersją) uruchamia wariant S2 dla wszystkich klientów,
- `GET /clients` zwraca listę klientów.

Wyniki porównania trafiają do `app/results/<indeks>.txt`, a dane eksperymentów
do `app/payloads/run_<nr>.json` (pełne dane trzymane są dla 5 ostatnich eksperymentów).

## Jak uruchomić

```
pip install -r requirements.txt
python -m uvicorn main:app --port 5678
```

Przy uruchomieniu w sieci: `python -m uvicorn main:app --host 0.0.0.0 --port 5678`.
Dokumentacja API: `http://localhost:5678/redoc`.
