Laboratorium 3 - Implementacja wątków w Python, Synchronizacja, Lock, Wait, Notify, Semafory
============================================================================================

Uwaga! w przypadku niepoprawnego zakończenia ktoregoś z kodów poniżej
musicie Państwo zrestartować Kernel Jupytera żeby móc uruchamiać
programy. Jest to spowodowane zawieszeniem się wątka przetwarzania,
który czeka na zakończenie wątku, który być może nigdy się nie skończy!

Inna opcja to uruchamianie programów w PyCharm gdzie zawsze możemy
wymusić zakończenie (zabicie) procesu.

Wątki
=====

Klasa **Thread** reprezentuje działanie uruchamiane w osobnym wątku.

Przetwarzanie można określić na dwa sposoby: przekazując funkcję do
konstruktora lub przesłaniając metodę run() w podklasie. Pierwszą metodę
poznaliśmy na pierwszych zajęciach. W przypadku podklasy, żadne inne
metody (z wyjątkiem konstruktora) nie powinny być nadpisywane w
podklasie. Innymi słowy, nadpisuj tylko metody **init\ ()** i **run()**:

.. class:: highlight

.. code:: python


    import threading
    import time
    
    class MyThread(threading.Thread):
    
        def run(self):
    	    time.sleep(1)
    	    return
    
    t = MyThread()
    t.start()
    print('Wątek t.is_alive()=', t.is_alive())
    t.join()
    print('Wątek t.is_alive()=', t.is_alive())



.. parsed-literal::

    Wątek t.is_alive()= True
    Wątek t.is_alive()= False


Konstruktor klasy Thread wygląda następująco:

   class threading.Thread(group=None, target=None, name=None, args=(),
   kwargs={}, \*, daemon=None)

Ten konstruktor powinien być zawsze wywoływany z argumentami słów
kluczowych.

Argumenty:

**group** powinna mieć wartość *None*; zarezerwowane dla przyszłych
rozszerzeń, gdy zostanie zaimplementowana klasa ThreadGroup.

**target** to wywoływalny obiekt (funkjca), który ma zostać wywołany
przez metodę run(). Domyślnie *None*, co oznacza, że wywołujemy po
prostu run.

**name** to nazwa wątku. Domyślnie unikalna nazwa jest tworzona w
postaci „Wątek-N”, gdzie N jest liczbą całkowitą.

**args** to lista lub krotka argumentów dla wywołania docelowego.
Domyślnie to ().

**kwargs** jest słownikiem argumentów słów kluczowych dla wywołania
docelowego. Domyślnie {}.

Uruchomienie wątków z parametrem poprzez utworzenie podklasy Thread
wygląda następująco:

.. class:: highlight

.. code:: python


    import threading
    import time
    import logging
    
    logging.basicConfig(level=logging.DEBUG,
                        format='(%(threadName)-9s) %(message)s',)
    
    class MyThread(threading.Thread):
    
        def __init__(self, group=None, target=None, name=None,
                     args=(), kwargs=None, verbose=None):
            super(MyThread,self).__init__(group=group, target=target, 
    			              name=name)
            self.args = args
            self.kwargs = kwargs
            return
    
        def run(self):
            print("Parametry args %s oraz kwargs %s" % (self.args, self.kwargs))
            return
    
    if __name__ == '__main__':
        for i in range(3):
            t = MyThread(args=(i,), kwargs={'a':1, 'b':2})
            t.start()


.. parsed-literal::

    Parametry args (0,) oraz kwargs {'a': 1, 'b': 2}
    Parametry args (1,) oraz kwargs {'a': 1, 'b': 2}
    Parametry args (2,) oraz kwargs {'a': 1, 'b': 2}


Metody modułu threading
-----------------------

Do działania na wątkach użyteczne mogą być funkcje z modułu threading
takie jak: **enumerate(), current_thread(), get_ident()** - opisane na
wykładzie.

Uwaga! Uruchom w PyCharm jeżeli w Jupiterze będą problemy, zwróć uwagę,
że w Jupiter jest wiele dodatkowych wątków oprócz uruchamianych przez
nas stąd stosujemy warunki żeby wyfiltrować tylko te tworzone przez nas:

