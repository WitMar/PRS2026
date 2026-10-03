.. role:: todo

.. role:: raw-latex(raw)
            :format: latex html

==========================================
Przetwarzanie równoległe i strumieniowe
==========================================

Projekt II opis
=====================================

W ramach projektu należy napisać proste przetwarzanie danych.

W zależności od wykonania zadań student otrzymuje punkty wg listy na końcu opisu.

Student ma za zadanie przetwarzać dane zapisane na serwerze Kafka (w przypadku, gdy student nie chce skorzystać z Kafki może korzystać z danych z pliku lub kolekcji w Pythonie, dane jednak mają być sensowne i realne).

Kafka serwer adres : 150.254.78.69:29092 (IP : port)

Dostępne na Kafce są na bieżąco uzupełniane dane w topicach:

**air_poznan** - informacje o jakości powietrza w Poznaniu ze stacji Poznań - Dąbrowskiego

źródło danych: https://powietrze.gios.gov.pl/pjp/content/api
częstotliwość odświeżania: 1h

format danych :

.. class:: highlight

.. code:: python

	{"SO2": 9.2681, "date": "2022-06-04 18:00:00", "PM10": 18.4511, "C6H6": 0.1978, "CO": 320.62, "NO2": 17.3031, "O3": 116.843, "PM2.5": 10.6337}

**temp_poznan** - dane meteorologiczne z Poznania

źródło danych: https://openweathermap.org/current
częstotliwość odświeżania: 5 min

.. class:: highlight

.. code:: python

	{'temp': 21.78, 'temp_feel': 21.78, 'temp_min': 21.32, 'temp_max': 22.53, 'pressure': 1019, 'humidity': 52, 'visibility': 10000, 'wind_speed': 1.03, 'sunrise': '06-04-2022 04:34:03', 'sunset': '06-04-2022 21:07:22'}

**bitcoin** - kurs waluty bitcoin w stosunku do wybranych walut światowych i dwóch wybranych walut internetowych

źródło danych: https://www.coingecko.com/en/api/documentation#
częstotliwość odświeżania: 5 min

.. class:: highlight

.. code:: python

	{"Bitcoin": 1.0, "eth": 16.739, "ltc": 470.6, "usd": 29730.174, "aud": 41249.576, "cad": 37447.235, "chf": 28593.203, "eur": 27735.963, "gbp": 23806.05, "pln": 127312.038}

Dane na serwerze Kafka proszę zapisywać w topicu o nazwie będący numerem Państwa indeksu (jeżeli nie chcemy zapisywać możemy też dane wypisywać na ekran lub do pliku).

Na ocenę końcową składać się będą procenty w zależności od wykonania poniższych elementów, wszystkie są traktowane **niezależnie** czyli jak wczytam dane z Kafki przetworzę i wypiszę do Kafki to wykonuje tym samym trzy niezależne punkty, jak wczytam dane z Kafki, przetworzę i wypiszę na ekran to wykonam dwa itd.

	| Stworzenie źródła danych i pobranie danych z serwera Kafka - 20%
	| Przetwarzanie danych za pomoca TABLE API (dowolne, w miare sensowne podsumowanie) 10%
	| Przetwarzanie danych za pomoca SQL API (dowolne w miare sensowne podsumowane) 10%
	| Przetwarzanie danych za pomoca SQL API wykorzystując podzapytanie (dowolne w miare sensowne podsumowane) 10% *
	| Stworzenie ujścia danych jako topic w Kafce i zapisanie tam wyniku 10% *
	| Przetwarzanie danych za pomoca **okna** danych w TABLE API (dowolne w miare sensowne podsumowane) 10%
	| Przetwarzanie danych za pomoca **okna** danych w SQL API (dowolne w miare sensowne podsumowane) 10%
	| Przetwarzanie danych za pomocą fukcji stanu, własna zaawansowana funkcja przetwarzania 20%

* zadania wychodzące poza zakres przedstawiony na zajęciach, ale łatwo znajdywalne w dokumentacji lub w sieci.
