========================
Pracowania Programowania
========================

--------------
JSON & XML 
--------------

*Współautor części materiału : Tomasz Ziętkiewicz*

.. class:: important 

    Uwaga! Kod do tych zajęć znajduje się na gałęzi **JsonAndXmlStart** w repozytorium https://github.com/WitMar/PRA2025 . Kod końcowy w gałęzi **JsonAndXmlEnd**.
    
Jeżeli nie widzisz odpowiednich gałęzi na GitHubie wykonaj **Ctr+T**, a jak to nie pomoże to wybierz z menu **Git->Fetch**.   
     

JSON
====
JSON (JavaScript Object Notation) http://www.json.org/ to lekki, tekstowy format wymiany danych.

Jest oparty na podzbiorze języka JavaScript.

Powszechnie wykorzystywany do przechowywania i przekazywania ustrukturyzowanych danych w postaci tekstowej.

Właściwości JSON-a:

- czytelny dla człowieka
- szeroko rozpowszechniony - biblioteki dla każdego języka (lista na http://www.json.org) 

Przykład JSON
~~~~~~~~~~~~~
.. code:: json
        
    {
        "artist": "Pink Floyd",
        "title": "Dark Side of the moon",
        "year": 1973,
        "tracks": [
            {
                "track#": 1,
                "title": "Speak to Me/Breathe",
                "length": "3:57",
                "music": ["Mason"]
            },
            {
                "track#": 2,
                "title": "On the run",
                "length": "3:50",
                "music": ["Waters", "Gilmour"]
            }
        ]
    }

Przykład z życia: `API rowerów miejskich <http://www.poznan.pl/mim/plan/map_service.html?mtype=pub_transport&co=stacje_rowerowe>`_


Składnia JSON
~~~~~~~~~~~~~

Dwie struktury danych:

- **object** (obiekt, słownik, mapa) 
  zbiór par klucz-wartość

.. code:: json

        {
        "title": "Dark Side of the Moon",
        "year": 1973,
        "tracks#": 9
        }

.. raw:: html

   <div style="text-align: center;">
       <img src="object.gif" alt="My Image">
   </div>


- **array** (tablica, lista)
   uporządkowany zbiór wartości

.. code:: json

    {
        "name":"John",
        "age":30,
        "cars":[ "Ford", "BMW", "Fiat" ]
    } 


.. raw:: html

   <div style="text-align: center;">
       <img src="array.gif" alt="My Image">
   </div>

Siedem typów wartości:

.. raw:: html

   <div style="text-align: center;">
       <img src="value.gif" alt="My Image">
   </div>


Komentarze
----------
Do pliku JSON nie możemy dodawać komentarzy

XML
===
XML (Extensible Markup Language) - język znaczników (markup language),
który podobnie jak JSON umożliwia serializację i wymianę strukturalnych danych 
w postaci tekstowej.


Składnia XML
~~~~~~~~~~~~

W dokumencie XML możemy wydzielić *zawartość* (*content*) i *znaczniki* (*markup*).

Znaczniki znajdują się między parami znaków "<" i ">" lub "&" i ";".

Treść dokumentu to wszystkie znaki, które nie są znacznikami.


Tagi
----
- tagi początku elementu:

.. code:: xml

   <album>

- tagi końca elementu:

.. code:: xml

   </album>

- tagi puste (bez zawartości):

.. code:: xml

    <album />

Element
-------
Element rozpoczna się tagiem początku, kończy tagiem końca elementu, albo jest pustym tagiem.

Pomiędzy tagami znajduje się zawartość elementu, którym może być albo zwykły tekst, albo zagnieżdżone elementy.

Tagi początkowy i pusty mogą zawierać atrybuty, czyli pary klucz-wartość.

Klucz podajemy jako text bez cudzysłowów, wartości zawsze w cudzysłowie.

.. code:: xml

        <track number="3" title="Time" length="3:57">
            Ticking away the moments that make up a dull day
            You fritter and waste the hours in an offhand way
            Kicking around on a piece of ground in your home town
            Waiting for someone or something to show you the way
        </track>


Komentarze
----------
Komentarze znajdują się między znacznikami "<!--" i "-->". 


Przykład XML
~~~~~~~~~~~~

.. code:: xml

    <?xml version="1.0" encoding="UTF-8"?> 
    <album title="Dark Side of the Moon" year="1973">
        <track number="1" title="Speak to Me/Breathe">
            Breathe, breathe in the air
            Don't be afraid to care
            Leave but don't leave me
            Look around and choose your own ground
            For long you live and high you fly
            Smiles you'll give and tears you'll cry
            And all you touch and all you see
            Is all your life will ever be
        </track>
        <track number="2" title="On the run" />
        <track number="3" title="Time" length="3:57">
            Ticking away the moments that make up a dull day
            You fritter and waste the hours in an offhand way
            Kicking around on a piece of ground in your home town
            Waiting for someone or something to show you the way
        </track>
    </album>




Życiowy przykład: `API rowerów miejskich, XML <https://nextbike.net/maps/nextbike-official.xml?city=192>`_


Serializacja / Deserializacja
=============================

Serializacja - proces polegający na przekształceniu struktur danych albo stanu obiektu do sekwencyjnej formy, która umożliwa zapisanie lub przesłanie tych danych i potencjalnie odtworzenie struktur danych lub obiektów w późniejszym czasie/przez inny proces/komputer (deserializację).

Na przykład, serializacja może polegać na zapisie do pliku w formacie JSON obiektów wygenerowanych przez nasz program, w celu późniejszego wczytania tych obiektów z powrotem do programu w celu kontynuowania obliczeń.

JSON i XML są przykładami formatów dobrze nadających się do serializacji danych w sposób czytelny dla człowieka.

Dane można również serializować dane w postaci binarnej, niezrozumiałej dla człowieka.

Jackson
~~~~~~~~~~~

`Jackson <https://github.com/FasterXML/jackson>`_ - zestaw narzędzi do przetwarzania danych dla Javy ("suite of data-processing tools for Java").

Głównym komponentem jest generator/parser JSON, pozwalający m.in. na deserializację/serializację do/z JSON z/do Javy.

Posiada liczne moduły dodające obsługę innych formatów danych, m.in. XML, YAML czy CSV.

Strona domowa projektu nie działa, ale projekt jest aktywnie rozwijany na `GitHub <https://github.com/FasterXML/jackson>`_.

`Zarchiwizowana wersja strony domowej <https://web.archive.org/web/20170801130759/http://wiki.fasterxml.com/JacksonHome>`_.

.. class:: tag

    Przygotowanie

Zobacz jak tworzeni są pracownicy w kodzie oraz jak są serializowani oraz co jest wynikiem programu.
Każdy z pracowników ma przypisany adres. 

Zobacz jak za pomocą om.fasterxml.jackson.databind.ObjectMapper zapisywany (serializowany) jest obiekt.

Przykłady:

    | https://www.mkyong.com/java/how-to-convert-java-object-to-from-json-jackson/

    | http://www.baeldung.com/jackson-object-mapper-tutorial

.. class:: tag

    Zadanie 0: Uruchom serializację

Uruchom kod, sprawdź jaka wersja biblioteki Jackson jest zainmportowana do pom.xml.

.. class:: important 

    Wskazówka: Odpowiedni wpis znajdzie w dokumentacji w `repozytorium maven <https://mvnrepository.com/artifact/com.fasterxml.jackson.core/jackson-databind>`_.

.. class:: tag

    Zadanie 1: Uruchom deserializację
    
Odkomentuj linijkę

.. code:: Java

    //deserializeDemo(jsonMapper, "json");    

Uruchom kod, zobacz jaki błąd widzisz. Dodaj do katalou resources plik employee.json i wklej do niego zawartość pliku result.json, czy błąd zniknął? Co zobaczysz jeżeli plik będzie zapisany w niepoprawnym miejscu?

.. class:: tag

    Zadanie 2: Deserializacja z JSON

Uruchom kod korzystając z debugera żeby sprawdzić jak zachowują się obiekty i jak zmienia się wynagrodzenie.

.. class:: tag

    Zadanie 3: Annotacje

W języku Java dla zapisu nazwy pól klasy przyjmuje się konwencję notacji `lowerCamelCase <https://pl.wikipedia.org/wiki/CamelCase>`_.

W JSON nie ma przyjętego standardu notacji (`dyskusja na StackOverflow <https://stackoverflow.com/questions/5543490/json-naming-convention>`_).

Domyślnie pola w JSONie wygenerowanym przez Jackson/Gson mają **takie same nazwy jak pola w klasie**, którą serializujemy.

Dodaj do modelowanych klas annotacje zmieniającą nazwę pola w JSON z salary na "wynagrodzenie" oraz adnotacje do ignorowania pola "pesel" przy serializacji.

.. class:: important 

    Wskazówka: Skorzystaj z `dokumentacji <https://github.com/FasterXML/jackson-databind/#annotations-changing-property-names>`_.
    

Zobacz w jakiej kolejności serializowane są pola oraz odpowiedz na pytanie dlaczego wystąpił błąd deserializacji? Napraw błąd. Czy Pesel wczytuje się przy deserializacji?


.. class:: tag

    Zadanie 4: Deserializacja typów generycznych


Spróbuj serializować listę pracowników (w postaci ArrayList) zobacz jak wygląda plik json zawierający listę kilku pracowników.
Wczytaj tę listę do kolekcji ArrayList<Employee>.

Następnie spróbuj zdeserializować otrzymany plik wynikowy.

.. class:: important 

    Wskazówka: Skorzystaj z `3 minute tutorial <https://github.com/FasterXML/jackson-databind/#3-minute-tutorial-generic-collections-tree-model>`_.

Jackson XML
-------------
Jackson posiada `moduł <https://github.com/FasterXML/jackson-dataformat-xml>`_
rozszerzający go o obsługę formatu XML.
Aby użyć XML zamiast JSON wystarczy zmienić "ObjectMapper" na XmlMapper":

.. code:: Java

    ObjectMapper xmlMapper = new XmlMapper();

Więcej szczegółów:     
     
    http://www.baeldung.com/jackson-xml-serialization-and-deserialization

.. class:: tag

    Zadanie 5: XML
    
Korzystając z istniejącej klasy JacksonSerialization zmodyfikuj ją, albo stwórz nową klasę tak, żeby umożliwić serializację / deserializację do/z formatu XML.
Dodaj do katalogu main/resources pliki xml odpowiadające istniejącym już plikom json.

.. class:: important 
    
    Wskazówka: Nie musisz tworzyć zawartości plików xml samodzielnie, możesz wygenerować je za pomocą odpowiednich metod.

.. class:: important  

    Wskazówka: Pamiętaj żeby dodać bibliotekę do pom.xml. Odpowiedni wpis znajdziesz w `repozytorium GitHub modułu XML <https://github.com/FasterXML/jackson-dataformat-xml#maven-dependency>`_. Skorzystaj z wersji **2.17.1**.

.. class:: tag

    Zadanie 6: Joda Time

Dodaj do klasy Employee pole 

.. code:: java

    DateTime birthDate 
    
zawierające datę urodzenia pracownika. 

.. class:: important 

    Wskazówka: Możesz potrzebować modułu `jackson-datatype-joda <https://github.com/FasterXML/jackson-datatype-joda>`_.
    

Spróbuj dokonać serializacji a następnie deserializacji obiektu tak zmodyfikowanej klasy.   

Żeby wszystko zadziałało potrzebujesz zarejestrować w mapperze moduł Joda. 
    
    | https://stackoverflow.com/questions/29523169/register-jodamodule-in-jax-rs-application

Zobacz jak teraz serializuje się plik.

StackOverflow powie Ci, że brakuje Ci adnotacji względem tego jak formatowana powinna być data. 
Dodaj nad polem daty adnotacje 

.. code:: java

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd HH:mm:ss.SSSZ")

.. class:: tag    
    
    Zadanie 7: rekurencyjne odwołania

Zauważ, że w JSONie wypisywane są całe obiekty wraz z zależnościami. Co stałoby się gdyby pracownik X miał podwładnego Y którego podwładnym byłby znów X? Otrzymalibyśmy nieskończoną rekurencję i błąd serializacji. Żeby tego uniknąć możemy zastosować adnotację:

Odkomentuj linie w ModeObjectCreator.java 

 .. code:: java
 
     emp2.getManagers().add(emp);

i dodaj:

 .. code:: java

    @JsonIdentityInfo(generator=ObjectIdGenerators.IntSequenceGenerator.class,
            property="refId", scope=Employee.class)
    public class Employee { ... }

Która spowoduje, że obiekty wypisywane będą tylko raz, a przy wielokrotnych odwołaniach zostanie zastosowane Id jako referencja.

Więcej na ten temat:

http://www.baeldung.com/jackson-bidirectional-relationships-and-infinite-recursion


Generowanie klas z JSON
=========================

Istnieje wiele generatorów online zamieniających JSON na klasy modelu w Java.

	| https://json2csharp.com/code-converters/json-to-pojo
	
	| https://www.site24x7.com/tools/json-to-java.html