.. class:: highlight

.. code:: python


    import threading
    import time
    import random
    
    def fun():
        t = threading.currentThread()
        r = random.randint(1,3)
        print('sleeping %s' % r)
        time.sleep(r)
        print('ending %s %s' % (threading.get_ident(), threading.current_thread().name))
        return
    
    if __name__ == '__main__':
        names = []
        for i in range(3):
            t = threading.Thread(target=fun)
            t.setDaemon(True)
            t.start()
            names+=t.getName()
    
        main_thread = threading.current_thread()
        print(main_thread)
        print(threading.enumerate())
        for t in threading.enumerate():
            if t is main_thread or t.getName() not in names:
                continue
            print('joining %s' % t.getName())
            t.join()


.. parsed-literal::

    sleeping 1
    sleeping 2
    sleeping 1
    <_MainThread(MainThread, started 140066318255936)>
    [<_MainThread(MainThread, started 140066318255936)>, <Thread(IOPub, started daemon 140066222970624)>, <Heartbeat(Heartbeat, started daemon 140066214577920)>, <Thread(Thread-3, started daemon 140065980274432)>, <Thread(Thread-4, started daemon 140065971881728)>, <ControlThread(Control, started daemon 140065963489024)>, <HistorySavingThread(IPythonHistorySavingThread, started 140065955096320)>, <ParentPollerUnix(Thread-2, started daemon 140065946703616)>, <Thread(Thread-39, started daemon 140065594406656)>, <Thread(Thread-41, started daemon 140065569228544)>, <Thread(Thread-42, started daemon 140065577621248)>, <Thread(Thread-43, started daemon 140065552443136)>, <Thread(Thread-44, started daemon 140065586013952)>]
    ending 140065594406656 Thread-39
    ending 140065569228544 Thread-41
    ending 140065577621248 Thread-42
    ending 140065586013952 Thread-44
    ending 140065552443136 Thread-43


Local data
----------

Podczas gdy niektóre zasoby muszą być blokowane, aby wiele wątków mogło
z nich korzystać jednocześnie, inne muszą być chronione, aby były ukryte
przed widokami wątków, które ich nie „posiadają”. Funkcja local() tworzy
obiekt zdolny do ukrywania wartości przed widokiem w oddzielnych
wątkach.

Thread-local data to dane, których wartości są związane z wątkiem. Aby
zarządzać danymi lokalnymi wątku, po prostu utwórz instancję local (lub
podklasę) i przechowuj na niej atrybuty:

.. class:: highlight

.. code:: python


    from time import sleep
    import threading
     
    def task(value):
        global data
        data.counter = 0
        for i in range(1,10):
            time.sleep(0.1)
            data.counter +=1
        print(f'Stored value: {data.counter}')
     
    data = threading.local()
    threading.Thread(target=task, args=(1,)).start()
    sleep(0.5)
    threading.Thread(target=task, args=(1,)).start()


.. parsed-literal::

    Stored value: 9
    Stored value: 9


Poniżej przykład dla którego otrzymamy nieprawidłowe wartości w
przypadku wykorzystania zwykłej zmiennej globalnej.

.. class:: highlight

.. code:: python


    from time import sleep
    import threading
     
    def task(value):
        global data
        data = 0
        for i in range(1,10):
            time.sleep(0.1)
            data +=1    
        print(f'Stored value: {data}')
     
    
    data = 0
    threading.Thread(target=task, args=(1,)).start()
    sleep(0.5)
    threading.Thread(target=task, args=(1,)).start()


.. parsed-literal::

    Stored value: 7
    Stored value: 13


Zamek (lock)
============

**Lock** - klasa implementująca obiekt blokady. Gdy jeden wątek uzyska
blokadę, kolejne próby jego uzyskania blokują wykonanie innych wątków,
aż do jego zwolnienia. Zamek służy do **synchronizacji** procesów, czyli
w najprostszym scenariuszu zabezpieczenia przed równoczesnym zapisem
przez wiele wątków wartości we wspólne miejsce w pamięci operacyjnej.
Samo zastosowanie może być jednak szerze i służyć do kontroli przepływu
i działania wątków poprzez ustawianie blokad synchronizujących kolejne
kroki naszego programu.

