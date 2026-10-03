Laboratoria 10 - Przetwarzanie danych strumieniowych w Apache Flink - API, model danych
=========================================================================================

**PyFlink** to interfejs API Pythona dla **Apache Flink**, który
umożliwia tworzenie skalowalnych obciążeń wsadowych i strumieniowych,
takich jak potoki przetwarzania danych w czasie rzeczywistym,
eksploracyjna analiza danych na dużą skalę, potoki uczenia maszynowego
(ML) i procesy ETL.

Instalacja na własnym komputerze:

.. class:: highlight

.. code:: python

    python -m pip install apache-flink==1.17.1

Począwszy od Flink 1.11, obsługiwane jest również lokalne uruchamianie
zadań PyFlink w systemie Windows, dzięki czemu można opracowywać i
debugować zadania PyFlink w systemie Windows.

Datastream
----------

Strumienie danych w bibliotece Flink nazywamy DataStream - strumieniami
danych. Służą one do opisu zarówno danych do przetwarzania
**strumieniowego** jak i **batchowego**, które w bibliotece Flink
posiadają ten sam interfejs do wykonywania operacji na danych.

Przetwarzanie strumieni danych DataStream we Flink to zwykłe programy,
które realizują transformacje na strumieniach danych (np. filtrowanie,
aktualizowanie stanu, definiowanie okien, agregowanie). Strumienie
danych są początkowo tworzone z różnych źródeł (np. kolejki komunikatów,
strumienie gniazd, pliki). Wyniki są zwracane przez ujścia (sink), które
mogą na przykład zapisywać dane do plików lub na standardowe wyjście (na
przykład terminal wiersza poleceń). Programy Flink działają w różnych
kontekstach, samodzielnie lub osadzone w innych programach. Wykonanie
może odbywać się w lokalnej maszynie JVM lub w klastrach wielu maszyn.

Struktura programu w Apache Flink
---------------------------------

Programy Flink wyglądają jak zwykłe programy, które przekształcają
strumienie danych. Każdy program składa się z tych samych podstawowych
części:

::

   Uzyskaj środowisko wykonawcze,
   Załaduj/utwórz dane początkowe / źródło danych,
   Określ przekształcenia na tych danych,
   Określ, gdzie umieścić wyniki swoich obliczeń,
   Uruchom wykonanie programu

Środowisko uruchomieniowe
-------------------------

StreamExecutionEnvironment jest podstawą wszystkich programów Flink.
Możesz go uzyskać za pomocą tych statycznych metod na obiekcie
StreamExecutionEnvironment:

getExecutionEnvironment();

createLocalEnvironment();

createRemoteEnvironment(String host, int port, String... jarFiles);

W naszym przypadku będziemy korzystać z **getExecutionEnvironment()**,
ponieważ wywołuje on potrzebną funkcję w zależności od kontekstu: jeśli
wykonujesz swój program w IDE lub jako zwykły program Java, utworzy
lokalne środowisko, które wykona twój program na twojej lokalnej
maszynie. Środowisko zapewnia metody kontrolowania wykonywania zadań
(takie jak ustawienie parametrów równoległości lub odporności na
błędy/punkty kontrolne) oraz interakcji ze światem zewnętrznym (dostęp
do danych).

Przykład tworzenia środowiska i ustawiania / odczytu paramertów można
znaleźć poniżej:

.. class:: highlight

.. code:: python

    from pyflink.common import ExecutionMode
    from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
    
    env = StreamExecutionEnvironment.get_execution_environment()
    
    env.set_runtime_mode(RuntimeExecutionMode.STREAMING)
    
    print(env.get_config().get_execution_mode())
    print(env.get_config().get_parallelism())
    
    env.get_config().set_execution_mode(ExecutionMode.BATCH)
    
    print(env.get_config().get_execution_mode())
    print(env.get_config().get_parallelism())


.. parsed-literal::

    ExecutionMode.PIPELINED
    6
    ExecutionMode.BATCH
    6


Tryb wykonywania (runtime_mode) **STREAMING** to sposób wykonywania
programów w zależności czy dane są skończone czy też nie. Streamin
powinno być używane w przypadku zadań bez ograniczeń, które wymagają
ciągłego przetwarzania przyrostowego i oczekuje się, że pozostaną w
trybie online przez nieokreślony czas.

Ponadto istnieje tryb wykonywania w stylu wsadowym, który nazywamy
trybem wykonywania **BATCH**. Wykonuje to zadania w sposób bardziej
przypominający ramy przetwarzania wsadowego, takie jak MapReduce. Batch
powinno być używane w przypadku zadań ograniczonych, dla których znane
są stałe dane wejściowe i które nie są wykonywane w sposób ciągły.

Trzecia opcja to **AUTOMATIC** pozwalająca wybrać tryb przetwarzania
bazując na typie źródła danych.

Zunifikowane podejście Apache Flink do przetwarzania strumieniowego i
wsadowego oznacza, że aplikacja DataStream wykonywana na ograniczonych
danych wejściowych będzie generować **takie same** wyniki końcowe
niezależnie od skonfigurowanego trybu wykonywania.

