Laboratorium 7 - Thread Pool i Executory w Python
=================================================

Dodatkowe metody synchronizacji
===============================

Event
-----

Python udostępnia obiekt zdarzenia za pośrednictwem klasy
threading.Event.

Zdarzenie jest prostym prymitywem współbieżności, który umożliwia
komunikację między wątkami.

Obiekt Threading.Event opakowuje zmienną logiczną, która może być
„ustawiona” (prawda) lub „nieustawiona” (fałsz). Wątki współużytkujące
instancję zdarzenia mogą sprawdzać, czy zdarzenie jest ustawione,
ustawiać zdarzenie, kasować zdarzenie lub czekać na ustawienie
zdarzenia.

Threading.Event zapewnia łatwy sposób współdzielenia zmiennej logicznej
między wątkami, która może działać jako wyzwalacz akcji.

.. class:: highlight

.. code:: python

    import threading
    
    event = threading.Event()

Do ustawiania wartości true służy funkcja **set()** a do czekania na
wartość true służy funkcja **wait()**. Przykład:

.. class:: highlight

.. code:: python

    from time import sleep
    from random import random
    from threading import Thread
    from threading import Event
     
    def task(event, number):
        event.wait()
        value = random()
        sleep(value)
        print(f'Thread {number} got {value}')
        sleep(value)
      
    event = Event()
    
    for i in range(5):
        thread = Thread(target=task, args=(event, i))
        thread.start()
    
    print('Main thread blocking...')
    sleep(2)
    
    event.set()



.. parsed-literal::

    Main thread blocking...
    Thread 2 got 0.0905810157918302
    Thread 1 got 0.29938274432374745
    Thread 3 got 0.3827683096186707
    Thread 4 got 0.46137967365279275
    Thread 0 got 0.6282123321402183


Uzycie clear i is_set():

.. class:: highlight

.. code:: python

    from time import sleep
    from random import random
    from threading import Thread
    from threading import Event
     
    def task(event, number):
        event.wait()
        value = random()
        sleep(value)
        print(event.is_set())
        event.clear()
        print(event.is_set())
        print(f'Thread {number} got {value}')
        sleep(value)
        event.set()
      
    event = Event()
    
    for i in range(5):
        thread = Thread(target=task, args=(event, i))
        thread.start()
    
    print('Main thread blocking...')
    sleep(2)
    
    event.set()



.. parsed-literal::

    Main thread blocking...
    True
    False
    Thread 3 got 0.16971435437230664
    True
    False
    Thread 4 got 0.3947643335340075
    False
    False
    Thread 2 got 0.6601305334674352
    False
    False
    Thread 0 got 0.692246900797233
    False
    False
    Thread 1 got 0.7431957790318557


Bariera
-------

Bariera jest kolejną metodą synchronizacji procesów. Python udostępnia
barierę poprzez klasę threading.Barrier.

Instancja bariery musi najpierw zostać utworzona i skonfigurowana za
pomocą konstruktora, określając liczbę wątków, które muszą zarejestrować
się na blokadzie, zanim bariera zostanie zniesiona.

.. class:: highlight

.. code:: python

    import threading
    
    barrier = threading.Barrier(10)

Przykład użycia bariery, czekamy na zakończenie wszystkich wątków by
zakończyć główny wątek programu:

.. class:: highlight

.. code:: python

    import threading
    
    barrier = threading.Barrier(3)
    
    def run(id):
    	print(str(id) + "\n")
    	barrier.wait()
    		
    thread1 = threading.Thread(target=run, args=(100,))
    thread2 = threading.Thread(target=run, args=(101,))
    
    thread1.start()
    thread2.start()
    barrier.wait()
    
    print("Exit\n")



.. parsed-literal::

    100
    
    101
    
    Exit
    


Przykład użycia bariery z action. Funkcja z action wywoływana jest tylko
raz, gdy bariera jest zwalniania i jest wywoływana przed zwolnieniem
wątków do działania!

.. class:: highlight

.. code:: python

    import threading
    
    def printHi():
        print("Barrier reached")
    
    barrier = threading.Barrier(3, action=printHi)
    
    def run(id):
        barrier.wait()
        print(str(id) + "\n")
    	
    thread1 = threading.Thread(target=run, args=(100,))
    thread2 = threading.Thread(target=run, args=(101,))
    
    thread1.start()
    thread2.start()
    barrier.wait()
    
    print("Exit\n")