Metody:

   **acquire**\ (blocking=True, timeout=- 1)

Uzyskaj blokadę, blokującą lub nieblokującą.

Argument blocking może być stosowany do “fałszywego” blokowania
(blocking = False powoduje stworzenie tzw blokady nieblokującej) oznacza
niezablokowanie zamka dla innych operacji acquire z blocking = false,
ale w przypadku gdy inny wątek z blocking = true spróbuje go zablokować
otrzyma błąd.

W przypadku wywołania z argumentem limitu czasu zmiennoprzecinkowego
ustawionym na wartość dodatnią blokuje maksymalnie na liczbę sekund
określoną przez limit czasu i tak długo, jak blokada nie może zostać
nabyta. Argument limitu czasu -1 określa nieograniczone oczekiwanie.

Zwracana wartość to **True**, jeśli blokada została uzyskana pomyślnie,
**False**, jeśli nie.

   **release**\ ()

Zwolnij blokadę. Można to wywołać z dowolnego wątku, nie tylko wątku,
który uzyskał blokadę. Gdy zamek jest zablokowany, zresetuj go do stanu
odblokowanego i wróć. Jeśli jakiekolwiek inne wątki są zablokowane w
oczekiwaniu na odblokowanie blokady, pozwól dokładnie jednemu z nich
kontynuować.

Po wywołaniu na odblokowanej blokadzie zgłaszany jest **RuntimeError**.

   **locked**\ ()

Zwróć wartość **True**, jeśli blokada została uzyskana.

Poniżej przykład kodu symulującego błąd synchronizacji procesów:

.. class:: highlight

.. code:: python


    from threading import Thread, Lock
    from time import sleep
    
    counter = 0
    
    def increase(by):
        global counter
        local_counter = counter
        local_counter += by
        sleep(0.1)
        counter = local_counter
        print("counter= %s" % counter)
    
    # create threads
    t1 = Thread(target=increase, args=(1, ))
    t2 = Thread(target=increase, args=(2, ))
    
    # start the threads
    t1.start()
    t2.start()
    
    # wait for the threads to complete
    t1.join()
    t2.join()
    
    print("The final counter is %s" % counter)


.. parsed-literal::

    counter= 1
    counter= 2
    The final counter is 2


Ten sam kod z zabezpieczeniem dostępu poprzez **lock**. Teraz tylko
jeden koc może wykonywać zadania w synchronizawanej sekcji miedzy
**lock.acquire()** a **lock.release()**.

.. class:: highlight

.. code:: python


    from threading import Thread, Lock
    from time import sleep
    
    
    counter = 0
    
    
    def increase(by, lock):
        global counter
    
        lock.acquire()
    
        local_counter = counter
        local_counter += by
    
        sleep(0.1)
    
        counter = local_counter
        print("counter= %s" % counter)
    
        lock.release()
    
    
    lock = Lock()
    
    # create threads
    t1 = Thread(target=increase, args=(1, lock))
    t2 = Thread(target=increase, args=(2, lock))
    
    # start the threads
    t1.start()
    t2.start()
    
    
    # wait for the threads to complete
    t1.join()
    t2.join()
    
    print("The final counter is %s" % counter)


.. parsed-literal::

    counter= 1
    counter= 3
    The final counter is 3


Zamek RLock
===========

Domyślna blokada **Lock** nie rozpoznaje, który wątek aktualnie blokuje
zasób.

Jeśli dostęp do udostępnionego zasobu jest uzyskiwany przez dowolny
wątek, inne wątki próbujące uzyskać dostęp do udostępnionego zasobu
zostaną zablokowane, nawet jeśli jest to ten sam wątek, który zablokował
już wcześniej udostępniony zasób. Blokada ponownego wejścia (**RLlock**)
jest używana w takich sytuacjach, aby zapobiec niepożądanemu blokowaniu
dostępu do udostępnionego zasobu.

