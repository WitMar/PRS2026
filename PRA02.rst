.. role:: todo

.. role:: hold

.. role:: important

.. role:: badimportant

.. role:: raw-latex(raw)
            :format: latex html

==========================================
Pracownia Programowania
==========================================

------------------------------------
Debugowanie i Testowanie
------------------------------------

.. class:: important 

    Uwaga! Kod z którego będziemy korzystać na zajęciach jest dostępny na branchu **TestAndDebugStart** w repozytorium https://github.com/WitMar/PRA2025  . Kod końcowy można znaleźć na branchu **TestAndDebugEnd**.


Jeżeli nie widzisz odpowiednich gałęzi na GitHubie wykonaj **Ctr+T**, a jak to nie pomoże to wybierz z menu **Git->Fetch**.     

Podsumowanie zajęć I
======================

Co wiemy po pierwszych zajęciach:

    | * Projekt podzielony jest na katalogi: źródłowy - :todo:`src`, testowy - :todo:`test`, zasobów - :todo:`resources`.

    | * W katalogu projektu umieszczony jest plik **pom.xml** odpowiadający za ustawienia Mavena, w pliku tym dodajemy odnośniki do zewnętrznych bibliotek i ustawienia budowania aplikacji.
    
    | * Ustawienia dodatkowych bibliotek znajdziemy w plikach w katalogu resources.
    
    | * Pracujemy na GIT - nowa funkcjonalność (nowy temat zajęć) zakładana jest na nowej gałęzi (ang. *branch*).     

Synchronizacja kodu Git z oryginalnym repo
===========================================

Stwórz swoje własne repozytorium na GitHub.

Przejdź do **Git -> Manage Remotes**

Dodaj wpis kierujący na Twoje repozytorium

    | https://github.com/LINK_CO_MOJEGO_REPO
    
nazwij je najlepiej jako **MojeRepozytorium**    

Wybierz :hold:`Ctrl + T`, aby odświeżyć zależności.

Jeżeli Ctrl+T z jakiegoś powodu nie ściągnie oczekiwanych zmian, to żeby wymusić ściągnięcie zmian wybierz **Git -> fetch**.

Wtedy na liście branchy w prawym dolnym rogu ekranu powinieneś widzieć gałęzie z repo przedmiotowego i ze swojego. 

Przejdź na gałąź **TestAndDebugStart**.

Jako że dodaliśmy nowe repozytorium, możliwe, że musisz ponownie skonfigurować mavena. Przejdź do zakładki Maven i sprawdź, czy widzisz goale (Lifecycle, Plugin, Dependencies), jeżeli nie, spróbuj odświeżyć Mavena (dwie strzałki w kółko). Jeśli to nie pomoże wybierz lupkę wpisz add maven project i wskaż plik **pom.xml** z dysku twardego. Następnie odśwież ponownie Mavena. To powinno pomóc - sprawdź, czy twoje pliki .java mają niebieskie kółko obok nich w zakładce **Project**.

.. class:: center
	
.. image:: mavenTryAgain.png

Przydatne skróty IdeaJ
=======================

Lista skrótów IdeaJ

    | https://resources.jetbrains.com/storage/products/intellij-idea/docs/IntelliJIDEA_ReferenceCard.pdf
    

:hold:`Alt + Enter` pokaż podpowiedź rozwiązania błędu
    
:hold:`Ctrl + W`, :hold:`Ctrl + Shift + W` zaznaczenie całej sekcji, rozszerzenie zaznaczenia, zawężenie zaznaczenia.

:hold:`Ctrl + Shift + N` wyszukanie pliku po nazwie

:hold:`Shift + Shift` wyszukiwanie wszędzie

:hold:`Alt + Insert` generuj kod

:hold:`Ctrl + /` zakomentuj line

:hold:`Ctrl + Shift + /` odkomentuj linie

:hold:`Ctrl + E` ostatnio otwierane pliki

:hold:`Ctrl + Alt + L` formatuj kod

