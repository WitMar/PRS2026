.. role:: important

.. role:: badimportant

=======================
Programming Laboratory
=======================

--------------------
React
--------------------

.. class:: important 

    .. class:: important 

    Uwaga! cały kod znajduje się na gałęzi **ReactStart** w repozytorium https://github.com/WitMar/PRA2024 . Kod końcowy w gałęzi **ReactEnd**.
       
Jeżeli nie widzisz odpowiednich gałęzi na GitHubie wykonaj **Ctr+T**, a jak to nie pomoże to wybierz z menu **VCS->Git->Fetch**. 

Node
-----

W celu uruchomienia React na swoim komputerze potrzebujesz dwóch elementów Node i npm. Zalecane wersje to **Node v8.0.0** i **npm v6.14.7**.

Node.js to środowisko programistyczne przeznaczone do tworzenia wysoce skalowalnych aplikacji internetowych, w szczególności serwerów WWW napisanych w JavaScript. Node.js umożliwia tworzenie aplikacji sterowanych zdarzeniami, które korzystają z asynchronicznego systemu we/wy.

W systemach Linux wyszukaj czy masz już zainstalowane pakiety nodejs i npm, np. instalacja dla Ubuntu wygląda tak:

.. code:: bash

    sudo apt-get install nodejs npm

Instalacja na windows:

	| https://phoenixnap.com/kb/install-node-js-npm-on-windows

Środowisko pracy z javascriptem może być dowolnym edytorem tekstu lub bardziej zaawansowanym środowiskiem np. bardzo podobnym do IntelliJ (jest to bardzo pomocne w wyszukiwaniu błędów składniowych i składniowych w kodzie).

    | https://www.jetbrains.com/webstorm/

    
Instalacja zależności w domu
------------------------------------

Aplikacja wymaga posiadania na komputerze instalacji node: https://nodejs.org/en/

Aby utworzyć nową aplikację, najprosćiej jest wykorzystać następującą metodę:

.. code:: bash

    npx create-react-app todoapp
    
Uwaga! Aby uruchomić polecenie, musisz mieć wersję **Node >= 10** na swoim lokalnym komputerze programistycznym. Możesz użyć **nvm** (macOS/Linux) lub **nvm-windows**, aby zainstalować i przełączać się między wersjami Node na swoim komputerze. Powyższe polecenie utworzy strukturę plików nowego projektu.    

Jeżeli otwierasz już pobraną aplikację, to z poziomu terminala w katalogu projektu należy wywołać następujące polecenia:


.. code:: bash
    
    npm start

Errors
--------

Jeżeli zobaczysz błąd:

.. code:: bash

    npm ERR! ENOTFOUND code
    npm ERR! errno ENOTFOUND
    npm ERR! network request to https://registry.npmjs.org/inline-process-browser/-/inline-process-browser-1.0.0.tgz failed, reason: getaddrinfo ENOTFOUND registry.npmjs.org registry.npmjs.org:443
    npm ERR! network This is a problem related to network connectivity.
    npm ERR! network In most cases you are behind or have bad network settings.
    npm ERR! network
    npm ERR! network If you are behind a proxy, please make sure that the
    npm ERR! network 'proxy' config is set properly. See: 'npm help config'

Spróbuj jedno z następujących:

Tymczasowe rozwiązanie na linux: **add 104.16.20.35 registry.npmjs.org to /etc/hosts file**

lub

.. code:: bash

    npm config set registry http://registry.npmjs.org
    
    
Instalacja - windows komputery na UAM
------------------------------------------

Musisz zainstalować pakiety (najlepiej na dysku poligon).

.. code:: bash

    P:
    
    mkdir s[numer_indeksu]
    
    cd s[numer_indeksu]

Pobierz kod z repozytorium Git do utworzonego katalogu i uruchom

.. code:: bash
    
    npm install
    
    npm start
    
Musisz mieć **Node v8.0.0** na lokalnym komputerze programistycznym, aby uruchomić json-server, uruchom server imitujący backend w osobnym terminalu

.. code:: bash

    json-server --watch db.json --port 8080
    
Aplikacja będzie dostępna pod adresem **localhost: 3000**, serwer będzie działał pod adresem **localhost: 8080**.

Aplikacja jest przebudowywana na żywo, podczas każdej zmiany w plikach źródłowych. Wszystko, co musisz zrobić, to zapisać plik, a zmiany zostaną natychmiast zastosowane.

