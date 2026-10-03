Laboratorium 4 - Multiprocessing. Anomalie związane z przetwarzaniem równoległym, zagłodzenie, race condition, zakleszczenie
============================================================================================================================

multiprocessing
---------------

**multiprocessing** to pakiet obsługujący tworzenie procesów przy użyciu
interfejsu API podobnie do modułu thread.

Pakiet multiprocessing oferuje zarówno lokalną, jak i zdalną
współbieżność, skutecznie omijając globalną blokadę interpretera,
używając podprocesów zamiast wątków. Dzięki temu moduł wieloprocesorowy
pozwala programiście na pełne wykorzystanie wielu procesorów na danej
maszynie. Działa zarówno na systemie Unix, jak i Windows.

W przetwarzaniu multiprocessing procesy są tworzone przez utworzenie
obiektu **Process**, a następnie wywołanie jego metody **start()**.

.. class:: highlight

.. code:: python

    from time import sleep
    from multiprocessing import Process
     
    def task():
        sleep(1)
        print('This is from another process')
     
    if __name__ == '__main__':
        process = Process(target=task)
        process.start()
        print('Waiting for the process...')
        process.join()


.. parsed-literal::

    Waiting for the process...
    This is from another process


.. class:: highlight

.. code:: python

    from multiprocessing import Process
    
    def f(name):
        print('Cześć', name)
    
    if __name__ == '__main__':
        p = Process(target=f, args=('Marcin',))
        p.start()
        p.join()


.. parsed-literal::

    Cześć Marcin


Podobnie możemy tworzyć proces jako podklase klasy Process:

.. class:: highlight

.. code:: python

    from time import sleep
    from multiprocessing import Process
     
    class CustomProcess(Process):
        def run(self):
            sleep(1)
            print('This is coming from another process')
     
    if __name__ == '__main__':
        process = CustomProcess()
        process.start()
        print('Waiting for the process to finish')
        process.join()


.. parsed-literal::

    Waiting for the process to finish
    This is coming from another process


Jak widać w poniższym przykładzie wykonywany kod uruchamia nowy process
w systemie.

.. class:: highlight

.. code:: python

    from multiprocessing import Process
    import os
    
    def info(title):
        print(title)
        print('module name:', __name__)
        print('parent process:', os.getppid())
        print('process id:', os.getpid())
    
    def f(name):
        info('function f')
        print('Cześć', name)
    
    if __name__ == '__main__':
        info('main funkcja')
        p = Process(target=f, args=('Marcin',))
        p.start()
        p.join()


.. parsed-literal::

    main funkcja
    module name: __main__
    parent process: 58469
    process id: 59795
    function f
    module name: __main__
    parent process: 59795
    process id: 60127
    Cześć Marcin


Wykorzystanie Lock w multiprocessing

.. class:: highlight

.. code:: python

    from multiprocessing import Process, Lock
    
    def f(l, i):
        l.acquire()
        try:
            print('hello world', i)
        finally:
            l.release()
    
    if __name__ == '__main__':
        lock = Lock()
    
        for num in range(10):
            Process(target=f, args=(lock, num)).start()


.. parsed-literal::

    hello world 0
    hello world 1
    hello world 2
    hello world 3
    hello world 4
    hello world 5
    hello world 6
    hello world 7
    hello world 8
    hello world 9


Dane między procesami być przechowywane na mapie pamięci współdzielone
przy użyciu **Value** lub **Array**.

Zmienne współdzielone oznaczają, że zmiany dokonane w jednym procesie są
zawsze propagowane i udostępniane innym procesom. Wystąpienie
multiprocessing.Value można zdefiniować w konstruktorze klasy jako
zmienną. Konstruktor klasy multiprocessing.Value wymaga od nas
określenia typu danych oraz wartości początkowej. Definicje
konstruktorów obiektów:

   multiprocessing.Array(typecode_or_type, size_or_initializer, \*,
   lock=True)

..

   multiprocessing.Value(typecode_or_type, \*args, lock=True)

Typy z moduly ctypes: ‘i’ - int, ‘d’ - double, c_char - char, c_bool -
bool, c_wchar_p - String.

Jeśli blokada ma wartość True (wartość domyślna), tworzony jest nowy
obiekt blokady w celu synchronizacji dostępu do wartości. Jeśli lock
jest obiektem Lock lub RLock, zostanie użyty do synchronizacji dostępu
do wartości. Jeśli blokada ma wartość False, dostęp do zwróconego
obiektu nie będzie automatycznie chroniony blokadą, więc niekoniecznie
będzie „bezpieczny dla procesu”.

Na przykład:

.. class:: highlight

.. code:: python

    from multiprocessing import Process, Value, Array
    from ctypes import Structure, c_bool
    
    def f(n, a, m):
        n.value = 3.1415927
        m.value = True
        for i in range(len(a)):
            a[i] = -a[i]
    
    if __name__ == '__main__':
        num = Value('d', 0.0)
        bools = Value(c_bool, False)
        arr = Array('i', range(10))
    
        p = Process(target=f, args=(num, arr, bools))
        p.start()
        p.join()
    
        print(num.value)
        print(bools.value)
        print(arr[:])  
    



