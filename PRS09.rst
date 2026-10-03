Laboratoria 9 - Przetwarzanie strumieniowe na przykładzie Streamz
=================================================================

Przetwarzanie Strumieniowe
==========================

Przetwarzanie strumieniowe, znane również jako przetwarzanie w czasie
rzeczywistym, to technika przetwarzania danych, w której dane są
przetwarzane na bieżąco, w miarę ich napływania. Oznacza to, że dane są
analizowane w locie, w przeciwieństwie do tradycyjnego przetwarzania
wsadowego, w którym dane są zgromadzane i przetwarzane później.

Główną ideą przetwarzania strumieniowego jest ciągłe przetwarzanie
danych w czasie rzeczywistym, w sposób inkrementalny, gdy tylko dane są
dostępne. Strumienie danych mogą pochodzić z różnych źródeł, takich jak
czujniki, urządzenia IoT (Internet of Things), sieci społecznościowe,
transakcje finansowe itp.

Przetwarzanie strumieniowe wymaga specjalnych narzędzi i technologii,
które umożliwiają przetwarzanie danych na bieżąco. Istnieje wiele
frameworków i platform, takich jak **Apache Kafka, Apache Flink** czy
**Apache Storm**, które są popularne w dziedzinie przetwarzania
strumieniowego i pomagają w skutecznym zarządzaniu strumieniami danych.

Na tych zajęciach poznamy prostą bibliotekę przetwarzania strumieniowego
dla języka Python o nazwie **Streamz**.

Przykład przetwarzania strumieniowego : wyliczanie średniej
-----------------------------------------------------------

Weźmy przykład w którym mamy ciągły strumień plików CSV i chcemy
wydrukować średnią naszych danych w czasie. Za każdym razem, gdy pojawia
się nowy plik CSV, musimy ponownie obliczyć średnią całego zestawu
danych.

Jeśli jesteśmy sprytni, wystarczy że będziemy utrzymywać pośredni stan,
abyśmy mogli obliczyć tę średnią bez patrzenia wstecz na resztę naszych
danych historycznych. Możemy to osiągnąć, utrzymując bieżącą sumę i
licznik w następujący sposób:

.. class:: highlight

.. code:: python


    #Przykład jest tylko teoretycznym szkicem i oczywiście się nie uruchomi w Jupyter, gdyż nie definiujemy zbioru plików filenames
    
    total = 0
    count = 0
    
    for filename in filenames:  # filenames is an infinite iterator
        df = pd.read_csv(filename)
        total = total + df.sum()
        count = count + df.count()
        mean = total / count
        print(mean)


Streamz
=======

**Streamz** to biblioteka języka Python, która pomaga budować
przetwarzanie do zarządzania ciągłymi strumieniami danych. Jest prosty w
użyciu w prostych przypadkach, ale obsługuje również złożone
przetwarzania, które obejmują rozgałęzienia, łączenie, kontrolę
przepływu, sprzężenie zwrotne i tak dalej.

https://streamz.readthedocs.io/en/latest/

**Uwaga! Streamz nie jest obecnie zainstalowany na Jupiterze w wersji
online więc musisz korzystać z lokalnego Jupytera lub np z edytora
PyCharm!** Żeby zainstalować bibliotekę Streamz uruchom:

.. class:: highlight

.. code:: python


    pip install streamz  

Prosty przykład programu z wykorzystaniem Streamz:

.. class:: highlight

.. code:: python


    from streamz import Stream
    
    source = Stream()
    source.sink(print)

Aby zdefniować proces przetwarzania danych musimy utworzyć strumień
danych. Strumień ma swój początek i koniec. Końcem strumienia będzie
funkcja **sink()**, która aplikuje podaną w argumencie funkcję do
wszystkich elementów strumienia i kończy przetwarzanie.

Mając zdefiniowany strumień możemy dodawać dane do przetwarzania
korzystając z funkcji **emit()** dla tego strumienia.

.. class:: highlight

.. code:: python


    from streamz import Stream
    
    source = Stream()
    source.sink(print)
    
    source.emit(1)
    source.emit(2)
    source.emit(10)
    