React
-------------

React to deklaratywna biblioteka JavaScript do budowania interfejsów użytkownika. Pozwala budować złożone interfejsy użytkownika z małych i odizolowanych fragmentów kodu zwanych „komponentami”. React może służyć jako baza przy tworzeniu aplikacji single page lub mobilnych. React jako framework zajmuje się tylko zarządzaniem stanem i renderowaniem stanu do DOM. Document Object Model (DOM) to programistyczny interfejs API dla dokumentów HTML i XML. Definiuje logiczną strukturę dokumentów oraz sposób uzyskiwania dostępu do dokumentu i manipulowania nimi.
Z racji tego, że React odpowiada tylko za zmiany w modelu DOM, tworzenie aplikacji React zwykle wymaga użycia dodatkowych bibliotek do routingu i zarządzania stanem aplikacji. 

React używa wirtualnego Document Object Model lub wirtualnego DOM, tworząc pamięć podręczną struktury danych w pamięci, obliczając powstałe różnice, a następnie wydajnie aktualizując wyświetlany DOM przeglądarki. Pozwala to programiście na pisanie kodu tak, jakby cała strona była renderowana przy każdej zmianie, podczas gdy biblioteki React renderują tylko te podkomponenty, które faktycznie się zmieniają.


Project structure
-------------------

Zależności naszego projektu są przechowywane w pliku **package.json**.

Plik package.json pełni tę samą rolę, co pom.xml w projektach Maven.

Sekcja Skripts definiuje zestaw skryptów node, które możesz uruchomić. Te skrypty są aplikacjami wiersza poleceń. Możesz je uruchomić, wywołując npm run XXXX lub yarn XXXX, gdzie XXXX to nazwa polecenia. Przykład: *npm run build*.

package.json zachowuje składnie json. Najważniejsze dla nas elementy znajdują się pod tagiem **dependencies**. 

Instalacja pakietu przy użyciu npm lub yarn:

.. code:: bash

    npm install <PACKAGENAME>
    yarn add <PACKAGENAME>

taki pakiet jest automatycznie wstawiany do listy zależności.

Wersje pakietu:

W powyższym opisie widziałeś numery wersji takie jak: **~3.0.0** lub **^0.13.0**. Co one oznaczają i jakich innych specyfikatorów wersji możesz użyć?

Te symbole określają, które aktualizacje twój pakiet akceptuje. Biorąc pod uwagę, że przy użyciu semver (wersjonowania semantycznego) wszystkie wersje mają 3 cyfry, pierwsza to wydanie główne, druga wydanie podrzędne, a trzecia to wydanie poprawki, obowiązują następujące zasady:

	| ~: jeśli piszesz ~0.13.0, chcesz aktualizować tylko wydania poprawek: 0.13.1 jest w porządku, ale 0.14.0 nie.
	| ^: jeśli piszesz ^0.13.0, chcesz zaktualizować łatkę i mniejsze wydania: 0.13.1, 0.14.0 i tak dalej.
	| \*: jeśli napiszesz \*, oznacza to, że akceptujesz wszystkie aktualizacje, w tym aktualizacje głównych wersji.
	| >: akceptujesz każdą wersję wyższą niż ta, którą określiłeś
	| >=: akceptujesz dowolną wersję równą lub wyższą niż ta, którą określiłeś
	| <=: akceptujesz dowolną wersję równą lub niższą od podanej
	| <: akceptujesz dowolną wersję niższą od określonej
    
są też inne zasady:

    | brak symbolu: akceptujesz tylko tę konkretną wersję, którą określisz
    | latest: chcesz użyć najnowszej dostępnej wersji
    
Pobrane zależności są przechowywane w folderze **node_modules** i nie powinny być elementem repozytorium kodu.

Kod jest przechowywany w folderze **src**.

Aby dodać nową zależność uruchom **npm install NAZWA_BIBLIOTEKI** w forlderze projektu. Zależność zostanie automatycznie dodana do pliku package.json.    
       
Javascript i Immutability
-----------------------------

Generalnie istnieją dwa podejścia do zarządzania danymi. Pierwsze podejście polega na "mutowaniu" danych poprzez bezpośrednią zmianę wartości danych. Drugie podejście polega na zastąpieniu danych nową kopią, która zawiera pożądane zmiany. Elementy React są immutable. Po utworzeniu elementu nie możesz zmienić jego dzieci ani atrybutów a jedynie podmienić cały obiekt na nowy.

