
=======================
Pracownia Programowania
=======================

--------------------
Projekt
--------------------

.. class :: tag

    Projekt z tematów 1-4
    
Zadanie:

Napisz program działający w terminalu (konsoli, inaczej proram tesktowy), który będzie analizował dane meteorologiczne z linka (odczyty sensorów z sensor community z rejonu Warszawy)

    | https://data.sensor.community/airrohr/v1/filter/box=52.36734243199027,20.819494415027485,52.09692843752652,21.319390572461643

Model danych (wygenerowane online klasy z formatu json) można znaleźć tutaj:

	| https://mw.home.amu.edu.pl/zajecia/PRA2025/model.zip
	
Program powinien wypisywać dowolne statystyki z odczytanych danych wymyślone przez użytkownika (np średnie temp, wilgotność, liczbę miejsc o dużej temp, dużym zanieczyszczeniu powietrza itp) 
i mieć możliwość zapisania tych statystyl w trzech formatach do wyboru: pliku PDF, json lub xml. Wykorzystaj dowolną bibliotekę Javy do tworzenia plików PDF. Postać pliku jest dowolna.

Napisz testy do wyrzystywanych metod, skorzystaj obowiązkowo z zamockowania danych dla danych pobieranych z data.sensor.

W programie wykorzystaj strumienie oraz co najmniej jedną strukturę danych (set, map, list, stack, etc.). 

Przykłąd wywołania:

.. code:: xml

		Statystyki:
		.........
		.........
		.........
		Zapisz jako:
		P-Pdf J-Json X-xml
		>>P
		Zapisanow wynik do pliku pdf

------------------------
Zapytania HTTP in Java
------------------------

Możemy wykonywać żądania HTTP z kodu, najprościej użyć biblioteki Apache.httpclient.

.. code:: xml

      <dependency>
            <groupId>org.apache.httpcomponents</groupId>
            <artifactId>httpclient</artifactId>
            <version>4.5.10</version>
      </dependency>

Wykonanie zapytania GET:

.. code:: java

					DefaultHttpClient httpClient = new DefaultHttpClient();
                    HttpGet getRequest = new HttpGet(
                            "https://data.sensor.community/airrohr/v1/filter/box=52.36734243199027,20.819494415027485,52.09692843752652,21.319390572461643");
                    getRequest.addHeader("accept", "application/json");

                    HttpResponse response = httpClient.execute(getRequest);

                    if (response.getStatusLine().getStatusCode() != 200) {
                        throw new RuntimeException("Failed : HTTP error code : "
                                + response.getStatusLine().getStatusCode());
                    }

                    BufferedReader br = new BufferedReader(
                            new InputStreamReader((response.getEntity().getContent())));
                    StringBuilder sb = new StringBuilder();
                    String line;
                    while ((line = br.readLine()) != null) {
                        sb.append(line);
                    }
                    String json = sb.toString();
                    ObjectMapper mapper = new ObjectMapper();
                    
Wykorzystanie modelu

.. code:: java

		ArrayList<Root> obj = mapper.readValue(...........                  

-------------
Ocena
-------------

Testy - test zmockowanego zapytania, co najmiej 3 scenariusze testów, 2xPozytywny, Negatywny - np złe dane wejściowe : 30%

Strumienie - wykorzystanie strumienia do przetwarzania informacji: 10%

Serializacja i Deserializacja JSON + XML: 20%

Biblioteka PDF: 20%

Działanie zgodne ze specyfikacją i pobieranie prawidłowych danych 20%

    


    
    