.. parsed-literal::    

	1
	2
	10

Map
---

Najprostsza i znana nam już funkcja, która zamienia strumień danych
wejściowych mapując element wchodzący na element wychodzący i tym samym
zwracając zmieniony strumień danych.

.. class:: highlight

.. code:: python


    from streamz import Stream
    
    def toUpper(a):
        return a.upper()
    
    source = Stream()
    source.map(toUpper).sink(print)
    
    source.emit('a')
    source.emit('b')
    source.emit('c')
    source.emit('D')

.. parsed-literal::

	A
	B
	C
	D

Kiedy wywołujesz **Stream**, tworzysz strumień. Gdy wywołujesz dowolną
metodę w strumieniu, na przykład **Stream.map**, tworzysz również
strumień. Wszystkie operacje można ze sobą połączyć. Ponadto, jak
omówimy w części dotyczącej rozgałęzień, można rozdzielić wiele
strumieni z dowolnego punktu. Strumienie będą przekazywać swoje dane
wyjściowe do wszystkich dalszych strumieni, dzięki czemu każdy może
podłączyć się w dowolnym momencie i uzyskać pełny wgląd w to, co ten
strumień wytwarza.

Filter
------

Filter odrzuca elementy ze strumienia jeżeli nie spełniają warunku
logicznego zawartego w funkcji filtrującej.

.. class:: highlight

.. code:: python


    from numpy.core.defchararray import islower
    from streamz import Stream
    
    def upperIs(x):
        return islower(x)
    
    def toUpper(a):
        return a.upper()
    
    source = Stream()
    source.filter(upperIs).map(toUpper).sink(print)
    
    source.emit('a')
    source.emit('B')
    source.emit('c')
    source.emit('D')

.. parsed-literal::
	
	A
	C

Kiedy nasze obliczenia są **liniowe** i **proste**, do wykonania
obliczeń wystarczy pętla **for** oraz funkcje map, filter i sink. Jednak
gdy nasze obliczenia mają kilka rozgałęzień lub zbieżności strumieni,
być może z ograniczeniem szybkości lub buforowaniem między nimi, to
podejście stosujące pętlę **for** może stać się złożone i trudne do
zarządzania.

Accumulate
----------

Wykonuje to bieżące lub skumulowane redukcje, stosując funkcję do
poprzedniego stanu i nowego elementu. Funkcja powinna przyjąć dwa
argumenty, poprzedni stan skumulowany i następny element oraz powinna
zwrócić nowy stan skumulowany.

.. class:: highlight

.. code:: python


    from streamz import Stream
    
    def add(x, y):
        return x + y
    
    source = Stream()
    source.accumulate(add).sink(print)
    
    source.emit(1)
    source.emit(2)
    source.emit(3)
    source.emit(4)

.. parsed-literal::

	1
	3
	6
	10	

Powyższa funkcja akumulacji jest szczególnie prosta, stan, który
przechowujemy, i wartość, którą emitujemy, są takie same. W bardziej
złożonych sytuacjach możemy chcieć utrzymać inny stan niż emitujemy. Na
przykład policzmy, ile różnych elementów widzieliśmy do tej pory.

.. class:: highlight

.. code:: python


    from streamz import Stream
    
    def num_distinct(state, new):
        state.add(new)
        return state, len(state)
    
    source = Stream()
    source.accumulate(num_distinct, returns_state=True, start=set()).sink(print)
    
    source.emit('cat')
    source.emit('dog')
    source.emit('cat')
    source.emit('mouse')

.. parsed-literal::
	
	1
	2
	2
	3

Funkcja accumulate przyjmuje dwa argumenty, poprzedni stan skumulowany i
następny element oraz powinna zwrócić nowy stan skumulowany i wynik,

::

   - state = func(previous_state, new_value) (returns_state=False) 
   - state,result = func(previous_state, new_value) (returns_state=Prawda)

.. class:: highlight

.. code:: python


    from streamz import Stream
    
    source = Stream()
    source.accumulate(lambda acc, x: acc + 1, start=0).sink(print)
    for _ in range(5):
        source.emit(0)