.. parsed-literal::

    3.1415927
    True
    [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]


Tworzenie nowych procesów czy wątków? Jak zobaczymy niżej jako że
Jupyter działa na Linuxie uruchamiane są nowe wątki poprzez fork.
Uruchom program u siebie na systemie windows.

.. class:: highlight

.. code:: python

    import multiprocessing
    
    methods = multiprocessing.get_all_start_methods()
    print(methods)
    method = multiprocessing.get_start_method()
    print(method)


.. parsed-literal::

    ['fork', 'spawn', 'forkserver']
    fork


Aby sprawdzić czy warto wykorzystywać ten moduł sprawdź liczbę rdzeni na
komputerze z któreo korzystasz (odpal lokalnie!)

.. class:: highlight

.. code:: python

    import multiprocessing
    
    print("Number of cpu : ", multiprocessing.cpu_count())


.. parsed-literal::

    Number of cpu :  6


Race condition
--------------

Przykład:

.. class:: highlight

.. code:: python

    from threading import Thread
     
    def adder(amount, repeats):
        global value
        for _ in range(repeats):
            value += amount*2
     
    def subtractor(amount, repeats):
        global value
        for _ in range(repeats):
            value -= amount*2
     
    value = 0
    adder_thread = Thread(target=adder, args=(10, 500000))
    adder_thread.start()
    subtractor_thread = Thread(target=subtractor, args=(10, 500000))
    subtractor_thread.start()
    print('Waiting for threads to finish...')
    adder_thread.join()
    subtractor_thread.join()
    
    print(f'Value: {value}')


.. parsed-literal::

    Waiting for threads to finish...
    Value: 4731260


Zakleszczenie
-------------

Przykład watki czekają na siebie (złe użycie join()):

.. class:: highlight

.. code:: python

    from threading import current_thread
    from threading import Thread
     
    def task(other):
        print(f'[{current_thread().name}] waiting on [{other.name}]...')
        other.join()
     
    main_thread = current_thread()
    new_thread = Thread(target=task, args=(main_thread,))
    new_thread.start()
    task(new_thread)

Przykład złe blokowanie locków:

.. class:: highlight

.. code:: python

    from time import sleep
    from threading import Thread
    from threading import Lock
     
    def task(number, lock1, lock2):
        print(f'Thread {number} acquiring lock 1...')
        with lock1:
            sleep(1)
            print(f'Thread {number} acquiring lock 2...')
            with lock2:
                pass
     
    lock1 = Lock()
    lock2 = Lock()
    thread1 = Thread(target=task, args=(1, lock1, lock2))
    thread2 = Thread(target=task, args=(2, lock2, lock1))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

Zagłodzenie
-----------

.. class:: highlight