Jeśli udostępniony zasób znajduje się w **RLock**, można go bezpiecznie
wywołać ponownie. Dostęp do zasobu RLocked można uzyskać wielokrotnie za
pomocą różnych wątków, chociaż nadal działa poprawnie, gdy jest
wywoływany przez różne wątki. Spójrzmy na poniższy przykład, aby
zrozumieć użycie RLocks.

Poniższy program się nie zakończy (**Uwaga! uruchomienie go w Jupyter
zawiesi sesję interpretatora, więc postaraj uruchomić go w Pycharm**):

.. class:: highlight

.. code:: python


    // Uruchom mnie w PyCharm
    import threading
     
    counter = 0
     
    lock = threading.Lock()
    
    lock.acquire()
    counter = counter + 1
     
    lock.acquire()
    counter = counter +1
    lock.release()
    lock.release()
     
    print(counter)

W przypadku zamiany Lock na Rlock nie mamy już tego problemu:

.. class:: highlight

.. code:: python


    import threading
     
    counter = 0
     
    lock = threading.RLock()
    
    lock.acquire()
    counter = counter + 1
     
    lock.acquire()
    counter = counter +1
    lock.release()
    lock.release()
     
    print(counter)


.. parsed-literal::

    2


   Uwaga! Musimy wywołać release() raz dla każdego acquire() blokady
   obiektu RLock !

Podsumowanie
------------

+-----------------------------------------------+----------------------+
| Lock                                          | RLock                |
+===============================================+======================+
| Obiekt Lock nie może zostać ponownie          | Obiekt RLock może    |
| pozyskany przez żaden wątek, chyba że         | być pozyskiwany      |
| zostanie zwolniony przez wątek, który         | wiele razy przez     |
| uzyskuje dostęp do udostępnionego zasobu.     | dowolny wątek.       |
+-----------------------------------------------+----------------------+
| Obiekt Lock może zostać zwolniony przez       | Obiekt RLock może    |
| dowolny wątek.                                | zostać zwolniony     |
|                                               | tylko przez wątek,   |
|                                               | który go pozyskał.   |
+-----------------------------------------------+----------------------+
| Obiekt Lock nie może należeć do nikogo        | Obiekt RLock może    |
|                                               | należeć do wielu     |
|                                               | wątków.              |
+-----------------------------------------------+----------------------+
| Wykonywanie obiektu Lock jest szybsze.        | Wykonywanie obiektu  |
|                                               | RLock jest           |
|                                               | wolniejsze niż       |
|                                               | obiektu Lock         |
+-----------------------------------------------+----------------------+

Condition Objects
=================

Python udostępnia zmienną warunkową za pośrednictwem klasy
**multiprocessing.Condition**

Możemy utworzyć zmienną condition, która domyślnie utworzy nową blokadę
Rlock (klasa multiprocessing.RLock), która będzie używana do blokowania
dostępu do synchronizawanego kontekstu.

Aby proces mógł skorzystać z warunku, musi go uzyskać i zwolnić,
podobnie jak blokadę Lock. Można to osiągnąć ręcznie za pomocą funkcji
**acquire()** i **release()**:

.. class:: highlight

.. code:: python


    from multiprocessing import Condition
    
    condition = Condition()
    print("Start")
    condition.acquire()
    condition.release()
    print("Finish")


.. parsed-literal::

    Start
    Finish


Alternatywą dla bezpośredniego wywołania funkcji acquire() i release()
jest skorzystanie z menedżera kontekstu, który automatycznie wykona za
nas zajęcie/zwolnienie blokady. Funkcja **wait()** domyślnie czeka w
nieskończoność, aż inny wątek nie złosi **notify()**. Możemy również
przekazać argument „timeout”, który pozwoli procesowi zatrzymać
blokowanie po upływie określonego czasu w sekundach.

.. class:: highlight

.. code:: python


    from multiprocessing import Condition
    
    condition = Condition()
    with condition:
        print("Waiting")
        condition.wait(2)
        print("Koniec")


.. parsed-literal::

    Waiting
    Koniec


Możemy powiadomić pojedynczy oczekujący proces na blokadzie za pomocą
funkcji notify().

.. class:: highlight

.. code:: python


    from multiprocessing import Condition
    
    condition = Condition()
    with condition:
        print("Waiting")
        condition.notify()
        print("Koniec")