.. parsed-literal::

    Barrier reached
    Exit
    
    100
    
    101
    


Parametry obiektu bariery:

**abort:** Zmienia stan bariery na broken. Wszystkie wątki które
wywołają wait() na takiej barierze otrzymają wyjątek BrokenBarrierError

Składnia:

barrier.abort()

**reset:** Resetuje licznik bariery. Każdy oczekujący na niej wątek
otrzyma błąd BrokenBarrierError

Syntax:

barrier.reset()

**broken**: Wartość logiczna, która ma wartość True, jeśli bariera jest
w stanie zepsutym.

Składnia:

bariera.broken

**parties**: liczba wątków wymaganych do przejścia przez barierę.

Składnia:

barrier.parties

**n_waiting:** Liczba wątków oczekujących w danym momencie na barierze

Składnia:

barrier.n_waiting

Bariera może być wykorzystywana cyklicznie, wiele razy:

.. class:: highlight

.. code:: python

    import threading
    
    def printHi():
        print("Barrier reached")
    
    barrier = threading.Barrier(3, action=printHi)
    
    def run(id):
        print(barrier.n_waiting)
        barrier.wait()
        print(str(id) + "\n")
    	
    thread1 = threading.Thread(target=run, args=(100,))
    thread2 = threading.Thread(target=run, args=(101,))
    
    thread1.start()
    thread2.start()
    barrier.wait()
    
    print("Barrier left")
    print(barrier.broken)
    barrier.reset
    print(barrier.broken)
    
    thread3 = threading.Thread(target=run, args=(100,))
    thread4 = threading.Thread(target=run, args=(101,))
    thread3.start()
    thread4.start()
    barrier.wait()
    
    print("Exit\n")



.. parsed-literal::

    0
    1
    Barrier reached
    Barrier left
    False
    False
    101
    
    100
    
    0
    1
    Barrier reached
    Exit
    
    101
    
    100
    


Timer
-----

Ta klasa reprezentuje akcję, która powinna zostać uruchomiona dopiero po
upływie określonej ilości czasu — licznik czasu. Timer jest podklasą
Thread i jako taki działa również jako przykład tworzenia
niestandardowych wątków.

Timer czasu są uruchamiane, podobnie jak wątki, przez wywołanie ich
metody start(). Timer czasu można zatrzymać (zanim jego akcja się
rozpocznie) przez wywołanie metody cancel().

Uwaga! Przedział czasu, przez który licznik czasu będzie czekał przed
wykonaniem swojej akcji, może nie być dokładnie taki sam, jak przedział
czasu określony przez użytkownika.

.. class:: highlight

.. code:: python

    import threading as th  
    
    def pri():  
       print("Zombie is still alive \n")  
    
    S = th.Timer(2.0, pri)  
    S.start()  
    print("Exit Program\n")


.. parsed-literal::

    Exit Program
    
    Zombie is still alive 
    


Wykonanie funcji timer możemy przerwać wykonując cancel().

.. class:: highlight

.. code:: python

    import threading as th  
    
    def pri():  
       print("Zombie is still alive \n") 
    
    S = th.Timer(2.0, pri)  
    S.start()  
    print("PROGRAM TERMINATION\n")  
    S.cancel()


.. parsed-literal::

    PROGRAM TERMINATION
    


Pool
====

Pula procesów to wzorzec programistyczny służący do automatycznego
zarządzania pulą procesów roboczych.

Pula odpowiada za ustaloną liczbę procesów.

Python udostępnia pulę procesów za pośrednictwem klasy
multiprocessing.Pool.

.. class:: highlight

.. code:: python

    from multiprocessing import Pool
    
    work = [1,2,3]
    
    def multi(x):
        return x*x
    
    def pool_handler():
        p = Pool(2)
        print(p.map(multi, work))
    
    if __name__ == '__main__':
        pool_handler()



.. parsed-literal::

    [1, 4, 9]


Istnieją cztery główne etapy cyklu życia korzystania z klasy
multiprocessing.Pool, są to: tworzenie, przesyłanie zadań, oczekiwanie i
zamykanie.