Ważne jest, aby zauważyć, co oznacza tutaj final: zadanie wykonywane w
trybie STREAMING może generować przyrostowe aktualizacje (pomyśl o
upsertach w bazie danych), podczas gdy zadanie BATCH dałoby tylko jeden
końcowy wynik na końcu.

Obok runtime mode możemy zdefiniować także execution mode - określa on w
jaki sposób program wsadowy jest wykonywany pod względem wymiany danych:
potokowo lub wsadowo.

Istnieje jeszcze jedna skrócona forma pobierania ustawień dla
przetwarzania batchowego lub strumieniowego, która jest stosowana w
niektórych przykładach ponizej.

.. class:: highlight

.. code:: python

    from pyflink.table import EnvironmentSettings
    
    env_settings = EnvironmentSettings.in_streaming_mode()

.. class:: highlight

.. code:: python

    from pyflink.table import EnvironmentSettings
    
    env_settings = EnvironmentSettings.in_batch_mode()

Źródła danych
-------------

Najprostszym źródłem danych jest kolekcja. Tworzy ono źródło ztrumienia.
Najprostsze przetwarzanie wypisze ten strumień na ekran, aby wywołać
uruchomić przetwarzanie na środowisku musimy wykonać metodę
**execute()**.

.. class:: highlight

.. code:: python

    from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
    
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.BATCH)
    
    data_stream = env.from_collection(collection=[1, 2, 3, 4, 5]).print()
    
    env.execute()

.. parsed-literal::

	3
	1
	2
	4
	5	

.. class:: highlight

.. code:: python

    from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
    
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.STREAMING)
    
    data_stream = env.from_collection(collection=[1, 2, 3, 4, 5]).print()
    
    env.execute()

.. parsed-literal::

	2> 4
	3> 5
	12> 2
	11> 1
	1> 3

Jak widać różnica w tm wypadku to sposób wypisywania danych w przypadku
strumieniowego podejścia widzimy też na ekranie identyfikator jednostki
przetwarzającej zadanie. Uwaga! w przypadku przetwarzania strumieni
lokalnie w systemie czasem zadania sa zamykane za wcześnie i pokazuje
się błąd komunikacji między węzłami Flink, ciężko jest powiedzieć jak
temu zaradzić, i jedynym rozwiazaniem jest ignorowanie błędu lub próba
uruchomienia programu raz jeszcze. Błąd ma postać:

.. parsed-literal::

	grpc._channel._MultiThreadedRendezvous: <_MultiThreadedRendezvous of RPC that terminated with:
		status = StatusCode.CANCELLED
		details = "Multiplexer hanging up"
		debug_error_string = "UNKNOWN:Error received from peer ipv6:%5B::1%5D:45267 {created_time:"2023-06-04T21:26:24.200378935+02:00", grpc_status:1, grpc_message:"Multiplexer hanging up"}"

Generycznym typem źródła danych jest obiekt **Source**:

.. class:: highlight

.. code:: python

    env = StreamExecutionEnvironment.get_execution_environment()
    
    my_source = ...
    
    env.from_source(
        my_source,
        "my_source_name")

Przykładem Source mogą być pliki, inne źródła danych jak Kafka itp.
Poniżej plik a.csv :

.. parsed-literal::


	1|Berlin
	2|San Francisco
	3|Beijing

Program czytający plik jako wejście dla przetwarzania. Definiujemy w
obiekcie schemat danych które są odczytywane jako wiersze do strumienia
wejściowego.

.. class:: highlight

.. code:: python

    from pathlib import Path
    
    from pyflink.common import WatermarkStrategy
    from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
    from pyflink.datastream.connectors.file_system import FileSource
    from pyflink.datastream.formats.csv import CsvSchema, CsvReaderFormat
    from pyflink.table import DataTypes
    
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.BATCH)
    
    schema = CsvSchema.builder() \
        .add_number_column('id', number_type=DataTypes.BIGINT()) \
        .add_string_column('name') \
        .set_column_separator('|') \
        .build()
    
    source = FileSource.for_record_stream_format(
        CsvReaderFormat.for_schema(schema), 'a.csv').build()
    
    # the type of record will be Types.ROW_NAMED(['id', 'array'], [Types.LONG(), Types.LIST(Types.INT())])
    ds = env.from_source(source, WatermarkStrategy.no_watermarks(), 'csv-source').print()
    
    env.execute()

.. parsed-literal::
	
	+I(1,Berlin)
	+I(2,San Francisco)
	+I(3,Beijing)

Ten sam plik czytany jako dane txt linijka po linijce:

.. class:: highlight

.. code:: python

    from pyflink.common import WatermarkStrategy
    from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
    from pyflink.datastream.connectors.file_system import FileSource, StreamFormat
    
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.BATCH)
    
    source = FileSource \
        .for_record_stream_format(StreamFormat.text_line_format(), 'a.csv') \
        .build()
    
    stream = env.from_source(source, WatermarkStrategy.no_watermarks(), "file-source").print()
    
    env.execute()

.. parsed-literal::

	1|Berlin
	2|San Francisco
	3|Beijing

Środowisko Table i Datastream
-----------------------------

TableEnvironment jest punktem wejścia dla integracji Table API i SQL i
odpowiada za:

::

    Rejestrację tabeli w katalogu wewnętrznym
    Wykonywanie zapytań SQL
    Rejestrowanie funkcji zdefiniowanych przez użytkownika
    Konwersję między DataStream a Table (w przypadku StreamTableEnvironment)

Tabela jest zawsze powiązana z określonym środowiskiem TableEnvironment.
Stąd z naszym środowiskiem uruchomieniowym musimy połączyć obiekt
środowiska tabelarycznego. Nie jest możliwe łączenie tabel różnych
TableEnvironments w tym samym zapytaniu, np. join lub union.
TableEnvironment jest tworzony przez wywołanie statycznej metody
TableEnvironment.create().

Poniżej podano dwa sposoby tworzenia takiego środowiska.

.. class:: highlight

.. code:: python

    from pyflink.table import EnvironmentSettings, TableEnvironment
    
    # create a streaming TableEnvironment
    env_settings = EnvironmentSettings.in_streaming_mode()
    table_env = TableEnvironment.create(env_settings)

.. class:: highlight

.. code:: python

    from pyflink.datastream import StreamExecutionEnvironment
    from pyflink.table import StreamTableEnvironment
    
    s_env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(s_env)

TableEnvironment utrzymuje mapę katalogów tabel, które są tworzone z
identyfikatorem. Każdy identyfikator składa się z 3 części: nazwy
katalogu, nazwy bazy danych oraz nazwy obiektu.

Tabele mogą być wirtualne (WIDOK) lub zwykłe (TABELA). WIDOKI można
tworzyć z istniejącego obiektu tabeli, zazwyczaj w wyniku działania
interfejsu API tabeli lub zapytania SQL. TABELE opisują dane zewnętrzne,
takie jak plik, tabela bazy danych lub kolejka komunikatów.

Tabele służą za źródła danych jak i jako obiekty pośrednie przy
transformacji danych. Tabele możemy tworzyć zapisując obiekty na sztywno
w kodzie jako kolekcje w Pythonie lub odczytując je ze źródeł takich jak
pliki, tabele czy też zewnętrzne systemy (jak Kafka).