.. parsed-literal::

    Waiting
    Koniec


Możemy również powiadomić podzbiór procesów oczekujących, ustawiając
argument „n” na całkowitą liczbę procesów do powiadomienia, na przykład.
Na koniec możemy powiadomić wszystkie procesy oczekujące na warunek za
pomocą funkcji **notify_all()**.

.. class:: highlight

.. code:: python


    from multiprocessing import Condition
    
    condition = Condition()
    with condition:
        print("Waiting")
        condition.notify(n=3)
        condition.notify_all()
        print("Koniec")


.. parsed-literal::

    Waiting
    Koniec


Proces musi uzyskać warunek przed oczekiwaniem na niego lub
powiadomieniem oczekujących procesów. Niepowodzenie w uzyskaniu warunku
(blokada w warunku) przed wykonaniem tych działań spowoduje błąd
**RuntimeError**.

Przykład:

.. class:: highlight

.. code:: python


    from time import sleep
    import threading
    from multiprocessing import Condition
    
    def czekam(condition):
        with condition:
            print('Czekam na blokadę')
            condition.wait()
            print('Działam z blokadą równocześnie!')
        sleep(1)
        
    def dzialam(condition):
        sleep(1)
        print('Koniec procesowania')
        with condition:
            print('Zwalniam blokadę')
            condition.notify_all()
        sleep(1)
     
    # entry point
    if __name__ == '__main__':
     
        condition = Condition()
    
        print('Start')
        with condition:
            worker = threading.Thread(target=czekam, args=(condition,))
            worker2 = threading.Thread(target=dzialam, args=(condition,))
            worker.start()
            worker2.start()
            condition.wait()
    
        print('Koniec Main')


.. parsed-literal::

    Start
    Czekam na blokadę
    Koniec procesowania
    Zwalniam blokadę
    Działam z blokadą równocześnie!
    Koniec Main


Condition może nam posłużyć do implementacji przetwarzania w modelu
**producent-consument** z tzw. aktywnym czekaniem przez konsumenta:

.. class:: highlight

.. code:: python


    from time import sleep
    from random import random
    from threading import Thread
    from queue import Queue
    from multiprocessing import Condition
     
    def producer(queue, condition):
        print('Producent: Running')
        for i in range(5):
            with condition:
                value = random()
                queue.put(value)
                condition.notify()
            print('Wyslalem %s' % value)
            sleep(2)            
        print('Producer: Done')
     
    def consumer(queue, condition):
        with condition:
            print('Consument: Running')
            for i in range(5):
                print('Czekam')
                condition.wait()
                value = queue.get()
                sleep(0.2) 
                print('Dostałem %s' % value)
        print('Consument: Done')
     
    queue = Queue()
    condition = Condition()
    consumer = Thread(target=consumer, args=(queue,condition,))
    consumer.start()
    producer = Thread(target=producer, args=(queue,condition,))
    producer.start()
    producer.join()
    consumer.join()


.. parsed-literal::

    Consument: Running
    Czekam
    Producent: Running
    Wyslalem 0.7246806531871689
    Dostałem 0.7246806531871689
    Czekam
    Wyslalem 0.764394712675697
    Dostałem 0.764394712675697
    Czekam
    Wyslalem 0.9139622626543684
    Dostałem 0.9139622626543684
    Czekam
    Wyslalem 0.9383895972218189
    Dostałem 0.9383895972218189
    Czekam
    Wyslalem 0.14412814317848
    Dostałem 0.14412814317848
    Consument: Done
    Producer: Done


Semafory
========

Jest to jedna z najstarszych metod synchronizacji w historii
informatyki, wymyślony przez Edsgera W. Dijkstrę (używał nazw P() i V()
zamiast acquire() i release()). Najprościej mówiąc semafor to zamek
który pozwala na jednoczesny dostęp do synchronizowanej sekcji
zdefiniowanej w nim liczbie wątków.

Semafor zarządza wewnętrznym licznikiem, który jest zmniejszany przez
każde wywołanie funkcji **acquire()** i zwiększany przez każde wywołanie
funkcji **release()**. Licznik nigdy nie może spaść poniżej zera; kiedy
**acquire()** stwierdzi, że wartość licznika wynosi zero, blokuje się,
czekając, aż jakiś inny wątek wywoła **release()**.

