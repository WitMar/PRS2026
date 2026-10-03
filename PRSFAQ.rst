========================================
Przetwarzanie równoległe i strumieniowe
========================================

--------------
FAQ 
--------------

.. class:: important

    Klasy nie są nie niebieskie (zielone) nie można ich uruchomić.
    
Projekt nie jest zdefiniowany jako project Mavenowy. Kliknij lupkę i wpisz maven, wybierz opcję **+ Add maven project**. Odnajdź swój projekt i wybierz w nim plik o rozszerzeniu **.pom**.    

.. class:: important

    Nie widzę wszystkich gałęzi z repozytorium.
    
Wykonaj **Ctrl + T**. Jeżeli nie pomoże wykonaj **Git->Fetch**.   
    
.. class:: important

    Ctrl+T powoduje błędy repozytorium (nie mogę nadpisać pliku, jestem niezsynchronizowany).
    
Spróbuj zamiast tego wykonać **Git->Pull**. Jeżeli masz w opisie błędów napisane conflicts wybierz **Git->Megre Changes** i wskaż gałąź z której chcesz ściągnąć kod.    

.. class:: important

    Klasy z bibliotek (logera, hibernate, jsona) świecą się na czerwono.
    
Najpewniej nie ściągnięte są zależności Mavenowe. Kliknij na dwie strzałeczki w kółeczku z okienka Mavena poczekaj aż się skończą ładować.

.. class:: important

    Klasy Javy jak String świecą się na czerwono.
    
Nie jest zdefiniowane JDK, wejdź w **File->Project Structure->Project** i zobacz czy dobrze wybrane jest JDK oraz czy poziom Javy ustawiony jest na **8**.    

.. class:: important

    Inne rzeczy świecą się na czerwono.
    
Najedź na nie kursorem kliknij i wybierz **Alt+Enter** zobacz czy środowisko umie pomóc Ci rozwiązać problem.

.. class:: important

    Uruchamia się inna klasa niż bym chciał.
    
Sprawdź czy uruchamiasz odpowiednią klasę (test). Nazwa aktualnie uruchamianej klasy znajduje się obok zielonego trójkącika na górze na pasku. Środowisko **NIE** uruchamia klasy aktualnie edytowaj, tylko najczęściej ostatnio uruchamianą. Dla pewności uruchamiaj poprzez wybór prawym klawiszem myszy na nazwie klasy i **run**.    

.. class:: important

    Nie mogę uruchomić klasy.
    
Uruchamiać można tylko klasy zawierające metodę main.

.. class:: important

    Nie mogę zapisać zmian na repo.
    
Wybierz **Ctrl+k** by zapisać zmiany na dysku. Wybierz **Ctrl+Shift+k** by przesłać zmiany do repo.


