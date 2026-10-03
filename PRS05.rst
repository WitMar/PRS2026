.. role:: todo

.. role:: raw-latex(raw)
            :format: latex html

==========================================
Przetwarzanie równoległe i strumieniowe
==========================================

.. class:: important 

    Uwaga! Kod z którego będziemy korzystać na zajęciach jest dostępny na branchu **projekt** w repozytorium https://github.com/WitMar/PRS2020 .

Jeżeli nie widzisz odpowiednich gałęzi na GitHubie wykonaj **Ctr+T**, a jak to nie pomoże to wybierz z menu **Git->Fetch**.    

Projekt opis
=====================================

W ramach projektu należy napisać rozwiązanie symulujące pracę magazynu.

Każdy student otrzymuje losowe 4 warunki, które ma spełnić z zakresu scenariuszy dostępnych w systemie, a są to:

Wycena

	| **CENA_BEZ_ZMIAN** - program odpowiada na zapytania o cenę, ale ona jest zawsze niezmienna.
	| **CENA_ZMIENNA** - program odpowiada na zapytania o cenę, ale ceny mogą zmieniać się w czasie działania magazynu.
	| **PROMO_CO_10_WYCEN** - program odpowiada na zapytania o cenę, które się nie zmieniają, ale co 10 *przychodzące* zapytanie traktowane jest jako promocja i wyceniane jest na 0.

Zamówienie 

	| **POJEDYNCZE** - program przyjmuje zamówienia na pojedyncze produkty, zamówienia zawsze są na 1 sztukę
	| **GRUPOWE** - program przyjmuje zamówienia na pojedyncze sztuki jak i na grupy produktów (grupa może liczyć 1 produkt), zamówienia zawsze są na 1 sztukę każdego produktu
	| **REZERWACJA** - program przyjmuje rezerwacje, które są pobierane ze stanów magazynowych i odbierane przez zadanie odbiór zamówienia
	
Zaopatrzenie

	| **POJEDYNCZE** - program przyjmuje do magazynu zaopatrzenie z pojedynczymi produktami, zaopatrzenie dodaje zawsze 1 sztukę
	| **GRUPOWE** - program przyjmuje do magazynu zaopatrzenie z pojedynczymi produktami jak i z grupami produktów, zaopatrzenie dodaje zawsze 1 sztukę kazdego produktu

Wydarzenie

	| **WYCOFANIE** - program obsługuje wycofanie produktu ze sprzedaży, które ustala stan magazynowy na -9999999L oraz przywrócenie produktu które zeruje stan magazynu, gdy produkt jest wycofany ze sprzedaży nie obsługujemy jego zaopatrzenia
	| **INWENTARYZACJA** - program obsługuje zapytania o inwentaryzację, które musi wypisać stan magazynu na dokładny moment wystąpienia inwentaryzacji
	| **RAPORT_SPRZEDAŻY** - program obsługuje zapytania o raport sprzedaży, na które musi odpowiedzieć raportem ze sprzedaży (produkt, liczba sprzedanych sztuk) na dokładny moment wystąpienia prośby o raport
	
Każde z warunków obsługuje tylko wybrane typy akcji przychodzących na kolejkę zdarzeń, odpowiednio:

    | CENY_BEZ_ZMIAN((WycenaAkcje.PODAJ_CENE)),
    | CENA_ZMIENNA((WycenaAkcje.PODAJ_CENE, WycenaAkcje.ZMIEN_CENE)),
    | PROMO_CO_10_WYCEN((WycenaAkcje.PODAJ_CENE));
    | WYCOFANIE((WydarzeniaAkcje.WYCOFANIE, WydarzeniaAkcje.PRZYWROCENIE)),
    | INWENTARYZACJA((WydarzeniaAkcje.INWENTARYZACJA)),
    | RAPORT_SPRZEDAŻY((WydarzeniaAkcje.RAPORT_SPRZEDAŻY));
    | POJEDYNCZE ((ZamowieniaAkcje.POJEDYNCZE_ZAMOWIENIE)),
    | GRUPOWE ((ZamowieniaAkcje.POJEDYNCZE_ZAMOWIENIE, ZamowieniaAkcje.GRUPOWE_ZAMOWIENIE)),
    | REZERWACJE ((ZamowieniaAkcje.POJEDYNCZE_ZAMOWIENIE, ZamowieniaAkcje.REZERWACJA, ZamowieniaAkcje.ODBIÓR_REZERWACJI));
    | POJEDYNCZE ((ZaopatrzenieAkcje.POJEDYNCZE_ZAOPATRZENIE)),
    | GRUPOWE ((ZaopatrzenieAkcje.POJEDYNCZE_ZAOPATRZENIE, ZaopatrzenieAkcje.GRUPOWE_ZAOPATRZENIE));