Immutable dane pozwalają łatwo określić, czy dokonano zmian, co pomaga określić, kiedy komponent wymaga ponownego renderowania.

JSX
----

JSX lub JavaScript XML to rozszerzenie składni języka JavaScript. Podobny z wyglądu do HTML, JSX zapewnia możliwość renderowania komponentów przy użyciu znanej składni HTML.

Wyrażenia JavaScript (ale nie instrukcje) mogą być używane wewnątrz JSX z nawiasami klamrowymi **\{\}**:

.. code:: java

  <h1>{10+1}</h1>

Wyeneruje dla nas następujący HTML

.. code:: java

  <h1>11</h1>

Nie możemy korzystać z polecenia if then, ale możemy korzystać z operatorów logicznych (jeżeli pierwsza część jest prawdziwa wykonaj kolejną) i operatora ternarnego "?".

.. code:: java

    <div>
        <h1>{ i === 1 ? 'true' : 'false' }</h1>
        <h1>{ i === 1 && "I equals one" }</h1>
    </div>
    
      
Index
------

Aplikacje zbudowane za pomocą Reacta zwykle mają jeden **główny węzeł DOM**. Aby wyrenderować element React od głównego węzła DOM, przekaż komponent i element główny do ReactDOM.render():

.. code:: java

    ReactDOM.render( <TodoList />, document.getElementById('root') );
    

Komponenty react
-------------------

Komponenty to niezależne fragmenty kodu, które mogą być wielokrotnie użyte w aplikacji.

**Komponenty klasowe** 

Podczas tworzenia komponentu React nazwa komponentu musi zaczynać się od wielkiej litery.

Komponent musi zawierać instrukcję extends React.Component, która tworzy dziedziczenie po React.Component i daje Twojemu komponentowi dostęp do funkcji React.Component. 
Komponent wymaga posiadania metody render, która zwraca hierarchię widoków do wyświetlenia.

.. code:: java

    class TodoList extends React.Component {
        render() {
            return (
                <div className="TodoList">
                    <h1>Todo List {this.props.name}</h1>
                    <ul>
                        <li>Learn React</li>
                        <li>Pass programming laboratory</li>
                        <li>Have a nice holiday</li>
                    </ul>
                </div>
            );
        }
        
        export default TodoList;

    }
    
React czerpie swoją siłę w ponownym wykorzystaniu kodu, sensowne jest więc umieszkanie komponentów w osobnych plikach. Zauważ, że plik musi zaczynać się od zaimportowania Reacta i kończyć się instrukcją *export default TodoList;*. Czyli udostępnienia go dla innych komponentów do użytku.
    
Kiedy już zdefiniujemy komponent, możemy teraz wyrenderować go w innym komponencie, pisząc *<TodoList />*. Każdy komponent tworzy zamkniętą całość i może działać niezależnie; pozwala to na budowanie złożonych interfejsów użytkownika z prostych komponentów.    
    
**Komponenty funkcyjne**

W React komponenty funkcyjne są bardziej zwinnym sposobem na pisanie komponentów, zawierają one tylko metodę render i nie mają własnego stanu. Możemy napisać funkcję, która pobiera props jako dane wejściowe i zwraca to, co powinno zostać wyrenderowane.

.. code:: java

    function Todo() {
        return (
            <li className="todo" >
                Have a nice holidays
            </li>
        );
    }

    export default Todo;

.. class:: tag

    Exercise
    
Dodaj Todo component do TodoList

Style css
--------------

Style css możemy dodawać na pare sposobów:
    
    | jako osobne pliki
    | inline w kodzie komponentu
 
.. code:: java

    const greenStyle = {
        color: 'green',
    };    
    
     <li style={greenStyle}>Learn React</li>

or 

    | jako stylowane komponenty 
    
Utwórz zmienną, wybierając konkretny element html, w którym przechowujemy nasze klucze stylów

.. code:: java

    const Div = styled.htmlElement`color: pink`

Następnie używamy nazwy naszej zmiennej jako opakowania *<Div></Div>*, tak jakbyśmy używali komponentu reakcji.    

    
.. code:: java

    const Undone = styled.p`
        color: red,
    `;

    <Undone>Pass programming laboratory</Undone>
    
