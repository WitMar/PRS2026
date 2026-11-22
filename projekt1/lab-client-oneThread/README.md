# Aplikacja kliencka (wersja jednowątkowa – wzorzec)

Klient rejestruje się na serwerze, odbiera zdarzenia z parkingów, liczy wynik i odsyła go na serwer.

Kroki:

* Po uruchomieniu klient sam rejestruje się na serwerze (adres IP, port, nr indeksu) i ponawia próby, dopóki serwer nie odpowie
* Prowadzący uruchamia eksperyment w panelu serwera
* Serwer wysyła zdarzenia na `/parking-data`
* Klient liczy wynik i odsyła go na `/results` serwera
* Serwer odpowiada werdyktem: liczbą poprawnych wartości, czasem, przyspieszeniem względem wzorca
  sekwencyjnego i listą różnic. Klient wypisuje go w terminalu.

## Co liczy klient

Dla każdego dnia i parkingu (P1–P5):

Zgłoszenie przychodzi przy wjeździe i od razu zawiera czas wyjazdu:
`{parking, ticket, day, enter, exit}` (minuty od początku dnia wjazdu, `exit >= 1440` = auto zostaje na noc).

- `ENTRIES`: liczba zgłoszeń wjazdu (**można liczyć równolegle**),
- `REJECTED`: wjazdy odrzucone, bo parking był pełny (`CAPACITY`),
- `MAX_OCCUPANCY`: największa liczba aut jednocześnie na parkingu w ciągu dnia, łącznie z autami z poprzednich dni,
- `REVENUE`: wpuszczone auto płaci `(exit − enter) × RATE`, liczone do dnia wjazdu,
- `AVG_STAY`, `MEDIAN_STAY`: średni czas postoju i jego mediana (w minutach) dla aut wpuszczonych w danym dniu.

Zgłoszenia przychodzą **w kolejności zgłoszeń** (dzień, minuta wjazdu, numer biletu). Wszystko poza
`ENTRIES` zależy od stanu parkingu – także z poprzednich dni, bo auta zostają na noc – więc zgłoszenia
jednego parkingu trzeba przetworzyć **w tej kolejności**. Różne parkingi są jednak od siebie niezależne.
Uwaga: kilka procesów czytających z jednej kolejki dostaje zgłoszenia przemieszane – kolejność trzeba
wtedy odtworzyć albo rozdzielać dane według parkingu.

## Jak uruchomić

W `main.py` ustaw `SERVER_IP`, `SERVER_PORT` (podane na stronie głównej serwera), `CLIENT_IP`
(adres Twojego komputera w sieci), `CLIENT_PORT` i `INDEKS`, a następnie w terminalu:

```
pip install -r requirements.txt
python main.py
```

Przeglądarka nie jest potrzebna.

## Pomiar czasu (na serwerze)

- **czas całkowity**: od rozpoczęcia wysyłania danych do odebrania wyniku,
- **przetwarzanie**: od odpowiedzi 201 na `/parking-data` (dane odebrane i w kolejce) do odebrania wyniku.
  Wynik wysłany przed odpowiedzią 201 jest oznaczany ⚠.