::

   Utwórz: Utwórz pulę procesów, wywołując konstruktor multiprocessing.Pool().
    Prześlij: przesyłaj zadania synchronicznie lub asynchronicznie.
        2a. Przesyłaj zadania synchronicznie
        2b. Przesyłaj zadania asynchronicznie
    Czekaj: Poczekaj i uzyskaj wyniki po ukończeniu zadań (opcjonalnie).
        3a. Poczekaj na zakończenie obiektów Result
        3b. Poczekaj na obiekty AsyncResult dla Result
    Shutdown: Zamknij pulę procesów, wywołując close().
        4a. Zamknij automatycznie za pomocą Menedżera kontekstu

Tworzenie puli wątków:

Pulę procesów tworzymy, podając argumenty konstruktorowi klasy
multiprocessing.Pool.

Argumenty dla konstruktora są następujące:

::

    procesy: maksymalna liczba procesów roboczych do użycia w puli.
    inicjator: Funkcja wykonywana po utworzeniu każdego procesu roboczego.
    initargs: Argumenty funkcji inicjalizacji procesu roboczego.
    maxtasksperchild: Ogranicz maksymalną liczbę zadań wykonywanych przez każdy proces roboczy.
    context: Skonfiguruj kontekst przetwarzania wieloprocesowego, taki jak metoda uruchamiania procesu.
    

Domyślnie konstruktor klasy multiprocessing.Pool nie przyjmuje żadnych
argumentów.

pool = multiprocessing.Pool()

Spowoduje to utworzenie puli procesów, która będzie wykorzystywać liczbę
procesów roboczych odpowiadającą liczbie logicznych rdzeni procesora w
systemie.

pool = multiprocessing.Pool(2)

Definiuje ile procesów ma być tworzone w puli - w tym przypadku dwa.

Poniżej podany jest przykład konfiguracji inicjalizacji procesów w puli:

.. class:: highlight

.. code:: python

    from time import sleep
    import multiprocessing
    from multiprocessing import current_process
    from threading import current_thread
     
    def task():
        print(f'Wykonanie, process={current_process().name}, thread={current_thread().name}')
        sleep(1)
     
    def initialization():
        print(f'Inicjalizacja, process={current_process().name}, thread={current_thread().name}')
     
    if __name__ == '__main__':
        pool = multiprocessing.Pool(3, initializer=initialization)
        for _ in range(5):
            pool.apply(task)
            
        pool.close()
        pool.join()


.. parsed-literal::

    Inicjalizacja, process=ForkPoolWorker-7, thread=MainThreadInicjalizacja, process=ForkPoolWorker-8, thread=MainThread
    
    Inicjalizacja, process=ForkPoolWorker-9, thread=MainThreadWykonanie, process=ForkPoolWorker-7, thread=MainThread
    
    Wykonanie, process=ForkPoolWorker-8, thread=MainThread
    Wykonanie, process=ForkPoolWorker-9, thread=MainThread
    Wykonanie, process=ForkPoolWorker-7, thread=MainThread
    Wykonanie, process=ForkPoolWorker-8, thread=MainThread


Pool mozemy wywoływać też kontektowo z wkorzystanie słowa kluczowego
**with**:

.. class:: highlight

.. code:: python

    from time import sleep
    import multiprocessing
    from multiprocessing import current_process
    from threading import current_thread
     
    def task():
        print(f'Wykonanie, process={current_process().name}, thread={current_thread().name}')
        sleep(1)
     
    def initialization():
        print(f'Inicjalizacja, process={current_process().name}, thread={current_thread().name}')
     
    if __name__ == '__main__':
        with Pool(3, initializer=worker_init, initargs=(start,lock,)) as pool:
            for _ in range(2):
                pool.apply(task)
            pool.close()
            pool.join()


.. parsed-literal::

    Initializing worker with: 0
    Initializing worker with: 0
    Initializing worker with: 0
    Wykonanie, process=ForkPoolWorker-23, thread=MainThread
    Wykonanie, process=ForkPoolWorker-24, thread=MainThread


Zadania są wysyłane do puli, a procesy robocze są tworzone w razie
potrzeby do wykonania zadań.

Po utworzeniu procesów roboczych są one inicjowane, a następnie
rozpoczynają wykonywanie wydanych zadań.

Co ważne, każdy proces roboczy jest inicjowany tylko raz i tylko przed
rozpoczęciem wykonywania zadań w puli, nawet jeżeli nie będzie
wykorzystywany (jak widać powyżej).

Za pomocą inicjalizacji można definiować globalne zmienne dla danego
workera (wątku). Zauważ, że zmienne te nie są wspołdzielone między
wątkami:

.. class:: highlight

.. code:: python

    import multiprocessing
    from time import sleep
    from multiprocessing.pool import Pool
    
    def add():
        global lock
        lock.acquire()
        global counter
        counter += 1
        lock.release()
        print(f'Worker executing with: {counter} {lock}', flush=True)
        sleep(0.1)
    
    def worker_init(custom, mlock):
        global counter
        counter = custom
        global lock
        lock = mlock
        print(f'Initializing worker with: {counter}', flush=True)
    
    if __name__ == '__main__':
        start = 0
        lock = multiprocessing.Lock()
        with Pool(2, initializer=worker_init, initargs=(start,lock,)) as pool:
            for _ in range(10):
                pool.apply(add)
            pool.close()
            pool.join()


.. parsed-literal::

    Initializing worker with: 0
    Initializing worker with: 0
    Worker executing with: 1 <Lock(owner=None)>
    Worker executing with: 1 <Lock(owner=None)>
    Worker executing with: 2 <Lock(owner=None)>
    Worker executing with: 2 <Lock(owner=None)>
    Worker executing with: 3 <Lock(owner=None)>
    Worker executing with: 3 <Lock(owner=None)>
    Worker executing with: 4 <Lock(owner=None)>
    Worker executing with: 4 <Lock(owner=None)>
    Worker executing with: 5 <Lock(owner=None)>
    Worker executing with: 5 <Lock(owner=None)>


Przy zmianie na multiprocess.Value

.. class:: highlight

.. code:: python

    import multiprocessing
    from time import sleep
    from multiprocessing.pool import Pool
    
    def add():
        global lock
        lock.acquire()
        global counter
        counter.value += 1.0
        lock.release()
        print(f'Worker executing with: {counter.value} {lock}', flush=True)
        sleep(0.1)
    
    def worker_init(custom, mlock):
        global counter
        counter = custom
        global lock
        lock = mlock
        print(f'Initializing worker with: {counter.value}', flush=True)
    
    if __name__ == '__main__':
        start = multiprocessing.Value('d',0)
        lock = multiprocessing.Lock()
        with Pool(2, initializer=worker_init, initargs=(start,lock,)) as pool:
            for _ in range(10):
                pool.apply(add)
            pool.close()
            pool.join()


.. parsed-literal::

    Initializing worker with: 0.0
    Initializing worker with: 0.0
    Worker executing with: 1.0 <Lock(owner=None)>
    Worker executing with: 2.0 <Lock(owner=None)>
    Worker executing with: 3.0 <Lock(owner=None)>
    Worker executing with: 4.0 <Lock(owner=None)>
    Worker executing with: 5.0 <Lock(owner=None)>
    Worker executing with: 6.0 <Lock(owner=None)>
    Worker executing with: 7.0 <Lock(owner=None)>
    Worker executing with: 8.0 <Lock(owner=None)>
    Worker executing with: 9.0 <Lock(owner=None)>
    Worker executing with: 10.0 <Lock(owner=None)>


Jak już zauważyłeś zadania do wykonania przez Pool dodajemy przez
**apply()** lub **map()**

.. class:: highlight

.. code:: python

    from multiprocessing.pool import Pool
     
    def task(identifier):
        print(f'Task {identifier} executing {current_process()}')
        return identifier
     
    if __name__ == '__main__':
        with Pool(2) as pool:
            for result in pool.map(task, range(5)):
                print(f'Got result: {result}')


.. parsed-literal::

    Task 0 executing <ForkProcess name='ForkPoolWorker-40' parent=247962 started daemon>
    Task 2 executing <ForkProcess name='ForkPoolWorker-40' parent=247962 started daemon>
    Task 3 executing <ForkProcess name='ForkPoolWorker-40' parent=247962 started daemon>
    Task 4 executing <ForkProcess name='ForkPoolWorker-40' parent=247962 started daemon>
    Task 1 executing <ForkProcess name='ForkPoolWorker-41' parent=247962 started daemon>
    Got result: 0
    Got result: 1
    Got result: 2
    Got result: 3
    Got result: 4


Jeżeli możemy otrzymywać wyniki jeden za drugim możemy skorzystać z
imap(), dostaniemy wtedy wyniki szybciej zaraz po przetworzeniu jak i
zużyjemy mniej pamięci bo będą one dodawane do kolejki pojedynczo a nie
wszystkie na raz czekając w pamięci na wykonanie:

.. class:: highlight

.. code:: python

    from multiprocessing.pool import Pool
     
    def task(identifier):
        print(f'Task {identifier} executing {current_process()}')
        return identifier
     
    if __name__ == '__main__':
        with Pool(2) as pool:
            for result in pool.imap_unordered(task, range(5)):
                print(f'Got result: {result}')


.. parsed-literal::

    Task 0 executing <ForkProcess name='ForkPoolWorker-13' parent=249305 started daemon>Task 1 executing <ForkProcess name='ForkPoolWorker-14' parent=249305 started daemon>
    
    Task 2 executing <ForkProcess name='ForkPoolWorker-13' parent=249305 started daemon>
    Task 3 executing <ForkProcess name='ForkPoolWorker-13' parent=249305 started daemon>
    Task 4 executing <ForkProcess name='ForkPoolWorker-13' parent=249305 started daemon>
    Got result: 0
    Got result: 2
    Got result: 3
    Got result: 4
    Got result: 1


Zadania możemy też wykonywać asynchronicznie przy wykorzystaniu
**apply_async()**, **map_async()**. Do czekania na wynik obliczeń
wykorzystujemy metode **wait()** a pobranie wyniku wykonujemy za pomocą
**get()**.

.. class:: highlight

.. code:: python

    from multiprocessing.pool import Pool
    from multiprocessing import Process, current_process
    
    def task(identifier):
        print(f'Task {identifier} executing {current_process()}')
        return identifier
    
    if __name__ == '__main__':
        with Pool(2) as pool:
            result = pool.map_async(task, range(5))
            result.wait()
            print(f'Got result: {result.get()}')


.. parsed-literal::

    Task 0 executing <ForkProcess name='ForkPoolWorker-50' parent=247962 started daemon>Task 1 executing <ForkProcess name='ForkPoolWorker-51' parent=247962 started daemon>
    
    Task 2 executing <ForkProcess name='ForkPoolWorker-50' parent=247962 started daemon>
    Task 3 executing <ForkProcess name='ForkPoolWorker-51' parent=247962 started daemon>
    Task 4 executing <ForkProcess name='ForkPoolWorker-50' parent=247962 started daemon>
    Got result: [0, 1, 2, 3, 4]


W przypadku przetwarzania asynchronicznego możemy zdefiniować funkcję
**callback** która będzie wykonana po zakończeniu działania
przetwarzania map.

.. class:: highlight

.. code:: python

    from multiprocessing.pool import Pool
    from multiprocessing import Process, current_process
    
    def task(identifier):
        print(f'Task {identifier} executing {current_process()}')
        return identifier
    
    def custom_callback(result):
    	print(f'Got result: {result}')
    
    if __name__ == '__main__':
        with Pool(2) as pool:
            res = pool.map_async(task, range(3), callback=custom_callback)
            res.wait()


.. parsed-literal::

    Task 0 executing <ForkProcess name='ForkPoolWorker-11' parent=249305 started daemon>Task 1 executing <ForkProcess name='ForkPoolWorker-12' parent=249305 started daemon>
    Task 2 executing <ForkProcess name='ForkPoolWorker-11' parent=249305 started daemon>
    
    Got result: [0, 1, 2]


Poniżej podsumowano kluczowe różnice między tymi dwiema funkcjami:

::

    Funkcja map_async() nie blokuje, podczas gdy funkcja map() blokuje.
    Funkcja map_async() zwraca AsyncResult, podczas gdy funkcja map() zwraca iterowalną kolekcje zwracanych wartości z funkcji docelowej.
    Funkcja map_async() może wykonywać funkcje callback w przypadku zwracanych wartości i błędów, podczas gdy funkcja map() nie obsługuje funkcji callback.

Kolejki
-------

Klasa multiprocess.Queue jest prawie klonem klasy Queue.Queue. Kolejki
są bezpieczne dla wątków i procesów i mogą służyć jako medium wymiany
informacji między wątkami.

.. class:: highlight

.. code:: python

    from multiprocessing import Process, Queue
    
    def f(q):
        q.put([42, None, 'hello'])
    
    if __name__ == '__main__':
        q = Queue()
        p = Process(target=f, args=(q,))
        p.start()
        print(q.get())    # prints "[42, None, 'hello']"
        p.join()