Pamiętaj, że nazwy komponentów stylizowanych muszą zaczynać się **wielką literą**.

Cykl życia komponentu
-----------------------

Cykl życia komponentu można podzielić na 4 części:

    | Mounting —  instancja komponentu jest tworzona i wstawiana do DOM.
    | Updating — gdy komponent React narodzi się w przeglądarce i będzie się rozwijał, otrzymując nowe aktualizacje.
    | Unmounting — składnik nie jest potrzebny i zostaje odmontowany.
    | Obsługa błędów  — wywoływana, gdy wystąpi błąd podczas renderowania, w metodzie cyklu życia lub w konstruktorze dowolnego komponentu podrzędnego.

.. class:: center
	
	|col|
	
.. |col| image:: reactLifecycle.png	

Metody cyklu życia używają wyzwalaczy, które umożliwiają wykonanie kodu w ustalonych punktach podczas życia komponentu:

    | **shouldComponentUpdate** pozwala programiście zapobiec niepotrzebnemu ponownemu renderowaniu komponentu przez zwrócenie wartości false, jeśli renderowanie nie jest wymagane.
    | **componentDidMount** jest wywoływana po „zamontowaniu” komponentu (komponent został utworzony w interfejsie użytkownika, często przez powiązanie go z węzłem DOM). Jest to powszechnie używane do wyzwalania ładowania danych ze zdalnego źródła za pośrednictwem interfejsu API.
    | **componentWillUnmount** jest wywoływany bezpośrednio przed usunięciem lub „odmontowaniem” komponentu. Jest to powszechnie używane do czyszczenia wymagających zasobów zależności od komponentu, które nie zostaną po prostu usunięte wraz z odmontowaniem komponentu (np. usunięcie wszelkich instancji setInterval(), które są powiązane z komponentem lub "eventListener" ustawionego na komponencie)
    | **renderowanie** to najważniejsza metoda cyklu życia i jedyna wymagana w każdym komponencie. Zwykle jest wywoływana za każdym razem, gdy stan komponentu jest aktualizowany, co powinno znaleźć odzwierciedlenie w interfejsie użytkownika.       

Lifecycle methods
-------------------

React ma cztery wbudowane metody, które są wywoływane w tej kolejności podczas montowania komponentu:

    | constructor()
    | getDerivedStateFromProps()
    | render()
    | componentDidMount()
    
Metoda getDerivedStateFromProps() jest wywoływana tuż przed wyrenderowaniem elementów w DOM. Jest to naturalne miejsce do ustawienia obiektu stanu na podstawie początkowych właściwości. Również przy aktualizacjach wywoływana jest metoda getDerivedStateFromProps. Jest to pierwsza metoda wywoływana po zaktualizowaniu składnika. 
    

Przekazywanie danych przez Props 
----------------------------------

Komponent przyjmuje parametry zwane **props** (skrót od „properties”). Dostęp do props można uzyskać za pomocą zmiennej **this.props**.

Definiując komponent do renderowania możemy przekazać wartość w definicji komponentu. Nazwa parametrów powinna być w tym wypadku zgodna z nazwą właściwości, którą zdefiniowaliśmy w komponencie *TodoList*.

.. code:: java

    class Lists extends React.Component {
        render() {
            return <TodoList name="My List" />;  
            }
    }

    class TodoList extends React.Component {
        render() {
            return (
            <div className="todoList">
                <h1>Todo List {this.props.name}</h1>
                <ul>
                    <Todo/>
                    <Todo/>
                    <Todo/>
                </ul>
            </div>
        );
        }
    }
    
Props są własnościami **read-only** i nie mogą być modyfikowane.    
 
.. class:: tag

    Exercise
    
Dodaj listę jako najbardziej ogólny (nadrzędny) komponent.
    
State (stan)
-------------

Chcemy mieć możliwość dodawania i zapamiętywania zadań todo do wykonania. Aby „zapamiętać” rzeczy, komponenty używają tzw. stanu. Komponenty Reacta mogą mieć stan, ustawiając this.state w swoich konstruktorach. Stan powinien być uważany za prywatny dla komponentu React, w którym jest zdefiniowany.

Dostęp do stanu konstruktora można uzyskać za pomocą zmiennej **this.state**.