Tworzenie tabel na postawie zapisanych na sztywno danych. Pyflink
wspiera użytkowników w tworzeniu tabel źródłowych z podanej listy.
Poniższy przykład definiuje tabelę zawierającą trzy wiersze danych:
[(Hello, 1), ((world, 2), ((Flink, 3)]), która ma dwie kolumny z nazwami
kolumn a i b oraz typami varchar i bigint.

.. class:: highlight

.. code:: python

    from pyflink.datastream import StreamExecutionEnvironment
    from pyflink.table import StreamTableEnvironment
    
    s_env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(s_env)
    
    tab = t_env.from_elements([("hello", 1), ("world", 2), ("flink", 3)], ['a', 'b']).print_schema()

.. parsed-literal::

    (
      `a` STRING,
      `b` BIGINT
    )


Ta metoda jest zwykle używana w fazie testowej, gdyż może szybko
utworzyć tabelę źródła danych w celu weryfikacji logiki zadania.
Pierwszy parametr służy do określenia listy danych. Każdy element na
liście musi być typu krotki; Drugi parametr określa schemat tabeli.

Tworzenie tabel za pomocą SQL API. Poniżej podano przykład różnego
rodzaju tworzenia tabel i nazwania kolumn. Metoda to_pandas pozwala nam
wypisać dane z tabeli na ekran.

.. class:: highlight

.. code:: python

    from pyflink.table import EnvironmentSettings, TableEnvironment, DataTypes
    
    settings = EnvironmentSettings.in_batch_mode()
    tbl_env = TableEnvironment.create(settings)
    
    products = [
        ('Mleko', 3.99),
        ('Chleb', 5.99),
        ('Mąka', 4.99),
        ('Jajka', 14.99)
    ]
    
    # simple table
    simple_data = tbl_env.from_elements(products)
    
    print('\nsimple_data schema')
    simple_data.print_schema()
    
    print('\nsimple_data data')
    print(simple_data.to_pandas())
    
    #####################################################
    col_names = ['product', 'price']
    simple_with_column_names = tbl_env.from_elements(products, col_names)
    print('\nsimple_with_column_names schema')
    simple_with_column_names.print_schema()
    
    print('\nsimple_with_column_names data')
    print(simple_with_column_names.to_pandas())
    
    #####################################################
    schema = DataTypes.ROW([
        DataTypes.FIELD('product', DataTypes.STRING()),
        DataTypes.FIELD('price', DataTypes.DOUBLE())
    ])
    table_with_schema = tbl_env.from_elements(products, schema)
    
    print('\ntable_with_schema schema')
    table_with_schema.print_schema()
    
    print('\ntable_with_schema data')
    print(table_with_schema.to_pandas())

.. parsed-literal::

	simple_data schema
	(
	`_1` STRING,
	`_2` DOUBLE
	)
	
	simple_data data
		_1     _2
	0  Mleko   3.99
	1  Chleb   5.99
	2   Mąka   4.99
	3  Jajka  14.99

	simple_with_column_names schema
	(
	`product` STRING,
	`price` DOUBLE
	)

	simple_with_column_names data
	product  price
	0   Mleko   3.99
	1   Chleb   5.99
	2    Mąka   4.99
	3   Jajka  14.99
	
	table_with_schema schema
	(
	`product` STRING,
	`price` DOUBLE
	)
	
	table_with_schema data
	product  price
	0   Mleko   3.99
	1   Chleb   5.99
	2    Mąka   4.99
	3   Jajka  14.99
	
Transformacje danych i operatory
--------------------------------

Tabele
------

Operatorzy przekształcają jeden lub więcej strumieni danych w nowy
strumień danych. Łańcuchy wywołań mogą łączyć wiele transformacji w
wyrafinowane topologie przepływu danych.

Interfejs SQL (sql_query) pozwala nam na tworzenie zapytań typu SQL dla
tabel i uruchamianiu ich na strumieniu danych.

Uwaga! Żeby podejrzeć jak wygląda nasz strumień wywołujemy metodę
to_pandas, która zrzucam nam tabelę do obiektu bibliotki pandas, który
możemy poźniej łatwo wypisać poprzez print. Nie ma innej prostej metody
podejrzenia zawartości tabeli.

.. class:: highlight

.. code:: python

    from pyflink.table import (
        TableEnvironment, EnvironmentSettings
    )
    
    env_settings = EnvironmentSettings.in_batch_mode()
    table = TableEnvironment.create(env_settings)
    
    table.execute_sql(f"""
        CREATE TABLE countries(
            code STRING,
            name STRING,
            continent STRING,
            wikipedia_link STRING
            ) WITH ( 
            'connector' = 'filesystem',
            'path' = 'countries.csv',
            'format' = 'csv')
        """)
    
    # important to note that operations will be parallelized over
    # task slots across system cores so output will appear randomly
    # ordered and differ from run to run
    
    # SQL query is run on the env not table!
    codes2 = table.sql_query(f"""
            SELECT code, name AS nazwa, CHARACTER_LENGTH(name) as nameLength
            FROM countries
        """)
    print('\nCodes_2 table')
    print(codes2.to_pandas())
    
    print('\nSchema')
    codes2.print_schema()

.. parsed-literal::

	Codes_2 table
		code                          nazwa  nameLength
	0     AD                        Andorra           7
	1     AE           United Arab Emirates          20
	2     AF                    Afghanistan          11
	3     AG            Antigua and Barbuda          19
	4     AI                       Anguilla           8
	..   ...                            ...         ...
	243   YT                        Mayotte           7
	244   ZA                   South Africa          12
	245   ZM                         Zambia           6
	246   ZW                       Zimbabwe           8
	247   ZZ  Unknown or unassigned country          29

	[248 rows x 3 columns]

	Schema
	(
	`code` STRING,
	`nazwa` STRING,
	`nameLength` INT
	)

Lista wspieranych typów danych dla TableAPI:

::

   https://nightlies.apache.org/flink/flink-docs-release-1.17/docs/dev/python/table/python_types/

Table API to ujednolicony, relacyjny interfejs API do przetwarzania
strumieniowego i wsadowego. Zapytania interfejsu API tabel można
uruchamiać na danych wejściowych wsadowych lub przesyłanych strumieniowo
bez modyfikacji.

Table API jest superzbiorem języka SQL i jest specjalnie zaprojektowany
do pracy z Apache Flink. Table API to zintegrowany język API dla Scali,
Javy i Pythona. Poniżej znajdziemy przykłady wywołania tych metod.

.. class:: highlight

.. code:: python

    from pyflink.table import (
        TableEnvironment, EnvironmentSettings, DataTypes
    )
    
    env_settings = EnvironmentSettings.in_batch_mode()
    t_env = TableEnvironment.create(env_settings)
    
    table = t_env.from_elements(
      [(1, 'ABC'), (2, 'ABCDE')],
      schema=DataTypes.ROW([DataTypes.FIELD('id', DataTypes.INT()),
                            DataTypes.FIELD('name', DataTypes.STRING())]))
    table.print_schema()
    # select
    print("SELECT")
    print(table.select(table.id, table.name.alias('nazwa')).to_pandas())
    # where
    print("WHERE")
    print(table.where(table.id == 1).to_pandas())
    print(table.filter(table.id == 2).to_pandas())
    
    table2 = t_env.from_elements(
      [(1, 'ABC'),(3, 'ABC'), (2, 'ABCDE')],
      schema=DataTypes.ROW([DataTypes.FIELD('id', DataTypes.INT()),
                            DataTypes.FIELD('name', DataTypes.STRING())]))
    table = table.union_all(table2)
    print("UNION")
    print(table.to_pandas())
    print(table2.to_pandas())
    # group_by
    print("GROUP")
    print(table.group_by(table.name).select(table.name, table.id.count.alias('sum')).to_pandas())
    # dictinct
    print("DISTINCT")
    print(table.distinct().to_pandas())

.. parsed-literal::

	(
	`id` INT,
	`name` STRING
	)
	SELECT
	id  nazwa
	0   1    ABC
	1   2  ABCDE
	WHERE
	id name
	0   1  ABC
	id   name
	0   2  ABCDE
	UNION
	id   name
	0   1    ABC
	1   2  ABCDE
	2   1    ABC
	3   3    ABC
	4   2  ABCDE
	id   name
	0   1    ABC
	1   3    ABC
	2   2  ABCDE
	GROUP
		name  sum
	0  ABCDE    2
	1    ABC    3
	DISTINCT
	id   name
	0   2  ABCDE
	1   3    ABC
	2   1    ABC

Lista wszystkich metod dostępna jest tutaj:

https://nightlies.apache.org/flink/flink-docs-release-1.17/api/python/reference/pyflink.table/table.html

DataStream
----------

DataStream jest podobny do zwykłych kolekcji Pythona pod względem
użycia, ale różni się pod pewnymi kluczowymi względami. Datastream są
niemutowalne (niezmienne), co oznacza, że po ich utworzeniu nie można
dodawać ani usuwać elementów. Nie ma też dostępu do elementów
środkowych, a operacje na nich można prowadzić tylko poprzez
transformacjami.

Tworzenie DataStream:

.. class:: highlight

.. code:: python

    from pyflink.common.typeinfo import Types
    from pyflink.datastream import StreamExecutionEnvironment
    
    env = StreamExecutionEnvironment.get_execution_environment()
    ds = env.from_collection(
        collection=[(1, 'aaa|bb'), (2, 'bb|a'), (3, 'aaa|a')],
        type_info=Types.ROW([Types.INT(), Types.STRING()]))

Parametr type_info jest opcjonalny, jeśli nie zostanie określony, typem
wyjściowym zwróconego strumienia danych będzie
Types.PICKLED_BYTE_ARRAY().

Możesz wywołać metodę print, aby wydrukować dane DataStream na
standardowe wyjście, lub wykorzystac metodę executeAndCollect do
pobrania kolekcji. Print wypisuje nam operacje na strumieniu +I oznacza
w tym wypadku insert i jest to taka konwencja Flinka.

.. class:: highlight

.. code:: python

    from pyflink.common.typeinfo import Types
    from pyflink.datastream import StreamExecutionEnvironment
    
    env = StreamExecutionEnvironment.get_execution_environment()
    ds = env.from_collection(
        collection=[(1, 'aaa|bb'), (2, 'bb|a'), (3, 'aaa|a')],
        type_info=Types.ROW([Types.INT(), Types.STRING()]))
    
    ds.print()
    env.execute()
    
    with ds.execute_and_collect() as results:
        for result in results:
            print(result)

.. parsed-literal::

	6> +I[3,aaa|a]
	5> +I[2,bb|a]
	4> +I[1,aaa|bb]
	<Row(1, 'aaa|bb')>
	<Row(2, 'bb|a')>
	<Row(3, 'aaa|a')>

Lista wspieranych typów danych dla DataStream:

::

   https://nightlies.apache.org/flink/flink-docs-release-1.17/docs/dev/python/datastream/data_types/

Możemy sfobodnie przechodzić między tabelami a strumieniami i korzystać
na zmianę z obi API. Przykład konwersji między DataStream <-> Table
znajdziemy poniżej:

.. class:: highlight

.. code:: python

    from pyflink.common.typeinfo import Types
    from pyflink.datastream import StreamExecutionEnvironment
    from pyflink.table import StreamTableEnvironment, DataTypes
    
    env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(stream_execution_environment=env)
    
    t_env.execute_sql("""
            CREATE TABLE my_source (
              a INT,
              b VARCHAR
            ) WITH (
              'connector' = 'datagen',
              'number-of-rows' = '10'
            )
        """)
    
    # DS -> TABLE
    
    ds = t_env.to_append_stream(
        t_env.from_path('my_source'),
        Types.ROW([Types.INT(), Types.STRING()]))
    
    table = t_env.from_data_stream(ds)
    print(table.to_pandas())
    
    # TABLE -> DS
    
    s_env2 = StreamExecutionEnvironment.get_execution_environment()
    t_env2 = StreamTableEnvironment.create(s_env2)
    
    schema = DataTypes.ROW([
        DataTypes.FIELD('name', DataTypes.STRING()),
        DataTypes.FIELD('nr', DataTypes.INT())
    ])
    table_with_schema = t_env2.from_elements([("hello", 1), ("world", 2), ("flink", 3)], schema)
    ds = t_env2.to_append_stream(table_with_schema, Types.ROW([Types.STRING(), Types.INT()]))
    
    ds.print()
    
    s_env2.execute()


Operatory
---------

Operatory przekształcają jeden lub więcej strumieni danych w nowy
strumień danych. Są to znane nam funkcje map, filter, flatmap itp.

Przykłady:

.. class:: highlight

.. code:: python

    from pyflink.common.typeinfo import Types
    from pyflink.datastream import StreamExecutionEnvironment
    
    env = StreamExecutionEnvironment.get_execution_environment()
    
    # Map
    
    data_stream = env.from_collection(collection=[1, 2, 3, 4, 5])
    data_stream.map(lambda x: 2 * x, output_type=Types.INT()).print()
    
    env.execute()
    print('-----')
    
    # FlatMap
    
    data_stream = env.from_collection(collection=['hello apache flink', 'streaming compute'])
    data_stream.flat_map(lambda x: x.split(' '), output_type=Types.STRING()).print()
    
    env.execute()
    print('-----')
    
    # Filter
    
    data_stream = env.from_collection(collection=[0, 1, 2, 3, 4, 5])
    data_stream.filter(lambda x: x != 0).print()
    
    env.execute()
    print('-----')
    
    # Key_By
    
    data_stream = env.from_collection(collection=[(1, 'a'), (2, 'a'), (3, 'b')])
    data_stream.key_by(lambda x: x[1], key_type=Types.STRING()).print()
    
    env.execute()
    print('-----')
    
    # Reduce
    
    data_stream = env.from_collection(collection=[(1, 'a'), (2, 'a'), (3, 'a'), (4, 'b')], type_info=Types.TUPLE([Types.INT(), Types.STRING()]))
    data_stream.key_by(lambda x: x[1]).reduce(lambda a, b: (a[0] + b[0], b[1])).print()
    
    env.execute()
    print('-----')
    
    # Partition
    
    partition = 3
    data_stream = env.from_collection(collection=[(2, 'a'), (2, 'a'), (3, 'b')])
    data_stream.partition_custom(lambda key, num_partition: key % partition, lambda x: x[0]).print()
    
    env.execute()
    print('-----')

.. parsed-literal::
	
	4> 4
	7> 10
	6> 8
	3> 2
	5> 6
	-----
	3> streaming
	3> compute
	2> hello
	2> apache
	2> flink
	-----
	8> 2
	10> 4
	9> 3
	7> 1
	11> 5
	-----
	7> (1, 'a')
	7> (2, 'a')
	7> (3, 'b')
	-----
	4> (1,a)
	4> (3,a)
	4> (6,a)
	1> (4,b)
	-----
	1> (3, 'b')
	3> (2, 'a')
	3> (2, 'a')
	-----
	
Operatory możemy także definiować sami implementując odpowiednie clasy
implementujące interfejsy, jako funkcje lub lambdy:

.. class:: highlight

.. code:: python

    import time
    from pyflink.common.typeinfo import Types
    from pyflink.datastream import StreamExecutionEnvironment, MapFunction
    
    env = StreamExecutionEnvironment.get_execution_environment()
    
    
    # Implementing MapFunction
    class MyMapFunction(MapFunction):
    
        def map(self, value):
            return value + 1
    
    data_stream = env.from_collection([1, 2, 3, 4, 5], type_info=Types.INT())
    mapped_stream = data_stream.map(MyMapFunction(), output_type=Types.INT()).print()
    
    env.execute()
    print('-----')
    time.sleep(2.4)
    
    data_stream = env.from_collection([1, 2, 3, 4, 5], type_info=Types.INT())
    mapped_stream = data_stream.map(lambda x: x + 1, output_type=Types.INT()).print()
    
    env.execute()
    print('-----')
    time.sleep(2.4)
    
    def my_map_func(value):
        return value + 1
    
    data_stream = env.from_collection([1, 2, 3, 4, 5], type_info=Types.INT())
    mapped_stream = data_stream.map(my_map_func, output_type=Types.INT()).print()
    
    env.execute()
    print('-----')

.. parsed-literal::

	7> 3
	9> 5
	10> 6
	6> 2
	8> 4
	-----
	1> 3
	2> 4
	12> 2
	3> 5
	4> 6
	-----
	10> 6
	8> 4
	9> 5
	6> 2
	7> 3

User defined function pozwalają nam na definiowanie różnych typów danych
na wejściu i wyjściu metody, co jest przypadne w funkcji map.

.. class:: highlight

.. code:: python

    from statistics import stdev, mean
    
    from pyflink.common import Row
    from pyflink.table import (
        DataTypes,
        TableEnvironment,
        EnvironmentSettings
    )
    from pyflink.table.udf import udf
    
    
    @udf(result_type=DataTypes.ROW([DataTypes.FIELD('code', DataTypes.STRING()),
                                    DataTypes.FIELD('total_length', DataTypes.INT()),
                                    DataTypes.FIELD('qtr_avg', DataTypes.DOUBLE()),
                                    DataTypes.FIELD('qtr_stdev', DataTypes.DOUBLE())]))
    def sales_summary_stats(country: Row) -> Row:
        code, name, continent, wiki = country
        country_stats = (len(code), len(name), len(continent), len(wiki))
        total_length = sum(country_stats)
        qtr_avg = round(mean(country_stats), 2)
        qtr_stdev = round(stdev(country_stats), 2)
        return Row(code, total_length, qtr_avg, qtr_stdev)
    
    
    env_settings = EnvironmentSettings.in_batch_mode()
    table = TableEnvironment.create(env_settings)
    
    table.execute_sql(f"""
        CREATE TABLE countries(
            code STRING,
            name STRING,
            continent STRING,
            wikipedia_link STRING
            ) WITH ( 
            'connector' = 'filesystem',
            'path' = 'countries.csv',
            'format' = 'csv')
        """)
    
    tableInput = table.from_path('countries')
    
    print('\nCountries Schema')
    tableInput.print_schema()
    
    country_stats = tableInput.map(sales_summary_stats).alias('code',
                                                              'total_length',
                                                              'quarter_avg',
                                                              'quarter_stdev')
    
    print('\nSales Summary Stats schema')
    country_stats.print_schema()
    
    print('\nSales Summary Stats data')
    print(country_stats.to_pandas().sort_values('code'))

.. parsed-literal::

	Countries Schema
	(
	`code` STRING,
	`name` STRING,
	`continent` STRING,
	`wikipedia_link` STRING
	)
	
	Sales Summary Stats schema
	(
	`code` STRING,
	`total_length` INT,
	`quarter_avg` DOUBLE,
	`quarter_stdev` DOUBLE
	)
	
	Sales Summary Stats data
		code  total_length  quarter_avg  quarter_stdev
	0     AD            48         12.0          16.83
	1     AE            74         18.5          22.65
	2     AF            56         14.0          18.49
	3     AG            72         18.0          22.17
	4     AI            50         12.5          17.23
	..   ...           ...          ...            ...
	243   YT            48         12.0          16.83
	244   ZA            58         14.5          18.93
	245   ZM            46         11.5          16.44
	246   ZW            50         12.5          17.23
	247   ZZ            92         23.0          27.17
	
	[248 rows x 4 columns]

Stany
-----

Stan pomaga nam zapamiętać dodatkowe informacje związane z
przychodzącymi danymi. Jest to niezbędne gdy chcemy np. wyliczyć średnią
z przychodzących wartości.

Jeśli chcesz użyć stanu, musisz najpierw określić klucz dla każdej danej
w DataStream, który powinien być użyty do partycjonowania stanu (a także
samych rekordów w strumieniu). Możesz określić klucz za pomocą
keyBy(KeySelector) w Java/Scala API lub key_by(KeySelector) w Python API
na DataStream. Spowoduje to wygenerowanie KeyedStream, który następnie
zezwoli na operacje używające stanu klucza.

Funkcja selektora klucza pobiera pojedynczy rekord jako dane wejściowe i
zwraca klucz dla tego rekordu. Klucz może być dowolnego typu i musi
pochodzić z obliczeń deterministycznych.

Aby uzyskać uchwyt stanu, musisz utworzyć StateDescriptor. Zawiera on
nazwę stanu (jak zobaczymy później, możesz utworzyć kilka stanów i muszą
one mieć unikalne nazwy, aby można było się do nich odwoływać), typ
wartości, które stan przechowuje i czasem funkcje użytkownika- określona
funkcja, taka jak ReduceFunction. W zależności od typu stanu, który
chcesz pobrać, tworzysz ValueStateDescriptor, ListStateDescriptor,
AggregatingStateDescriptor, ReducingStateDescriptor lub
MapStateDescriptor.

W poniższym przykładzie definiujemy własną metodę map, która w metodzie
open tworzy stan ValueState, będący liczbą typu long. W metodzie map
wywołujemy funkcje value() i funkcje update() na ValueState żeby
przechowywać licznik wczytanych danych. Dane są związane w stany kluczem
definiowanym w linijce

::

   .key_by(lambda a: a[0]) 

Dostęp do stanu uzyskuje się za pomocą RuntimeContext, poprzez
implementacje tzw. rich functions. Rich functions zapewniają, oprócz
funkcji zdefiniowanych przez użytkownika (map, reduce itp.), cztery
metody: open, close, getRuntimeContext, and setRuntimeContext.

.. class:: highlight

.. code:: python

    from pyflink.common import WatermarkStrategy, Row
    from pyflink.common.typeinfo import Types
    from pyflink.datastream import StreamExecutionEnvironment
    from pyflink.datastream.connectors import NumberSequenceSource
    from pyflink.datastream.functions import RuntimeContext, MapFunction
    from pyflink.datastream.state import ValueStateDescriptor
    
    
    class MyMapFunction(MapFunction):
    
        def open(self, runtime_context: RuntimeContext):
            state_desc = ValueStateDescriptor('cnt', Types.LONG())
            # Define value state
            self.cnt_state = runtime_context.get_state(state_desc)
    
        def map(self, value):
            cnt = self.cnt_state.value()
            if cnt is None:
                cnt = 0
    
            new_cnt = cnt + 1
            self.cnt_state.update(new_cnt)
            return value[0], new_cnt
    
    
    # 1. Create streamexecutionenvironment
    env = StreamExecutionEnvironment.get_execution_environment()
    
    # 2. Create data source
    seq_num_source = NumberSequenceSource(1, 10)
    ds = env.from_source(
        source=seq_num_source,
        watermark_strategy=WatermarkStrategy.for_monotonous_timestamps(),
        source_name='seq_num_source',
        type_info=Types.LONG())
    
    # 3. Define execution logic
    ds = ds.map(lambda a: Row(a % 4, 1), output_type=Types.ROW([Types.LONG(), Types.LONG()])) \
        .key_by(lambda a: a[0]) \
        .map(MyMapFunction(), output_type=Types.TUPLE([Types.LONG(), Types.LONG()])) \
        .print()
    
    # 4. Perform the operation
    env.execute()

.. parsed-literal::

	4> (1,1)
	4> (1,2)
	4> (1,3)
	3> (0,1)
	3> (0,2)
	2> (2,1)
	2> (2,2)
	2> (2,3)
	7> (3,1)
	7> (3,2)

Ujście (sink)
-------------

Ujścia danych zużywają strumienie danych i przesyłają je do plików,
gniazd, systemów zewnętrznych lub drukują je. Flink ma wiele wbudowanych
formatów wyjściowych, które są zamknięte w operacjach na strumieniach
danych:

::

   writeAsText() / TextOutputFormat — Zapisuje elementy liniowo jako łańcuchy. Łańcuchy są uzyskiwane przez wywołanie metody toString() każdego elementu.

    writeAsCsv(...) / CsvOutputFormat — zapisuje krotki jako pliki wartości oddzielonych przecinkami. Ograniczniki wierszy i pól można konfigurować. Wartość dla każdego pola pochodzi z metody toString() obiektów.

    print() / printToErr() — Drukuje wartość toString() każdego elementu w standardowym wyjściu / standardowym strumieniu błędów. Opcjonalnie można podać prefiks (msg), który jest dołączany do danych wyjściowych. Może to pomóc w rozróżnieniu różnych wezwań do drukowania. Jeśli równoległość jest większa niż 1, dane wyjściowe zostaną również poprzedzone identyfikatorem zadania, które wygenerowało dane wyjściowe.

    writeUsingOutputFormat() / FileOutputFormat — metoda i klasa bazowa dla niestandardowych plików wyjściowych. Obsługuje niestandardową konwersję obiektów na bajty.

    writeToSocket — zapisuje elementy do gniazda zgodnie ze schematem SerializationSchema

    addSink — Wywołuje niestandardową funkcję ujścia. Flink jest dostarczany w pakiecie ze złączami do innych systemów (takich jak Apache Kafka), które są zaimplementowane jako funkcje ujścia.

.. class:: highlight

.. code:: python

    from pyflink.common import Encoder, Types
    from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
    from pyflink.datastream.connectors.file_system import FileSink, OutputFileConfig, RollingPolicy
    
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.BATCH)
    
    data_stream = env.from_collection(collection=[1, 2, 3, 4, 5]).print()
    
    env.execute()
    
    data_stream = env.from_collection(collection=['as','bb','cc','dd'])\
        .map(lambda i: i, output_type=Types.STRING())\
        .sink_to(
        sink=FileSink.for_row_format(
            base_path="output",
            encoder=Encoder.simple_string_encoder())
        .with_output_file_config(
            OutputFileConfig.builder()
            .build())
        .build()
    )
    
    env.execute()