:hold:`Tab`, :hold:`Shift+Tab` wcięcie, cofnij wcięcie

:hold:`Shift + F6` zmiana nazwy

:hold:`Ctrl + Shift + Alt + T` refaktoruj

:hold:`Ctrl + Alt + M` wyekstraktuj metodę

:hold:`Alt + Right/Left` przełączaj zakładki

:hold:`Ctrl + Alt + Right / Left` nawiguj wstecz / do przodu (uwaga pod Linux system już używa tego skrótu więc trzeba zmenić ustawienia systemu)

:hold:`Ctrl + (klik na nazwie metody)` pokaż użycie

:hold:`Ctrl + Alt + (klik na nazwie metody)` pokaż implementację

:hold:`Ctrl + K` służy do commitowania kodu lokalnie do repozytorium

:hold:`Ctrl + Shift + K` służy do commitowania kodu do zewnętrznego repozytorium

:hold:`Ctrl + T` służy do odświeżania projektu - ściągania zmian z serwera

:badimportant:`Uwaga!!` Jeśli używasz Linuksa lub innego systemu operacyjnego innego niż Windows (lub zdalnego pulpitu), niektóre z tych skrótów mogą być już zarezerwowane w systemie, wtedy musisz zmienić ustawienia systemowe lub zmienić je w **Settins->Keymap** w Intellij

.. class:: tag

    Wykonaj

Przedź na branch **TestAndDebugStart**

Wyszukaj klasę o nazwie **ClassThatHaveItAll** (Ctrl + Shift + N).

Zformatuj kod (Ctrl + Alt + L) - na wydziałowym linuxie ten skrót oznacza wyloguj, musisz zmienić skrót w ustawieniach systemu żeby móc go używać lub zmienić skrót w środowsiku (Settings->Keymap).

Dodaj do klasy w nagłówku linijkę 

.. class :: highlight

.. code :: java

     List <Long> list;

Wybierz automatyczną poprawę błędu (Alt + Enter). 

Następnie wybierz (Alt + Insert) wygeneruj konstruktor, oraz settery i gettery dla klasy.

Znajdź interfejs **InterfaceOne** (Ctr + Shift + f). Wyszukaj użycie (Ctrl + click na nazwie metody) i implementacje metody (Ctrl + Alt + click na nazwie metody) **printMe()** klikając na definicje metody w interfejsie. 

Sprawdź, jak poruszać się między zakładkami (Alt + prawo / lewo) i przejść do poprzednich zmian (Ctrl + Alt + prawo / lewo).

Debug
======

Przejdź do klasy **Breakpoints** pakietu **debug**.

Poprzez wybór **Run -> Debug**  lub wybierając na klasie prawym przyciskiem myszy **Debug** możemy debugować nasz kod czyli uruchamiać w kontrolowany sposób, tak by móc zatrzymywać w dowolnym momencie wywołanie kodu.

Czym jest debugowanie?

    |	https://www.codeproject.com/Articles/991643/What-is-Debugging-How-to-Debug-A-Beginners-Guide

Aby uruchomić kod lub uruchomić debuggowanie możesz też kliknąć prawym przyciskiem na zielony trójkąt obok nazwy klasy i wybrać opcję DEBUG.

.. class:: center
	
.. image:: hereForDebug.png

Pomocne w debugowaniu są tzw. **breakpointy**, czyli miejsce w kodzie, w którym chcemy zatrzymać wywołanie kodu by móc podejrzeć wartości zmiennych i stan programu. Żeby dodać breakpoint klikamy obok numeru linii tak, by pojawiła się czerwona kropka.

.. class:: center
	
.. image:: breapoint.png

Po kliknięciu prawym przyciskiem myszy możemy określić także specjalny warunek przy breakpoincie.

.. class:: center
	
.. image:: warunek.png