.. parsed-literal::
	
	1
	2
	3
	4
	5

.. class:: highlight

.. code:: python


    from streamz import Stream
    
    source = Stream()
    source.accumulate(lambda acc, x: ((acc[0] + 1, x), (acc[0], x)),
                      start=(0, 0), returns_state=True)\
        .sink(print)
    for i in range(3):
        source.emit(0)

.. parsed-literal::
	
	(0, 0)
	(1, 0)
	(2, 0)

Flow control
============

Flatten
-------

Rozpakowuje strumienie list lub iteracji w strumień elementów.

.. class:: highlight

.. code:: python


    from streamz import Stream
    
    source = Stream()
    source.flatten().sink(print)
    for x in [[1, 2, 3], [4, 5], [6, 7, 7]]:
         source.emit(x)

.. parsed-literal::

	1
	2
	3
	4
	5
	6
	7
	7

Partition
---------

Podziel strumień na krotki o równym rozmiarze

Parametry

::

   n: rozmiar partycji
   limit czasu: int lub float, opcjonalnie. Liczba sekund, po których partycja zostanie wyemitowana, nawet jeśli jej rozmiar jest mniejszy niż n. Jeśli Brak (domyślnie), partycja zostanie wyemitowana tylko wtedy, gdy jej rozmiar osiągnie n.
   klucz: hashable lub callable, opcjonalny. Emituj elementy z tym samym kluczem razem jako oddzielną partycję. Jeśli klucz jest wywoływalny, partycja będzie identyfikowana przez klucz (x), w przeciwnym razie przez x[klucz]. Domyślnie Brak.

.. class:: highlight

.. code:: python


    from streamz import Stream
    from time import sleep
    
    source = Stream()
    source.partition(3).sink(print)
    for i in range(10):
         source.emit(i)
    
    source = Stream()
    source.partition(2, key=lambda x: x % 2).sink(print)
    for i in range(4):
         source.emit(i)
    
    source = Stream()
    source.partition(5, timeout=1).sink(print)
    for i in range(3):
        source.emit(i)
    sleep(1)

.. parsed-literal::
	
	(0, 1, 2)
	(3, 4, 5)
	(6, 7, 8)
	(0, 2)
	(1, 3)
	(0, 1, 2)

Union
-----

Łączy wiele strumieni w jeden

Każdy element z dowolnego strumienia upstream natychmiast wpłynie do
strumienia wyjściowego. Nie będą one łączone z elementami z innych
strumieni.

.. class:: highlight

.. code:: python


    from streamz import Stream
    
    source1 = Stream()
    stream = source1.map(lambda x: x-1)
    source = Stream()
    source.union(stream).map(lambda x : x+1).sink(print)
    
    for i in range(4):
         source.emit(i)
    print('Emituje do drugiego')
    for i in range(4):
         source1.emit(i)
            
.. parsed-literal::

	1
	2
	3
	4
	Emituje do drugiego
	0
	1
	2
	3


Wizualizacja potoku:

.. class:: center
	
	|a|
	
.. |a| image:: mystream2.png


Unique
------

Unikaj wysyłania powtarzających się elementów.

Powoduje to deduplikację strumienia, dzięki czemu przechodzą tylko nowe
elementy. Możesz kontrolować, jak duża część historii jest przechowywana
za pomocą parametru maxsize=. Na przykład ustawienie maxsize=1 pozwala
uniknąć wysyłania elementów, gdy jeden jest powtarzany zaraz po drugim.

.. class:: highlight

.. code:: python


    from streamz import Stream
    
    source = Stream()
    source.unique(maxsize=1).sink(print)
    for x in [1, 1, 2, 2, 2, 1, 3]:
         source.emit(x)

.. parsed-literal::

	1
	2
	1
	3

Sliding Window
--------------

Twórz nakładające się krotki o rozmiarze n.

.. class:: highlight

.. code:: python


    source = Stream()
    source.sliding_window(3, return_partial=False).sink(print)
    for i in range(8):
         source.emit(i)