W ramach projektu istnieje Generator, który po uruchomieniu klasy **SpringRedisApplication.java** (i otrzymaniu logu o treści application started) umożliwia generowanie zadań. Zadania generowane są losowo, ich liczbę definiujemy w pliku application.yml. Tam też należy umieścić swój numer indeksu oraz wybrane - otrzymane scenariusze, które musimy spełnić. Program filtruje losowe zgłoszenia tak, by docierały do nas tylko te z naszego scenariusza.

.. class:: highlight

.. code:: java

  ustawienia:
    numerIndeksu: 287046
    wycena: "CENY_BEZ_ZMIAN"
    zamowienia: "POJEDYNCZE"
    zaopatrzenie: "POJEDYNCZE"
    wydarzenia: "WYCOFANIE"
    liczbaZadan: 200
    
Aby wygenerować zadania należy wejść przeglądarką na adres http://localhost:8080/action/generate .    
	
Przedmiotem zainteresowania Państwa jest klasa **ParallelExecutor**. Odbiera ona zadania z rozproszonej kolejki, filtruje i przekazuje do lokalnej kolejki o nazwie kolejka (metoda process). Państwa celem jest napisanie metody threadProcess, która to przetwarza zadania z lokalnej kolejki, aktualizując stany magazynowe i przesyłając odpowiedzi na zadania. 

Dodatkowo w projekcie istnieje jednowątkowy process **SequenceRunner.java**, który przetwarza te same zadania sekwencyjnie na jednym wątku. Państwa zadaniem jest napisanie implementacji w **ParallelExecutor** tak, by działała szybciej niż SequenceRunner ale jednocześnie spełniała założenia, że wykonanie daje taki sam wynik jak SequenceRunner. Po zakończeniu przetwarzania SequenceRunner uruchamia zestaw testów sprawdzających poprawność wykonania Państwa implementacji. 

Uwaga! W momencie oddawania projektów mogą pojawić się dodatkowe metody sprawdzające poprawność.

Uwaga! Czas działania programów będzie w 5% częścią finalnej oceny. 

Dla przykładu obecna implementacja **ParallelExecutor** uruchamia dwa wątki, które nie dbają o kwestie przetwarzania równoległego przychodzących zadąń co prowadzi do błędów wykonania (ale nie zawsze, im więcej zadań tym większa szansa na błąd). Kilkukrotne uruchomienie powinno dać przynajmniej raz jakiś błąd. W przypadku oceniania projektów, też planowana jest seria uruchomień projektów, gdzie za każde poprawne uruchomienie uzyskiwać będą Państwo punkty.

Walidacja wyniku odbywa się w klasie Ledger.java w metodzie evaluate. Każda akcja ma przypisany numer id które rosną od zera do liczby zadań i mogą pomóc w przetwarzaniu.

Walidacja warunki:

	| **Czas** działania (pomiędzy przesłaniem pierwszej a ostatniej odpowiedzi) jest niższy niż czas działania alorytmu jednowątkowego (SequenceRunner).
	
	| **Liczba zaakceptowanych** oraz **niezaakceptowanych** zamówień (gdy nie ma dostatecznej liczby produktów) musi być taka sama przy obu uruchomieniach - co znaczy, że odebranie zaopatrzenia musi poczekać na wykonanie wszystkich zamówień, lub w inny sposób należy kontrolować ich odbieranie.
	
	| **Stan magazynu** na koniec musi być taki jak w przypadku działania sekwencyjnego
	
	| **Ceny produktów** na koniec muszą być takie jak w przypadku działania sekwencyjnego
	
	| Odpowiedzi odnośnie **cen produktów** muszą być takie same jak w przypadku działania sekwencyjnego. Uwaga! Kolejność tych odpowiedzi nie ma znaczenia! Ma znaczenie jednak czy pytanie o cenę wystąpiło po zmianie ceny oraz akcja z którym id była promocyjnym zapytaniem.
	
	| Odpowiedzi odnośnie **inwentaryzacji** muszą być takie same jak w przypadku działania sekwencyjnego. Inwentaryzacja musi odbywać się w tym samym czasie, jak w przypadku działania sekwencyjnego - innymi słowy nie powinniśmy obsługiwać zdarzeń zmieniających magazyn przychodzących po niej, zanim jej nie przeprowadzimy, jednocześnie musimy zaczekać na wykonanie zadań zmieniających stan magazynu zanim przeprocesujemy ją samą.
	
	| Odpowiedzi odnośnie **raportu** sprzedaży muszą być takie same jak w przypadku działania sekwencyjnego. Działa podobnie jak inwentaryzacja, tylko dotyczy samych zamówień.
	