Po uruchomieniu trybu debug na dole pojawia się nam okno debugowania na którym wyświetlone są aktualne wartości zmiennych. Dodatkowo możemy wybrać przez :hold:`Alt+F8` lub klikając na ikonę kalkulatora okno ewaluacji wyrażeń i wykonać ewaluację jakiegoś wyrażenia na obecnych wartościach zmiennych. Ewaluacja wyrażeń jest przydatna przy debugowaniu np. wartości list, których wartości nie jesteśmy w stanie przejrzeć pojedynczo.

.. class:: center
	
.. image:: debug.png

Przy odpowiednich ustawieniach możliwe jest także debugowanie aplikacji działających na serwerze w czasie uruchomienia (więcej na ten temat na przyszłych zajęciach).

.. class:: tag

    Wykonaj
    
Uruchom klasę **Breakpoints**. Jaki błąd wystąpił?

Uruchom debug klasy **Breakpoints**.

Żeby zatrzymać wywołanie dodaj breakpoint w klasie.

Użyj F8 (lub strzałka w dół na panelu debugingu) aby przejść w wywołaniu kodu linijka po linijce.

Użyj StepInto F7 (strzała w prawo-dół na panelu debugingu) aby wejść w wywołanie metody.

Znajdź i popraw błąd.

.. class:: tag

    Wykonaj

Uruchom klasę **EvaluateExpressions**. Jaki błąd wystąpił?

Ustaw breakpointa w metodzie **ProcessElementAtIndex**.

Otwórz okno ewaluacji wyrażeń i wpisz w niej **list.get(index)** .

Przechodź F9 (zielony trójkąt na panelu debug) do kolejnych wystąpień breakpointa i podglądaj wartości zmiennych. 

By sprawdzić jak naprawdę wyglądają ostatnie elementy listy wpisz w oknie evaluacji następujący kod:

.. class:: highlight

.. code:: java

    Collections.reverse(myList); 
    myList

Znajdź i popraw błąd.

.. class:: tag 

    Wykonaj
    
Uruchom klasę **ConditionalBreak**. Jaki błąd wystąpił?    

W linii 18, ustaw zwykły breakpoint, czy łatwo jest znaleźć błąd?

Ustaw w linii 18 warunkowy breakpoint tak, by zatrzymywał się przy spełnieniu warunku **!everythingIsOk**.

Jak widzisz breakpoint nie działa, przenieś go do linii 19.

Uruchom kod, co wywołało błąd?

Shelve ans Stash
==================

Czasami w czasie pracy jesteś zmuszony przełączyć się między różnymi zadaniami z niedokończonym kodem, a następnie wrócić do niego. IntelliJ IDEA zapewnia kilka sposobów wygodnej pracy nad kilkoma różnymi funkcjami bez utraty jej wyników:

    * utwórz nowy branch dla osobnego kodu

    * odłóż zmiany na półkę (ang. stash)
    
:badimportant:`Nie można odkładać na półkę niewersjonowanych plików, które nie zostały dodane do kontroli wersji.`

W widoku **Local Changes** na karcie **Git** pod kodem kliknij prawym przyciskiem myszy pliki lub listę zmian, które chcesz umieścić na półce, i wybierz **Shelve** z menu kontekstowego.

.. class:: center

.. image:: shelf.png

Czasami może być konieczne przywrócenie oryginalnej postaci gałęzi - HEAD, co zrobić by nie utracić w tym momencie wykonanych już zmian.

Stash działa podobnie jak shelve tylko zamiast obsługi poprzez GIT wykorzystuje IDE do przechowywania zmian.

Aby schować, zamiany lokalnie w IDE a nie w GIT wybierz **Git | Uncommited Changes | Stash Changes**, aby usunąć schowek, wybierz **Git | Uncommited Changes | Unstash Changes**.

Jeśli chcesz utworzyć nową gałąź na podstawie wybranego schowka zamiast stosować go do aktualnej gałęzi, wpisz nową nazwę w polu "As new branch".

JUnit
=======