**Nie modyfikuj stanu bezpośrednio** bezpośrednia zmiana stanu nie spowoduje ponownego renderowania komponentu:

.. code:: java

    // Wrong
    this.state.nr = 0;
    this.state.todosList.push({ name : "List", elements = [ "learnReact"] });

Zamiast tego korzystaj z metody setState():

.. code:: java
    
    // Correct 
    newelement = { name : "List", elements = [ "learnReact"] };
    this.setState(prevState => ({
        number : 0;
        todosList : [...prevState.todosList, newelement]
    }))
    
Zmiany stanu są wykonywane asynchronicznie, więc musisz być świadomy możliwych implikacji tego zachowania i nie zakładaj, że jeden setState zostanie wykonany przed innym (i przed następną linią w kodzie!!).

setState zmienia tylko wartość podanej zmiennej, pozostawiając inne zmienne stanu nienaruszone, więc nie trzeba ustawiać całego stanu w każdej komendzie setState.

Jedynym miejscem, w którym możesz bezpośrednio przypisać **this.state** jest **konstruktor**.

Stan nie jest dostępny dla żadnego komponentu innego niż ten, który go posiada i ustawia. Aby zebrać dane od wielu elementów podrzędnych lub aby dwa komponenty podrzędne komunikowały się ze sobą, musisz zamiast tego zadeklarować stan współdzielony w ich komponencie nadrzędnym. Komponent rodzica może przekazać stan z powrotem do dzieci za pomocą props; dzięki temu komponenty podrzędne są zsynchronizowane ze sobą oraz z komponentem nadrzędnym. W celu przekazania wartości od dziecka do rodzica używamy funkcji - wtedy rodzic przekazuje funkcję jako props do dziecka, gdy dziecko wykonuje funkcję, jest ona wykonywana na rodzicu z  dostępu do stanu rodzica.
    
Konstruktor
--------------

.. class:: important
    
    W klasach JavaScript musisz zawsze wywoływać super podczas definiowania konstruktora podklasy. Wszystkie klasy komponentów React, które mają konstruktor, powinny zaczynać się od wywołania super(props).

.. code:: java

    constructor(props) {    
        super(props);    
        this.state = { todosList: [] }; 
    }    
    
.. class:: tag

    Exercise
    
Dodaj konstruktor i stan do TodoList

.. code:: java

    class TodoList extends React.Component {
        constructor(props) {
            super(props);
            let t1 = { value : "Learn React", done : true };
            let t2 = { value : "Pass Programming Laboratory", done : false };
            let t3 = { value : "Have a nice holiday", done : false };
            this.state = { todosList: [t1, t2, t3] };
        }


        render() {

            const {todosList} = this.state;

            let todos = todosList.map( todo => {
                return (<ul>
                    <Todo value = {todo.value}
                            done = {todo.done}   />
                    </ul>);
            })

            return (
                <div className="TodoList">
                    <h1>Todo List {this.props.name}</h1>
                    {todos}
            </div>
            );  
        }   
    }
    
    export default TodoList;
    
Zdarzenia
-----------

W React możemy wykonywać zdarzenia HTML.

.. code:: java

    constructor(props) {
    // This binding is necessary to make `this` work in the callback    
    this.addTodo = this.addTodo.bind(this);  
    }
    
    addTodo = () => {
        let newelement = { value : "new", done : false };
        this.setState(prevState => ({
            todosList : [...prevState.todosList, newelement]
        }));
    };
    
    <button onClick={this.addTodo}>  
        AddTodo
    </button>

Gdzie addTodo to funkcja reakcji. Pamiętaj, aby powiązać funkcję, gdy jest zdefiniowana, jeśli zapomnisz powiązać (bind) this.addTodo i przekazać ją do onClick, będzie to niezdefiniowane, gdy funkcja zostanie faktycznie wywołana. Alternatywnie możesz użyć **arrow function** w wywołaniu zwrotnym:

.. code:: java

    constructor(props) {
    
    }
    
    addTodo = () => {
        let newelement = { value : "new", done : false };
        this.setState(prevState => ({
            todosList : [...prevState.todosList, newelement]
        }));
    };
    
    <button onClick={() => this.addTodo()}>  
        AddTodo
    </button>
    
Problem z tą składnią polega na tym, że za każdym razem, gdy komponent jest renderowany, tworzone jest inne wywołanie zwrotne, co może wymusić dodatkowe ponowne renderowanie.