Podział:

421831
PROMO_CO_10_WYCEN POJEDYNCZE POJEDYNCZE WYCOFANIE

426372
CENY_BEZ_ZMIAN GRUPOWE POJEDYNCZE INWENTARYZACJA

424322
PROMO_CO_10_WYCEN REZERWACJE POJEDYNCZE RAPORT_SPRZEDAŻY

394049
CENY_BEZ_ZMIAN POJEDYNCZE GRUPOWE INWENTARYZACJA

434881
CENY_BEZ_ZMIAN GRUPOWE GRUPOWE WYCOFANIE

444622
PROMO_CO_10_WYCEN POJEDYNCZE GRUPOWE INWENTARYZACJA

435466
CENY_BEZ_ZMIAN GRUPOWE POJEDYNCZE RAPORT_SPRZEDAŻY

424200
CENY_BEZ_ZMIAN GRUPOWE GRUPOWE WYCOFANIE

461015
CENY_BEZ_ZMIAN GRUPOWE POJEDYNCZE RAPORT_SPRZEDAŻY

424343
CENA_ZMIENNA GRUPOWE POJEDYNCZE INWENTARYZACJA

461013
CENY_BEZ_ZMIAN REZERWACJE POJEDYNCZE RAPORT_SPRZEDAŻY

461012
CENA_ZMIENNA POJEDYNCZE POJEDYNCZE INWENTARYZACJA

434901
PROMO_CO_10_WYCEN POJEDYNCZE POJEDYNCZE INWENTARYZACJA

461011
CENY_BEZ_ZMIAN REZERWACJE POJEDYNCZE RAPORT_SPRZEDAŻY

461010
CENA_ZMIENNA REZERWACJE POJEDYNCZE RAPORT_SPRZEDAŻY

461009
CENY_BEZ_ZMIAN GRUPOWE POJEDYNCZE RAPORT_SPRZEDAŻY

461008
CENY_BEZ_ZMIAN REZERWACJE GRUPOWE INWENTARYZACJA

426078
PROMO_CO_10_WYCEN GRUPOWE POJEDYNCZE RAPORT_SPRZEDAŻY

461021
CENY_BEZ_ZMIAN POJEDYNCZE GRUPOWE INWENTARYZACJA

461020
CENY_BEZ_ZMIAN GRUPOWE GRUPOWE RAPORT_SPRZEDAŻY

433245
PROMO_CO_10_WYCEN POJEDYNCZE POJEDYNCZE INWENTARYZACJA

461018
PROMO_CO_10_WYCEN POJEDYNCZE GRUPOWE INWENTARYZACJA

436440
CENY_BEZ_ZMIAN GRUPOWE POJEDYNCZE INWENTARYZACJA

460889
PROMO_CO_10_WYCEN POJEDYNCZE GRUPOWE WYCOFANIE

437862
CENA_ZMIENNA POJEDYNCZE GRUPOWE INWENTARYZACJA

436454
CENA_ZMIENNA REZERWACJE POJEDYNCZE RAPORT_SPRZEDAŻY

439655
CENY_BEZ_ZMIAN GRUPOWE POJEDYNCZE INWENTARYZACJA

434850
CENA_ZMIENNA REZERWACJE POJEDYNCZE INWENTARYZACJA

433250
CENY_BEZ_ZMIAN REZERWACJE POJEDYNCZE WYCOFANIE

433248
CENY_BEZ_ZMIAN REZERWACJE POJEDYNCZE INWENTARYZACJA

468655
CENY_BEZ_ZMIAN GRUPOWE POJEDYNCZE WYCOFANIE

468654
PROMO_CO_10_WYCEN REZERWACJE POJEDYNCZE INWENTARYZACJA

468653
CENY_BEZ_ZMIAN GRUPOWE GRUPOWE WYCOFANIE

426806
PROMO_CO_10_WYCEN GRUPOWE POJEDYNCZE RAPORT_SPRZEDAŻY

434999
CENA_ZMIENNA POJEDYNCZE GRUPOWE WYCOFANIE

434871
CENY_BEZ_ZMIAN POJEDYNCZE GRUPOWE RAPORT_SPRZEDAŻY

416244
CENA_ZMIENNA POJEDYNCZE POJEDYNCZE INWENTARYZACJA

406128
PROMO_CO_10_WYCEN GRUPOWE POJEDYNCZE INWENTARYZACJA

416381
CENA_ZMIENNA REZERWACJE POJEDYNCZE WYCOFANIE

424317
CENY_BEZ_ZMIAN REZERWACJE POJEDYNCZE INWENTARYZACJA	

**Update** 28.III.2022 dodano opis warunków walidacji