JUnit to biblioteka służąca do pisania testów kodu. Testy mają na celu kontrolę jakości kodu, różnych ścieżek wywołań a także tego czy nowe zmiany nie wprowadzają błędów i zachowują starą funkcjonalność.

Proces budowania wersji przez Maven domyślnie uruchamia wszystkie testy znajdujące się w katalogu TEST podczas budowania pliku wykonywalnego.

Najpierw musimy dodać w pliku **pom.xml** zależność dla modułu testowego.


    | https://mvnrepository.com/artifact/junit/junit/4.12

W naszym branchu jest już stworzona klasa testowa jednak by dodać nową należałoby wykonać poniższe operacje: wejść do klasy **AdvanceMath** i wybrać :hold:`Ctrl + Shift + T` , kliknąć create new Test. Aby osiągnąć to samo inaczej można wybrać nazwę klasy i kliknąć :hold:`Alt + Enter` i wybrać create test.

Biblioteka JUnit korzysta z tzw. adnotacji. Przed każdą metodą która ma być uruchamiana jako test umieszczamy **@Test**.

Inną istotną adnotacją jest **@Before** która pozwala nam zdefiniować operacje które będą wykonywane przed uruchomieniem każdego testu.

Przykładowa klasa testująca:

.. class:: highlight

.. code:: java

    package second.junit;

    import com.sun.xml.internal.ws.policy.AssertionSet;
    import example.HelloWorld;
    import org.apache.log4j.Logger;
    import org.junit.Assert;
    import org.junit.Before;
    import org.junit.Test;

    import static org.junit.Assert.*;
    
    public class AdvanceMathTest {

        AdvanceMath math;
        final static Logger logger = Logger.getLogger(AdvanceMath.class);

        @Before
        public void setUp(){
            logger.info("Odpalam setUpa");
            math = new AdvanceMath();
        }
    
        @Test
        public void additionTest() {
            Integer a = math.addition(1,4);
            assertTrue(a==5);
        }
    
        @Test
        public void additionTestString() {
            long a = math.addition("1",4);
            Assert.assertEquals(5L, a);
        }
        
        
        @Test(expected = Exception.class)
        public void additionTestString2() {
            int a = math.addition("a1",4);
        }
        
    }

Test możemy uruchomić klikając na klasę i wybierając **run** lub przez zakładkę Maven -> Test. Testy są też dodawane automatycznie przy wykonaniu **Install** w zakładce Mavena.

Przykłady wykorzystania biblioteki JUnit : 

    | http://www.mkyong.com/tutorials/junit-tutorials/
    
Polecam spojrzeć na przykłady na temat testowania list i map.


AssertJ
--------

Lepszą biblioteką do pisania bardziej złożonych testów jest biblioteka AssertJ. 

W pliku **pom.xml** dodano zależność do biblioteki assertj.

    | https://mvnrepository.com/artifact/org.assertj/assertj-core/3.17.2
        
        
Zobacz klasę **Frodo.java** w katalogu test. Testy w niej są o wiele łatwiejsze do zrozumienia i definiowania w przypadku złożonych warunków.       
        
Dokumentacja:
    
    | https://assertj.github.io/doc/ 
    
Mock
--------

W przypadku gdy testujemy złożone systemy nasz kod może zależeć od zewnętrznych bibliotek, serwisów, albo danych. W przypadku testów jednostkowych oczekiwanie jest, że będziemy je wykonywać wielokrotnie a czas ich wykonywania będzie ograniczony.
W związku z tym nie chcemy testując naszego kodu czekać na połączenie, podbierać dużych plików danych, czy zależeć od dostępności zewnętrznych elementów. 

Jak więc testować kod, który takie zależności posiada? Z pomocą przychodzą nam tzw. Mocki, czyli klasy udające inne klasy, dla których możemy sami definiować odpowiedź klasy dla wywołania jej metod (sami tym samym dostarczając danych testowych dla naszych przypadków testowych).

Do tworzenia Mock-ów będziemy stosować bibliotekę **Mockito**. 