Jeśli chcesz zapobiec domyślnemu zachowaniu zdarzenia HTML, musisz wykonać metodę PreventDefault().

.. code:: java

    function ActionLink() {
        function handleClick(e) {    
            e.preventDefault();    
            console.log('The link was clicked.');  
        }
        
        return (
            <a href="#" onClick={handleClick}> Click me </a>
        );
    }
    
.. class:: tag

    Exercise
    
Dodaj nowy element Todo po kliknięciu przez użytkownika.

React Listy i klucze
---------------------

Listy są ważnym aspektem Twojej aplikacji. Każda aplikacja musi korzystać z list w takiej czy innej formie. W React, gdy używasz list, każdy element listy wymaga unikalnego klucza.
Klucze są niezbędne do poprawy wydajności aplikacji React. Klucze pomagają React określić, które elementy zostały zmienione (dodane/usunięte/zmienione). Aby nadać unikatową tożsamość każdemu elementowi w tablicy, wymagany jest klucz.

.. code:: java

    <ul key = {todo.id}>
        
.. class:: tag

    Exercise
    
Skopiuj i przeanalizuj następujący kod:

.. code:: java

    class TodoList extends React.Component {
        constructor(props) {
            super(props);
            let t1 = { id : 0, value : "Learn React", done : true };
            let t2 = { id : 1, value : "Pass Programming Laboratory", done : false };
            let t3 = { id : 2, value : "Have a nice holiday", done : false };
            this.state = { todosList: [t1, t2, t3] };
            this.addTodo = this.addTodo.bind(this);
            this.counter = 2;
        };


        addTodo = () => {
            this.counter++;
            let newelement = { id: this.counter, value : "new", done : false };
            this.setState(prevState => ({
                todosList : [...prevState.todosList, newelement]
            }));
        };

        handleRemove = id => {
            let arrAfterDel = this.state.todosList.filter(function(item) {
                return item.id !== id
            });
            this.setState({todosList : arrAfterDel});
        }

        render() {
    
            const {todosList} = this.state;
    
            let todos = todosList.map( todo => {
                return (<ul key = {todo.id}>
                            <Todo value = {todo.value}
                                done = {todo.done}   />
                            <button type="button" onClick={() => this.handleRemove(todo.id)}>
                                Remove
                            </button>
                    </ul>);
            })

            return (
                <div className="TodoList">
                    <h1>Todo List {this.props.name}</h1>
                    {todos}
                    <button onClick={this.addTodo}>
                        AddTodo
                    </button>
                </div>
            );
        }
    }

    export default TodoList;    

Zauważ, że musimy użyć globalnego licznika zmiennych w celu dodania unikalnych identyfikatorów do obiektu. Ta wartość będzie żyć z komponentem. Moglibyśmy użyć stanu do zapisania licznika, ale pamiętaj, że zmiany stanu powodują ponowne renderowanie i nie jest to w tym przypadku potrzebne.

Zastosowanie cyklu życie komponentu
-------------------------------------   

.. class:: tag

    Exercise
    
Ustaw done jako element stanu klasy Todo i dodaj przycisk, który ustawia Todo na gotowe

.. code:: java

    import React from 'react';

    const greenStyle = {
        color: 'green',
    };

    const redStyle = {
        color: 'red',
    };


    class Todo extends React.Component {
        constructor(props) {
            super(props);
            this.setDone = this.setDone.bind(this);
            this.state = {done: null};
        }

        static getDerivedStateFromProps(props, state) {
            if (state.done === null)
                return {done: props.done}; else return {};
        }

        setDone = () => {
            if (this.state.done) {
                this.setState({done: false});
            } else {
                this.setState({done: true});
            }
        }

        render() {

            const {value} = this.props;
            const {done} = this.state;
    
            return (
                <div>
                    {done === true ?
                        <li style={greenStyle}>
                            {value}
                        </li> :
                        <li style={redStyle}>
                            {value}
                        </li>}
                    <button onClick={this.setDone}>
                        Change status
                    </button>
                </div>
            )

        };
    }

    export default Todo;
    
Oczywiście wadą tego rozwiązania jest to, że komponent nadrzędny nie wie o zmianie stanu komponentu potomnego.

