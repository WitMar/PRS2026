=======================
Pracownia Programowania
=======================

--------------------
Projekt
--------------------

.. class:: tag

    Projekt
    
Końcowy projekt wymagania:

Stworzenie aplikacji serwerowej oraz **niezależnego** klienta wykorzystujących REST API.

Aplikacja serwerowa powinna udostępniać utworzony wcześniej model danych w zakresie : dodawania, usuwania, edytowania, wyszukiwania (wylistowania) obiektów z bazy danych. Wszelkie założenia co do modelu danych opisanych dla przyrostu II obowiązują nadal. - 10 pkt

Dodatkowo aplikacja powinna posiadać endpointy udostępniające dla każdej tabeli jedną prostą statystykę : liczbę elementów, zbiór kategorii (jeżeli ma sens), średnią (jeżeli ma sens), najlepszy zespół (jeżeli ma sens) etc. - 10 pkt

Aplikacja serwerowa musi korzystać z silnika bazy danych takiego jak PostgreSQL, MySQL, MSSQL czy podobne. Komunikacja pomiędzy serwerem a światem zewnętrznym musi odbywać się przy pomocy REST API (innego standardu API na życzenie studenta). - 25 pkt

Aplikacja frontend musi mieć możliwość niezależnego uruchomienia (w odłączeniu od aplikacji serwerowej). Aplikacja frontend ma umożliwiać edycję, dodawanie, usuwanie danych z bazy danych oraz wyświetlać je w postaci tabeli, dodatkowo ogólny widok tabeli powinien być stronnicowany. - 25 pkt

Applikacja powinna być uruchomiona na osobnym serwerze aplikacji (np. Tomcat) / procesie systemowym. Nie w IDE. - 10 points

Dodatkowo aplikacja powinna być rozszerzona o pojedynczy aspekt nie omawiany na zajęciach taki jak : dodanie obłsugi "sesji użytkownika", integracja obsługi bazy danych w postaci Liquibase, integracja Springa z inną biblioteką, dodanie na froncie elementów raportów (wykresów, podsumowań), dodanie testów do aplikacji, dodanie testów obciążeniowych, partycjonowanie bazy danych, dodanie load balancera do Tomcata, każde inne wymyślone przez autora. Student sam wybiera, który aspekt aplikacji chciałby rozszerzyć i w jakim zakresie. - 20 pkt

W przypadku nie uzyskania łącznie 50% punktów, w terminie student zobowiązany jest jako "Projekt poprawkowy" do: 

    |  Uzupełnienia (oddania) nieoddanych projektów.
    |  Przygotowanie materiału do wybranych zajęć w oparciu o inne technologie (inny język programowania, edytor, program etc.)