.. class:: tag

	Zadanie

Znajdź odpowiedni wpis w Maven repository i dodaj Mockito do projektu. 

Tworzenie mock’ów sprowadza się do wywołania metody metodę Mockito.mock(). 

.. class:: highlight

.. code:: java

	Class1 mock1 = Mockito.mock(Class1.class);
	Class2 mock2 = Mockito.mock(Class2.class);

	TestedClass testedClass = new TestedClass(mock1, mock2);

Wykorzystanie mock'ów. Dla zadanych parametrów funkcji z mockowanej klasy zwróc dany wynik jako odpowiedź. To w jaki sposób mock ma zareagować na wywołanie metody definiujemy używając **Mockito.when**.


.. class:: highlight

.. code:: java

    Mockito.when(Class1.method1(any(), any()).thenReturn("mockedOutput");

Do określenia zachowania mock’a możesz także użyć metod:

    | Mockito.doReturn - zwróć wartość
    | Mockito.doThrow - zwróć wyjątek
    | Mockito.doNothing - nic nie zwracaj
    | Mockito.doAnswer - gdy chcesz zwrócić wartość w oparciu np. o wejściowe parametry

Zobacz jak działa klasa **ProcessQuery**.

W naszym przypadku chcemy przetestować metodę **process** klasy **ProcessQuery**, metoda ta korzysta z klasy **HttpQueryClass**, która oryginalnie w kodzie wywołuje zapytanie HTTP o dane z zewnętrznego serwera HTTP. 
To jest klasa, którą chcielibyśmy zamockować, a dokładniej wywołanie metody **query** z niej.

.. class:: highlight

.. code:: java

    @Test
    public void mockTestExample() {
        when(httpQueryClass.query()).thenReturn("test");

        ProcessQuery processQuery = new ProcessQuery(httpQueryClass);

        String result = processQuery.process();
        assertThat(result).isEqualTo("TEST");
    }

.. class:: tag

    Zadanie 
    
Dodaj do metody query parametr i zmień definicję mock tak by działała z wywołaniem metody z parametrem, dla konkretnej wartości jak i dla dowolnej wartości. 

Extra
======

Good practices of code development
------------------------------------

* Make indents inside loops and if-statements 

.. class:: highlight

.. code:: java


    function foo() {
        if ($maybe) {
            do_it_now();
            again();
        } else {
            abort_mission();
        }
        finalize();
    }

* You can deal with curly brackets also like this:    
    
.. class:: highlight

.. code:: java
    
    function foo()
    {
        if ($maybe)
        {
            do_it_now();
            again();
        }
        else
        {
            abort_mission();
        }
        finalize();
    }
        
* Use blank lines consistently and as required. Blank lines may be used for separating  code lines or line groups semantically for readability.        

* Character count of a line should be limited for readability. 
        
* Name variables, procedures, functions in sensible way, start with small letter and introduce new word with capital letter

.. class:: highlight

.. code:: java

    studentsCounter;
    listIterator;
    averageOverLastWeek;
    findBestInClass();
    computeAverage();
    
* Name classes in sensible way, start with capital letter and introduce new word with capital letter    

.. class:: highlight

.. code:: java

    NightShift;
    FastCar;

* Name constant values with all capital letters, separate words with **_**

.. class:: highlight

.. code:: python

    DAYS_IN_THE_WEEK();
    NUMBER_OF_SHIFTS();
    
* Using space chars in code should also be consistent in whole application. Generally, situations below are suitable for using spaces:

* Between operators and operands: 

.. class:: highlight

.. code:: java

    a += b , c = 0; (a == b)

* Between statement keywords and brackets: 

.. class:: highlight

.. code:: java
    
    if (value) {, public class A { 

* After ';' char in loops: 

.. class:: highlight

.. code:: java

    for (int i = 0; i < length; i++) 

* Between type casters and operands: 

.. class:: highlight

.. code:: java

    (int) value , (String) value
    