Uwaga! Program zapisuje wyniki w częściowych plikach w katalogu output.
Nie znane jest mi sposób zmuszenia flinka do wygenerowania pojedynczego
pliku.

Za pomocą Table API wynik zapisujemy do tabeli wynikowej.

.. class:: highlight

.. code:: python

    from pyflink.table import (
        TableEnvironment, EnvironmentSettings, DataTypes
    )
    
    env_settings = EnvironmentSettings.in_batch_mode()
    t_env = TableEnvironment.create(env_settings)
    
    table = t_env.from_elements(
      [(1, 'ABC'), (2, 'ABCDE')],
      schema=DataTypes.ROW([DataTypes.FIELD('id', DataTypes.INT()),
                            DataTypes.FIELD('name', DataTypes.STRING())]))
    table.print_schema()
    t_env.execute_sql("""
        CREATE TABLE print (
            id INT,
            data STRING
        ) WITH (
            'connector' = 'print'
        )
    """)
    table.select(table.id, table.name.alias('nazwa')).execute_insert("print").wait()

.. parsed-literal::


	(
	`id` INT,
	`name` STRING
	)
	+I[1, ABC]
	+I[2, ABCDE]
	
Poniższy program wykorzystuje plik **countries.csv** i zapisuje wynik do
pliku.