.. parsed-literal::

    [42, None, 'hello']


Shared memory
-------------

SharedMemory ma stały rozmiar i przechowuje dane bajtowe.

Typy Pythona można konwertować na tablice bajtów i przechowywać w
SharedMemory oraz odczytywać jako tablice bajtów i konwertować z
powrotem na typy Pythona.

Umożliwia procesom odczytywanie i zapisywanie z tej samej pamięci, co
jest szybsze i wydajniejsze niż udostępnianie danych poprzez
przekazywanie komunikatów, na przykład przez multiprocessing.Queue [2].

.. class:: highlight

.. code:: python

    from multiprocessing.shared_memory import SharedMemory
    from multiprocessing import Process
     
    def task(shared_mem):
        shared_mem.buf[:24] = b'Hello from child process'
        shared_mem.close()
     
    if __name__ == '__main__':
        shared_mem = SharedMemory(create=True, size=100)
        process = Process(target=task, args=(shared_mem,))
        process.start()
        process.join()
    
        data = bytes(shared_mem.buf[:24]).decode()
        print(data)
        
        shared_mem.close()
        shared_mem.unlink()


.. parsed-literal::

    Hello from child process


Dodatkowe uwagi
---------------

Różnica między threadPool a processPool, czyli wykonania wielowątkowego
i wieloprocesorowego [1]. Porównaj jak poniższy kod zachowa się na
systemie Windows!

.. class:: highlight

.. code:: python

    from time import time
    import multiprocessing as mp
    from multiprocessing.pool import ThreadPool
    import numpy as np
    import pickle
    
    def main():
        arr = np.ones((1024, 1024, 1024), dtype=np.uint8)
        expected_sum = np.sum(arr)
    
        with ThreadPool(1) as threadpool:
            start = time()
            assert (
                threadpool.apply(np.sum, (arr,)) == expected_sum
            )
            print("Thread pool:", time() - start)
    
        with mp.get_context("spawn").Pool(1) as processpool:
            start = time()
            assert (
                processpool.apply(np.sum, (arr,)) == expected_sum
            )
            print("Process pool:", time() - start)
    
    if __name__ == "__main__":
        main()



.. parsed-literal::

    Thread pool: 0.7617292404174805
    Process pool: 4.805462121963501


NumPy zwalnia interpreter globalny GIL z wykonywania wielu swoich
operacji, co oznacza, że możesz używać wielu rdzeni procesora nawet z
wątkami [1]

.. class:: highlight

.. code:: python

    import numpy as np
    from time import time
    from multiprocessing.pool import ThreadPool
    
    arr = np.ones((1024, 1024, 1024))
    
    start = time()
    for i in range(10):
        arr.sum()
    print("Sequential:", time() - start)
    
    expected = arr.sum()
    start = time()
    with ThreadPool(4) as pool:
        result = pool.map(np.sum, [arr] * 10)
        assert result == [expected] * 10
    print("4 threads:", time() - start)



.. parsed-literal::

    Sequential: 5.484835386276245
    4 threads: 1.8242735862731934


Przykład Scikit-learn [3], jeden wątek:

.. class:: highlight

.. code:: python

    from sklearn.ensemble import RandomForestClassifier
    from sklearn import datasets
    import time
    
    X, y = datasets.make_classification(n_samples=10000, n_features=50, n_informative=20, n_classes=10)
    
    start = time.time()
    model = RandomForestClassifier(n_estimators=500)
    model.fit(X, y)
    print('Time:', time.time()-start)


.. parsed-literal::

    Time: 30.666493892669678


vs 4 wątki:

.. class:: highlight

.. code:: python

    from sklearn.ensemble import RandomForestClassifier
    from sklearn import datasets
    import time
    
    X, y = datasets.make_classification(n_samples=10000, n_features=50, n_informative=20, n_classes=10)
    
    start = time.time()
    model = RandomForestClassifier(n_estimators=500, n_jobs=4)
    model.fit(X, y)
    print('Time:', time.time()-start)



.. parsed-literal::

    Time: 8.18601655960083


Źródła:

[1] https://pythonspeed.com/articles/faster-multiprocessing-pickle/

[2] https://superfastpython.com/multiprocessing-sharedmemory/

[3]
https://blog.floydhub.com/multiprocessing-vs-threading-in-python-what-every-data-scientist-needs-to-know/