.. parsed-literal::

	(0, 1, 2)
	(1, 2, 3)
	(2, 3, 4)
	(3, 4, 5)
	(4, 5, 6)
	(5, 6, 7)

Branching and Joining
=====================

Możesz rozgałęziać wiele strumieni z jednego strumienia. Elementy, które
trafią na wejście, przejdą do obu strumieni wyjściowych. **Uwaga: do
wizualizacji wykresu strumienia należy zainstalować graphviz i
networkx.**

.. class:: highlight

.. code:: python


    pip install graphviz
    pip install networkx

w katalogu w którym uruchomisz program wygeneruje się plik mystream.png
z wizualizacją przetwarzania danych

.. class:: highlight

.. code:: python


    from streamz import Stream
    
    def increment(x):
        return x + 1
    
    def decrement(x):
        return x - 1
    
    source = Stream()
    a = source.map(increment).sink(print)
    b = source.map(decrement).sink(print)
    b.visualize(rankdir='LR')
    
    source.emit(1)
    source.emit(2)

.. parsed-literal::

	2
	0
	3	
	1

Podobnie można również łączyć wiele strumieni razem z operacjami takimi
jak Zip, który emituje, gdy oba strumienie dostarczą nowy element, lub
Combine_latest, który emituje, gdy jeden ze strumieni dostarczy nowy
element.

.. class:: center
	
	|a2|
	
.. |a2| image:: mystream2.png

Podobnie można również łączyć wiele strumieni w jeden za pomocą operacji
takich jak Zip, który emituje, gdy oba strumienie dostarczą nowy
element, lub Combine_latest, który emituje, gdy jeden ze strumieni
dostarczy nowy element.

.. class:: highlight

.. code:: python


    from streamz import Stream
    
    def increment(x):
        return x + 1
    
    def decrement(x):
        return x - 1
    
    source = Stream()
    source2 = Stream()
    a = source.map(increment)
    b = source2.map(decrement)
    c = a.zip(b).map(sum).sink(print)
    
    source.emit(10)
    source2.emit(20)
    source.emit(30)
    source.visualize(rankdir='LR')

.. parsed-literal::

	30

.. class:: highlight

.. code:: python


    from streamz import Stream
    
    def increment(x):
        return x + 1
    
    def decrement(x):
        return x - 1
    
    source = Stream()
    source2 = Stream()
    a = source.map(increment)
    b = source2.map(decrement)
    c = a.combine_latest(b).map(sum).sink(print)
    
    source.emit(10)
    source2.emit(20)
    source.emit(30)
    source2.emit(30)
    source.visualize(rankdir='LR')

.. parsed-literal::
	
	30
	50
	60

.. class:: center
	
	|a3|
	
.. |a3| image:: mystream3.png

Processing Time and Back Pressure
=================================

Możesz kontrolować przepływ danych w swoim strumieniu w czasie. Na
przykład możesz chcieć zgrupować wszystkie elementy, które dotarły w
ostatniej chwili, lub spowolnić przepływ danych przez wrażliwe części
potoku, zwłaszcza gdy mogą one zapisywać do wolnych zasobów, takich jak
bazy danych.

Streamz pomaga wykonywać te akcje operacjami takimi jak **delay,
rate_limit i timed_window**.

Time_Window
-----------

Emituj krotkę zebranych wyników co interwał

Co zadany interval w sekundach emituje krotkę wszystkich dotychczasowych
wyników. Może to pomóc w grupowaniu danych wychodzących ze strumienia o
dużej objętości.

.. class:: highlight

.. code:: python


    from time import sleep
    
    from streamz import Stream
    
    source = Stream()
    a = source.timed_window(2).map(sum).sink(print)
    
    source.emit(10)
    source.emit(20)
    source.emit(30)
    source.emit(30)
    sleep(5)
    source.emit(1)
    source.emit(2)
    source.emit(3)
    source.emit(3)
    sleep(3)

.. parsed-literal::

	0
	90
	0
	9
	0

Źródła
------

::

   https://matthewrocklin.com/blog/work/2017/10/16/streaming-dataframes-1
   https://streamz.readthedocs.io/en/latest/