.. class:: highlight

.. code:: python

    from pyflink.table import (
        DataTypes, TableEnvironment, EnvironmentSettings,
        TableDescriptor, Schema
    )
    
    env_settings = EnvironmentSettings.new_instance().in_batch_mode().build()
    table = TableEnvironment.create(env_settings)
    
    # all data to one output file
    table.get_config().get_configuration().set_string("parallelism.default", "1")
    
    table.execute_sql(f"""
            CREATE TABLE countries(
                code STRING,
                name STRING,
                continent STRING,
                wikipedia_link STRING
                ) WITH ( 
                'connector' = 'filesystem',
                'path' = 'countries.csv',
                'format' = 'csv')
            """)
    
    tableInput = table.from_path('countries')
    
    print('\nSchema')
    tableInput.print_schema()
    
    table.create_temporary_table('resultTable', TableDescriptor.for_connector('filesystem')
                                 .schema(Schema.new_builder()
                                         .column("code", DataTypes.STRING())
                                         .column("name", DataTypes.STRING())
                                         .column("continent", DataTypes.STRING())
                                         .column("wiki", DataTypes.STRING())
                                         .build())
                                 .option('path', 'result')
                                 .option('partition.default-name', 'result')
                                 .format('csv')
                                 .build())
    
    tableOutput = table.from_path('resultTable')
    
    tableOutput.print_schema()
    
    tableInput.execute_insert('resultTable').wait()