.. class:: highlight

.. code:: python


    from threading import *
    import time
    
    obj = Semaphore(2)
    
    
    def display(name):
        for i in range(2):
            obj.acquire()
            print("Sem down %s" % name)
            print("Semafor value %s" % obj._value)
            time.sleep(2)
            obj.release()
            print("Sem up %s" % name)
            print("Semafor value %s" % obj._value)
    
    t1 = Thread(target=display, args=('Thread-1',))
    t2 = Thread(target=display, args=('Thread-2',))
    t3 = Thread(target=display, args=('Thread-3',))
    t4 = Thread(target=display, args=('Thread-4',))
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()



.. parsed-literal::

    Sem down Thread-1
    Semafor value 1
    Sem down Thread-2
    Semafor value 0
    Sem up Thread-1Sem down Thread-3
    Semafor value 0
    
    Semafor value 0
    Sem up Thread-2
    Semafor value 1
    Sem down Thread-2
    Semafor value 0
    Sem up Thread-3
    Semafor value 1
    Sem down Thread-3
    Semafor value 0
    Sem up Thread-2
    Semafor value 1
    Sem down Thread-1
    Semafor value 0
    Sem up Thread-3Sem up Thread-1
    Semafor value 2
    Sem down Thread-4
    Semafor value 1
    
    Semafor value 1
    Sem up Thread-4
    Semafor value 2
    Sem down Thread-4
    Semafor value 1
    Sem up Thread-4
    Semafor value 2


Event Object
============

Jest to prostszą wersją Condition (bez zabezpieczenia jednoczesnego
dostępu do zasobów poprzez acquire i release) i służy jako mechanizmów
komunikacji między wątkami: jeden wątek sygnalizuje zdarzenie, a inne na
nie czekają.

Obiekt zdarzenia zarządza wewnętrzną flagą, którą można ustawić na
wartość **true** za pomocą metody **set()** i zresetować na wartość
**false** za pomocą metody **clear()** . Metoda **wait()** blokuje
wykonanie, dopóki flaga nie będzie prawdziwa.

Możemy przepisać powyższy przykład tak by działał dla event objects:

.. class:: highlight

.. code:: python


    from time import sleep
    from random import random
    from threading import Thread
    from threading import Event
    from queue import Queue
     
    def producer(queue, condition):
        print('Producent: Running')
        for i in range(5):
            value = random()
            queue.put(value)
            print('Jak flaga? %s' % condition.is_set())
            condition.set()
            print('Wyslalem %s' % value)
            sleep(2)            
        print('Producer: Done')
     
    def consumer(queue, condition):
        print('Consument: Running')
        for i in range(5):
            print('Czekam')
            condition.wait()
            print('Jak flaga? %s' % condition.is_set())
            condition.clear()
            value = queue.get()
            sleep(0.2) 
            print('Dostałem %s' % value)
        print('Consument: Done')
     
    queue = Queue()
    condition = threading.Event()
    consumer = Thread(target=consumer, args=(queue,condition,))
    consumer.start()
    producer = Thread(target=producer, args=(queue,condition,))
    producer.start()
    producer.join()
    consumer.join()


.. parsed-literal::

    Consument: Running
    Czekam
    Producent: Running
    Jak flaga? False
    Wyslalem 0.01176724153986497
    Jak flaga? True
    Dostałem 0.01176724153986497
    Czekam
    Jak flaga? False
    Wyslalem 0.7551721515228753
    Jak flaga? True
    Dostałem 0.7551721515228753
    Czekam
    Jak flaga? False
    Wyslalem 0.8645864714182996
    Jak flaga? True
    Dostałem 0.8645864714182996
    Czekam
    Jak flaga? False
    Wyslalem 0.8301915595032113
    Jak flaga? True
    Dostałem 0.8301915595032113
    Czekam
    Jak flaga? False
    Wyslalem 0.5119799983830534
    Jak flaga? True
    Dostałem 0.5119799983830534
    Consument: Done
    Producer: Done