.. code:: python

    from time import sleep
    from threading import Thread
    from threading import Lock
     
    # task
    def task(lock, identifier):
        with lock:
            for i in range(5):
                print(f'Thread {identifier} working')
                sleep(1)
     
    lock = Lock()
    threads = [Thread(target=task, args=(lock,i)) for i in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


.. parsed-literal::

    Thread 0 working
    Thread 0 working
    Thread 0 working
    Thread 0 working
    Thread 0 working
    Thread 1 working
    Thread 1 working
    Thread 1 working
    Thread 1 working
    Thread 1 working


Fix nr 1

.. class:: highlight

.. code:: python

    from time import sleep
    from threading import Thread
    from threading import Lock
     
    def task(lock, identifier):
        for i in range(5):
            lock.acquire()
            print(f'Thread {identifier} working')
            sleep(1)
            lock.release()
     
    lock = Lock()
    threads = [Thread(target=task, args=(lock,i)) for i in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


.. parsed-literal::

    Thread 0 working
    Thread 0 working
    Thread 0 working
    Thread 0 working
    Thread 0 working
    Thread 1 working
    Thread 1 working
    Thread 1 working
    Thread 1 working
    Thread 1 working


Nadal nie jest sprawiedliwie, fix nr 2:

.. class:: highlight

.. code:: python

    from time import sleep
    from threading import Thread
    from threading import Semaphore
     
    def task(lock, identifier):
        for i in range(5):
            with lock:
                print(f'Thread {identifier} working')
                sleep(1)
     
    lock = Semaphore(1)
    threads = [Thread(target=task, args=(lock,i)) for i in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


.. parsed-literal::

    Thread 0 working
    Thread 0 working
    Thread 0 working
    Thread 0 working
    Thread 0 working
    Thread 1 working
    Thread 1 working
    Thread 1 working
    Thread 1 working
    Thread 1 working


Żeby wymusić przełączenie najlepiej użyć sleep()

.. class:: highlight

.. code:: python

    from time import sleep
    from threading import Thread
    from threading import Semaphore
     
    def task(lock, identifier):
        for i in range(5):
            sleep(0.001)
            with lock:
                print(f'Thread {identifier} working')
                sleep(1)
     
    lock = Semaphore(1)
    threads = [Thread(target=task, args=(lock,i)) for i in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


.. parsed-literal::

    Thread 0 working
    Thread 1 working
    Thread 0 working
    Thread 1 working
    Thread 0 working
    Thread 1 working
    Thread 0 working
    Thread 1 working
    Thread 0 working
    Thread 1 working


Livelock
--------

.. class:: highlight

.. code:: python

    from time import sleep
    from threading import Thread
    from threading import Lock
     
    def task(number, lock1, lock2):
        for i in range(10):
            with lock1:
                sleep(0.1)
                if lock2.locked():
                    print(f'Task {number} cannot get the second lock, giving up...')
                else:
                    with lock2:
                        print(f'Task {number} made it, all done.')
                        break
     
    lock1 = Lock()
    lock2 = Lock()
    thread1 = Thread(target=task, args=(0, lock1, lock2))
    thread2 = Thread(target=task, args=(1, lock2, lock1))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


.. parsed-literal::

    Task 0 cannot get the second lock, giving up...
    Task 1 cannot get the second lock, giving up...
    Task 0 cannot get the second lock, giving up...
    Task 1 cannot get the second lock, giving up...
    Task 0 cannot get the second lock, giving up...
    Task 1 cannot get the second lock, giving up...
    Task 0 cannot get the second lock, giving up...
    Task 1 cannot get the second lock, giving up...
    Task 0 cannot get the second lock, giving up...
    Task 1 cannot get the second lock, giving up...
    Task 0 cannot get the second lock, giving up...
    Task 1 cannot get the second lock, giving up...
    Task 0 cannot get the second lock, giving up...
    Task 1 cannot get the second lock, giving up...
    Task 0 cannot get the second lock, giving up...
    Task 1 cannot get the second lock, giving up...
    Task 0 cannot get the second lock, giving up...
    Task 1 cannot get the second lock, giving up...
    Task 0 cannot get the second lock, giving up...
    Task 1 made it, all done.


Zadanie
-------

Przeanalizuj poniższy kod sklepu sprzedającego trzy elementy następnie
wykonaj zadania na moodle (debbuger z Pycharm może ci pomóc w analizie).

.. class:: highlight

.. code:: python

    from enum import Enum
    import random
    from threading import Thread, Lock, current_thread
    
    class Items(Enum):
        GARNEK = 0
        SZKLANKA = 1
        TALERZ = 2
    
    class Shop:
        listLock = []
        warehouse = {}
    
        def __init__(self):
            self.listLock.append(Lock())
            self.listLock.append(Lock())
            self.listLock.append(Lock())
            self.warehouse[Items.GARNEK.name] = 10000
            self.warehouse[Items.TALERZ.name] = 200
            self.warehouse[Items.SZKLANKA.name] = 800
    
        def purchase(self, item, wynik):
            #print("Kupuje %s %s" % (item, current_thread().name))
            stockSize = self.warehouse[item.name]
            if (stockSize > 0):
                #print("Zakup zaakceptowany - Na stanie %s %s %s" % (item.name, stockSize, current_thread().name))
                self.warehouse[item.name] = self.warehouse[item.name] - 1
            else:
                #print("Zakup odrzucony - nie ma dostępnych więcej elementów %s %s" % (item.name, current_thread().name))
                wynik[item.name] = wynik[item.name] + 1
    
    def shopper(shop, shoppingList, wynik):
        for el in shoppingList:
            shop.purchase(el, wynik)
    
    if __name__ == '__main__':
        shop = Shop()
        shoppingList_1 = []
        shoppingList_2 = []
        shoppingList_3 = []
        shoppingList_4 = []
        ile = {Items.GARNEK.name:  10000, Items.TALERZ.name:  200, Items.SZKLANKA.name: 800}
        wynik = {Items.GARNEK.name:  0, Items.TALERZ.name:  0, Items.SZKLANKA.name: 0}
        for _ in range(0, 50000):
            r = random.randrange(0, 3)
            item = list(Items)[r]
            shoppingList_1.append(item)
            ile[item.name] = ile[item.name] - 1
    
        for _ in range(0, 50000):
            r = random.randrange(0, 3)
            item = list(Items)[r]
            shoppingList_2.append(item)
            ile[item.name] = ile[item.name] - 1
    
        for _ in range(0, 50000):
            r = random.randrange(0, 3)
            item = list(Items)[r]
            shoppingList_3.append(item)
            ile[item.name] = ile[item.name] - 1
    
        for _ in range(0, 5000):
            r = random.randrange(0, 3)
            item = list(Items)[r]
            shoppingList_4.append(item)
            ile[item.name] = ile[item.name] - 1
    
        thread1 = Thread(target=shopper, args=(shop,shoppingList_1, wynik,))
        thread2 = Thread(target=shopper, args=(shop,shoppingList_2, wynik,))
        thread3 = Thread(target=shopper, args=(shop,shoppingList_3, wynik,))
        thread4 = Thread(target=shopper, args=(shop,shoppingList_4, wynik,))
    
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
    
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
    
        for i in Items:
            if ile[i.name] > 0:
                print("Ok")
            else:
                if ile[i.name] == -wynik[i.name]:
                    print("Ok")
                else:
                    print("Źle")
    



.. parsed-literal::

    Źle
    Źle
    Źle