Dodaj funkcję do właściwości komponentu potomnego, która zaktualizuje dane. W TodoList zdefiniuj:   

.. code:: java

    updateChild = (id, done) => {
        let arrAfterUpdate = this.state.todosList.map(function (item) {
            if(item.id === id) item.done = done;
            return item;
        });
        this.setState({todosList: arrAfterUpdate});
        console.log(arrAfterUpdate);
    };
    
w render dodaj :    

.. code:: java

      <Todo value={todo.value}
                      done={todo.done}
                      id = {todo.id}
                      update={(id, done) => this.updateChild(id, done)}  />

Wywołaj it in the Todo.js

.. code:: java

    setDone = () => {
        if (this.state.done) {
            this.setState({done: false}, this.props.update(this.props.id, !this.state.done));
        } else {
            this.setState({done: true}, this.props.update(this.props.id, !this.state.done));
        }

    }

Pamiętaj, że setState jest asynchroniczny, więc nie możemy tego zrobić w taki sposób

.. code:: java

        if (this.state.done) {
            this.setState({done: false});
        } else {
            this.setState({done: true});
        }
        this.props.update(this.props.id, this.state.done)

jako że prawdopodobnie stan zostanie zaktualizowany **po**, wykonaniu funkcji aktualizacji. Dlatego używamy funkcji zwrotnej (callback), która jest drugim argumentem funkcji setState i jest wykonywana po zakończeniu setState.    

Debugging
-----------

Możesz debugować i sprawdzać błędy w aplikacji React za pomocą przeglądarki. W programie firefox kliknij prawym przyciskiem myszy i wybierz opcję inspekcji elementu.

W zakładce konsoli można znaleźć błędy zwracane przez kod javascript.

W zakładce debugger możesz debugować aplikację. Kliknij kartę Debuger, kliknij **ctrl + p**, aby wybrać plik Todo.js. Ustaw punkt przerwania i kliknij na stronie. Sprawdź wartość zmiennych i sposób debugowania.

.. class:: center
	
	|col1|
	
.. |col1| image:: reactDebug.png	
    
Input fields
-------------

Formularz w React dodajesz jak każdy inny element. Dane są obsługiwane przez komponenty, wszystkie dane są przechowywane w stanie komponentów. Możesz kontrolować zmiany, dodając obsługę zdarzeń w atrybucie onChange.

.. class:: tag

    Exercise
    
Zezwalaj użytkownikowi na dodawanie todo za pomocą pola input field

Add to TodoList:

.. code:: java

    myChangeHandler = (event) => {
        this.setState({newTodo: event.target.value});
    }

    ...
    render() {
    ...
    return (
            <div className="TodoList">
                <h1>Todo List {this.props.name}</h1>
                {todos}
                <p> My new todo </p>
                <input
                    type='text'
                    onChange={this.myChangeHandler}
                />
                <button onClick={this.addTodo}>
                    AddTodo
                </button>
            </div>
        );
        
.. class:: tag

    Exercise
    
Przepisz wartość ze stanu do nowo tworzonego wpisu Todo (jako jego value).

Czyść w stanie pole tekstowe po dodaniu elementu.        

oraz dodaj w input 

.. code:: java

	value = {this.state.newTodo}

Zapytania http
--------------------

Naszym nadrzędnym celem jest, aby nasza aplikacja działała razem z serwerem json działającym na porcie 8080.

W tym celu użyjemy biblioteki, która nazywa się axios. Axios to lekki klient HTTP.

Dodaj do "package.json"

.. code:: java

    "devDependencies": {
      "axios": "^0.24.0"
    },
    
:badimportant:`Uwaga! najnowsza werjsa Axiosa nie działa z kodem z repozytorium więc ustawianie takiej wersji biblioteki jest konieczne!!`

Dodaj import do komponentu TodoList:

.. code:: java

    import axios from 'axios';
    

Pobierz wszystkie elementy z serwera i zapisz je jako todos na componentMount:
    
.. code:: java

    componentDidMount() {
        axios.get(`http://localhost:8080/todos`)
            .then(res => {
                const todosList = res.data;
                this.setState({ todosList });
            })
    }
    
W celu aktualizacji elementu na serwerze wykorzystujemy metodę PUT:

.. code:: java

    updateChild = (id, done) => {
        let arrAfterUpdate = this.state.todosList.map(function (item) {
            if(item.id === id) item.done = done;
            return item;
        });

        let object = arrAfterUpdate.find(function (item) {
            if(item.id === id) return item;
        });

        this.setState({todosList: arrAfterUpdate}, () => axios.put(`http://localhost:8080/todos/${object.id}`, object));

        console.log(arrAfterUpdate);
    };

POST by przesłać obiekt do serwera:

.. code:: java

   addTodo = () => {
        let nextId = this.state.todosList.map(a => { return a.id }).reduce((acc, val) => {
            return acc > val ? acc : val;
        });
        nextId++;
        let newelement = {id: nextId, value: this.state.newTodo, done: false};
        this.setState(prevState => ({
            todosList: [...prevState.todosList, newelement],
            newTodo: ""
        }), () => axios.post(`http://localhost:8080/todos/`, newelement));
    };
    
DELETE by usunąć obiekt:

.. code:: java

    handleRemove = id => {
        let object = this.state.todosList.find(function (item) {
            if(item.id === id) return item;
        });
        let arrAfterDel = this.state.todosList.filter(function (item) {
            return item.id !== id
        });
        this.setState({todosList: arrAfterDel}, () => axios.delete(`http://localhost:8080/todos/${object.id}`, object));
    }

Styling
--------------

Chcielibyśmy dodać do naszego projektu tabelę Bootstrap.

Render oczekuje, że zwracany oiekt będzie opakowujący w pojedynczy tag główny. Ale czasami nie chcesz mieć tego w swoim kodzie. W takim przypadku możesz użyć elementu React.Frament symulujący takie zachowanie.

.. code:: bash

    npm install bootstrap

Dodaj do Todo.js class:

.. code:: bash

    import 'bootstrap/dist/css/bootstrap.min.css';
 
.. code:: java

            <React.Fragment>
                {done === true ?
                    <th style={greenStyle}>
                        {value}
                    </th> :
                    <th style={redStyle}>
                        {value}
                    </th>}
                <th>
                    <button onClick={this.setDone}>
                        Change status
                    </button>
                </th>
            </React.Fragment>

Dodaj elementy tabeli bootstrap do głównej klasy:

.. code:: java
    
    render() {

        const {todosList} = this.state;

        let todos = todosList.map(todo => {
            return (<tr key={todo.id}>
                <Todo value={todo.value}
                      done={todo.done}
                      id = {todo.id}
                      update={(id, done) => this.updateChild(id, done)}  />
                <th>
                    <button type="button" onClick={() => this.handleRemove(todo.id)}>
                    Remove
                    </button>
                </th>
            </tr>);
        })

        return (
            <div className="TodoList">
                <h1>Todo List {this.props.name}</h1>
                <table className="table table-striped">
                    <thead className="thead-dark">
                    <th scope="col">Todo</th>
                    <th scope="col">Status</th>
                    <th scope="col"></th>
                    </thead>
                    <tbody>
                        {todos}
                    </tbody>
                </table>
                <p> My new todo </p>
                <input
                    type='text'
                    onChange={this.myChangeHandler}
                    value = {this.state.newTodo}
                />
                <button onClick={this.addTodo}>
                    AddTodo
                </button>
            </div>
        );
    }

Zobacz na wynik.

Tests
-------

Aby uruchomić test w TodoList.test.js musimy stworzyć nową konfigurację uruchomienia w WebStorm.

Wybierz plus i wybierz **Jest**, w oknie otwartym w opcjach *Jest options* wpisz **--env=jsdom**.

Więcej o testach można przeczytać na


    | https://jestjs.io/docs/en/tutorial-react
   
.. [*] Used materials from :

https://projects.wojtekmaj.pl/react-lifecycle-methods-diagram/

https://reactjs.org/tutorial/tutorial.html

https://codeburst.io/4-four-ways-to-style-react-components-ac6f323da822

https://en.wikipedia.org/wiki/React_(web_framework)

https://reactjs.org/docs/getting-started.html

https://medium.com/@krishankantsinghal/package-json-understanding-it-for-your-nodejs-reactjs-angularjs-or-any-javascript-app-which-use-5a18de90d33

https://adhithiravi.medium.com/why-do-i-need-keys-in-react-lists-dbb522188bbb

https://www.w3schools.com/react/react_lifecycle.asp

https://www.netguru.com/codestories/react-native-lifecycle
