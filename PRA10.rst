
=======================
Programming Laboratory
=======================

--------------------
React Hooks
--------------------

.. class:: important 

    .. class:: important 

    Uwaga! cały kod znajduje się na gałęziach **ReactHooksStart** i **ReactHooksEnd**  w repozytorium https://github.com/WitMar/PRA2025 .
       
Jeżeli nie widzisz odpowiednich gałęzi na GitHubie wykonaj **Ctr+T**, a jak to nie pomoże to wybierz z menu **VCS->Git->Fetch**. 

Różnice między klasowymi a funkcyjnymi komponentami
======================================================

React używa tej samej instancji komponentu Class pomiędzy ponownymi renderowaniami. Oznacza to, że w naszym kodzie obiekt *this* odnosi się do tej samej instancji. W związku z tym działając asynchronicznie możemy zmieniać wartości tej klasy zanim dane operacje zakończą swoje działanie, co może prowadzić do błędów w naszej aplikacji.

W przypadku funkcji react uruchamia całe funkcje za każdym rerenderem, w związku z tym nie ma możliwości wystąpienia tego błędu. Dotychczas jednak kłopotem było to, że w takim modelu nie mogliśmy zapisywać żadnych danych (stanu) pomiędzy wywołaniami funkcji.
Z pomoc przychodzą nam tzw hooki.

**"React simply calls your function components over and over again when it needs to render it. You’ll need to use React Hooks to store state and plug into the React render lifecycle. And thanks to JavaScript Closures, your variables are scoped to the specific function call.”**

Hooks
=======

Hooks są dostępne w Reactie od wersji v16.8.0. React Hooks to proste funkcje JavaScript, których możemy użyć do oddzielenia funkcji przechowujących elementy wielokrotnego wykorzystania (jak stan) od komponentu funkcyjnego. 

Zauważysz, że nasz prosty komponent funkcyjny StateExample nie ma nad sobą żadnej kontroli. Poza tym tak naprawdę nie możemy nic zrobić w odniesieniu do cyklu życia renderowania w React, jak w przypadku komponentu klasowego. 
Tutaj właśnie pojawiają się Hooki! 

Główną zmianą, którą musisz wprowadzić w rozumieniu, jest to, że w przeciwieństwie do komponentów klasowych, komponenty funkcyjne są uruchamiane podczas każdego renderowania.

Hooki to funkcje, które pozwalają „podczepić się” do funkcji stanu i cyklu życia React (mount, unmount, render) w kodzie komponentów funkcyjnych. Hooki nie działają wewnątrz klas — pozwalają używać Reacta bez komponentów klasowych.

Hooki nie zastąpią Twojej wiedzy na temat podstawowych mechanizmów Reacta. Zamiast tego Hooki zapewniają bardziej bezpośredni interfejs API dla własności komponentów React, które już znasz: właściwości, stan, kontekst, referencje i cykl życia. 
Hooki oferują także nowy, potężny sposób ich łączenia.

Pamiętasz na przykładzie komponentów klasowych problem ze współdzieleniem informacji o stanie między komponentami.
Dzięki hookom możesz wyodrębnić logikę stanową z komponentu, dzięki czemu można go niezależnie przetestować i ponownie wykorzystać. Hooki umożliwiają ponowne wykorzystanie logiki stanowej bez zmiany hierarchii komponentów.

Zasady hooków:

	| Wywołuj Hooki tylko na najwyższym poziomie. Nie wywołuj hooków wewnątrz pętli, warunków i funkcji zagnieżdżonych.
	| Nazwy hooków zaczynają się od słowa **use**
	| Wywołuj hooki tylko z komponentów funkcji React. Nie wywołuj hooków ze zwykłych funkcji JavaScript. 
	| Hooki nie mogą być warunkowe.
	| Hooki muszą być wykonywane w tej samej kolejności na każdym renderowaniu

Poniższa operacja jest niedozwolona:

.. code:: javascript
	
	const [value, setValue] = useState(1);
	const [doubleValue, setDoubleValue] = useState(1);
  
	if (value > 5) {
		useEffect(() => setDoubleValue(value * 2),[value]);
	}
	
i powoduje błąd "Uncaught Error: Rendered more hooks than during the previous render." - hook warunkowy.	

State Hooks 
-------------

Stan pozwala komponentowi „zapamiętać” informacje, takie jak dane wprowadzone przez użytkownika. Na przykład komponent formularza może używać stanu do przechowywania wartości wejściowej.

.. code:: javascript

	import React, { useState } from 'react';
	function Example() {
		// Declare a new state variable, which we'll call "count"  
		
		const [count, setCount] = useState(0);
		
		return (
			<div>
			<p>You clicked {count} times</p>
			<button onClick={() => setCount(count + 1)}>
				Click me
			</button>
			</div>
		);
	}

Aby dodać stan do komponentu, użyj jednego z tych hooków:

     | **useState** deklaruje zmienną stanu, którą możesz bezpośrednio zaktualizować.
     | **useReducer** deklaruje zmienną stanu z logiką aktualizacji wewnątrz funkcji redukującej (nie bedziemy opisywać tego hooka w tych materiałach).
     
.. code:: javascript

	import React, { useReducer } from 'react';

	function reducer(state, action) {
		switch (action.type) {
			case 'increment':
				return state + 1;
			default:
				return state;
		}
	}

	function Example() {
		const [count, dispatch] = useReducer(reducer, 0);

		return (
			<div>
			<p>You clicked {count} times</p>
			<button onClick={() => dispatch({ type: 'increment' })}>
				Click me
			</button>
			</div>
		);
	}
     
     
Tutaj useState jest hookiem. Wywołujemy go wewnątrz komponentu funkcyjnego, aby dodać do niego jakiś stan lokalny. React zachowa ten stan pomiędzy ponownymi renderowaniami jak w przypadku komponentu klasowego. 

Co zwraca useState? Zwraca parę wartości: bieżący stan i funkcję, która go aktualizuje. Dlatego piszemy **const [count, setCount] = useState()**. Działa to podobnie do this.state.count i this.setState w klasie, z tą różnicą, że otrzymujesz je w parze. 
Możesz też nazwać tę funkcję jak chcesz. 

Uwaga! W przypadku hooka nic nie łączy kolejnych stanów, więc trzeba zawsze definiować pełny stan!

.. code:: javascript

	const [user, setUser] = useState({ name: 'Anna', age: 30 });

Jeśli zrobisz:

.. code:: javascript

	setUser({ name: 'Kasia' });

To age zostanie usunięte, ponieważ setUser zastępuje cały obiekt, a nie scala go automatycznie.

Jedynym argumentem useState jest stan początkowy. W powyższym przykładzie jest to 0, ponieważ nasz licznik zaczyna się od zera.
Zauważ, że w przeciwieństwie do this.state, stan tutaj nie musi być obiektem — chociaż może nim być, jeśli chcesz. Argument stanu początkowego jest używany tylko podczas pierwszego renderowania.

Możemy definiować wiele wartości stanu jednocześnie, by to zrobić będziemy wywoływać funkcję useState wielokrotnie:

.. code:: javascript

	function Car() {
		const [brand, setBrand] = useState("Fiat");
		const [model, setModel] = useState("126p");
		const [year, setYear] = useState("1964");
		const [color, setColor] = useState("red");
		
Możemy też po prostu użyć jednego stanu i zamiast tego dołączyć obiekt:

.. code:: javascript
	
	function Car() {
		const [car, setCar] = useState({
			brand: "Fiat",
			model: "126p",
			year: "1964",
			color: "red"
	});
	
Domyślnie zaleca się by korzystać z:

.. code:: javascript
	
	const updateColor = () => {
		setCar(previousState => {
			return { ...previousState, color: "blue" }
		});
	}

React zakłada, że jeśli wywołujesz useState wiele razy, robisz to w tej samej kolejności podczas każdego renderowania.

.. class:: tag

    Zadanie
    
Uruchom przykład z hookiem useState.

Effect Hooks
--------------

Hook effect, useEffect, dodaje możliwość wykonywania efektów ubocznych (zmieniających stan wokół komponentu) z komponentu funkcyjnego. Służy temu samemu celowi, co **componentDidMount, componentDidUpdate i componentWillUnmount** w klasach React, ale jest zunifikowany w jednym API.

.. code:: javascript

	useEffect(() => {    
		// Update the document title using the browser API   
		document.title = `You clicked ${count} times`;  
	});

Kiedy wywołujesz **useEffect**, mówisz Reactowi, aby uruchomił funkcję „efektu” po dodaniu zmian do DOM. Efekty są deklarowane wewnątrz komponentu, dzięki czemu mają dostęp do jego właściwości i stanu. 
Domyślnie React uruchamia efekty po każdym renderowaniu — łącznie z pierwszym renderowaniem.

Podobnie jak w przypadku useState, w komponencie możesz użyć więcej niż jednego efektu. Domyślnym zachowaniem efektów jest uruchamianie efektu po każdym ukończonym renderowaniu. W ten sposób efekt jest zawsze odtwarzany, jeśli tylko zmieni się jedna z jego zależności.

Aby to zaimplementować, przekaż drugi argument do useEffect, który jest tablicą wartości, od których zależy efekt. Nasz zaktualizowany przykład wygląda teraz tak:

Podany effect wywoła się tylko raz

.. code:: javascript

	useEffect(() => {
		//Runs only on the first render
	}, []);

Podany efekt wywoła się przy każdej zmianie wartości "props.source":

.. code:: javascript

	useEffect(
		() => {
			const subscription = props.source.subscribe();
			return () => {
				subscription.unsubscribe();
			};
		},
	[props.source],
	);
	
Wykorzystując useEffect możemy użyć czegoś, co nazywa się czyszczeniem. Służy do tego funcja wykonywana po return (czyli w momencie niszczenia hooka) i wykorzystywana jest głównie np do czyszczenia listenerów.

.. code:: javascript

	useEffect(() => {
		console.log("side effect 1", count);
		return () => {
		console.log("DESTROYED 1");
		};
	});


.. class:: tag

    Zadanie
    
Dodaj effect hook do komponentu zliczający liczbę odświeżeń komponentu setState, zobacz jego działanie.

.. class:: tag

    Zadanie
    
Sprawdź podany w rozdziale hooks błąd wykonania effect w przypadku wykorzystania go w instrukcji warunkowej.

Custom Hooks
-------------

Niestandardowe hooki są bardziej konwencją niż funkcją. Jeśli nazwa funkcji zaczyna się od „use” i wywołuje inne hooki, mówimy, że jest to hook niestandardowy.

Stan każdego komponentu jest całkowicie niezależny. Hooki pozwalają na ponowne wykorzystanie logiki stanowej, a nie samego stanu. Tak naprawdę każde wywołanie Hooka ma całkowicie izolowany stan — możesz więc nawet dwukrotnie użyć tego samego niestandardowego Hooka w jednym komponencie.

.. class:: tag

    Zadanie
    
Dodaj własny hook, pamiętaj że jego nazwa musi zaczynać się od "use...". Spraw by hook zwracał napis "parzyste/nieparzyste" zależnie od parzystości licznika. 
Dodaj jego wyświetlanie do głównego komponentu App.

.. code:: javascript

	import { useEffect, useState } from 'react';

	function useCustomExample(counter) {
		const [word, setWord] = useState('Parzyste');

		useEffect(() => {
			if (counter % 2 === 0) {
			setWord('Parzyste');
		} else {
			setWord('Nieparzyste');
		}
	}, [counter]);

	return word;
	}

	export default useCustomExample;
	
Użycie:

.. code:: javascript
 
	const parity = useCustomExample(count);
 
.. code:: javascript
 
	<p class="indented">{parity}</p>	

Context hooks
--------------

Kontekst pozwala komponentowi odbierać informacje od odległych rodziców bez przekazywania ich jako props. Na przykład komponent najwyższego poziomu aplikacji może przekazać bieżący motyw interfejsu użytkownika do wszystkich komponentów poniżej, niezależnie od głębokości.

		| **useContext** odczytuje i subskrybuje kontekst.

.. code:: javascript

	function Button() {
		const theme = useContext(ThemeContext);
	// ...
	
Parametry:

     | SomeContext: Kontekst utworzony wcześniej za pomocą narzędzia createContext. Sam kontekst nie przechowuje informacji, reprezentuje jedynie rodzaj informacji, które możesz dostarczyć lub odczytać z komponentów.	

Aby określić wartość kontekstu, React przeszukuje drzewo komponentów i znajduje najbliższego dostawcę kontekstu powyżej dla tego konkretnego kontekstu.

.. class:: tag

    Zadanie

Zobacz implementację ThemeProvidera i jego użycie w index.js. Następnie dodaj to klasy app.js wywołanie zmiany stylu strony

.. code:: javascript

	import './App.css';
	import React from "react";
	import StateExample from "./StateExample/StateExample";
	import {ThemeContext} from "./ContextExample/ThemeProvider";
	import Form from "./Form/Form";

	function App() {
	
		const {theme, toggle, dark} = React.useContext(ThemeContext)
	
		return (
			<div className="App" style={{backgroundColor: theme.backgroundColor, color: theme.color}}>
				Test
				<StateExample/>
				<button
					type="button"
					onClick={toggle}
					style={{
						backgroundColor: theme.backgroundColor,
						color: theme.color,
						outline: 'none'
					}}	
				>
					Toggle to {!dark ? 'Dark' : 'Light'} theme
				</button>			
			</div>
		);
	}

	export default App;
	

Ref hook
-----------

Referencje pozwalają komponentowi przechowywać pewne informacje, które nie są używane do renderowania, takie jak węzeł DOM lub identyfikator limitu czasu. W przeciwieństwie do stanu, aktualizacja ref nie powoduje ponownego renderowania komponentu. Referencje są „ucieczką” od paradygmatu React. Są przydatne, gdy musisz pracować z systemami innymi niż React, takimi jak wbudowane interfejsy API przeglądarki.

     | **useRef** deklaruje ref. Można w nim przechowywać dowolną wartość, ale najczęściej służy do przechowywania węzła DOM.

.. code:: javascript

    const initialRenderTimeRef = useRef(new Date().toLocaleString());
	
Przykład:


.. code:: javascript

	import React, {useEffect, useRef, useState} from 'react';
	import useCustomExample from "./UseCustomExample";

	function StateExample() {
		const [count, setCount] = useState(0);
		const parity = useCustomExample(count);

		const initialRenderTimeRef = useRef(new Date().toLocaleString());

		useEffect(() => {
			console.log("side effect 1", count);
			return () => {
				console.log("DESTROYED 1");
			};
		});

		function refreshDate(param) {
			initialRenderTimeRef.current = new Date().toLocaleString();
		}

		return (
			<div>
				<p>You clicked {count} times</p>
				<p>Initial render time (stored in ref): {initialRenderTimeRef.current}</p>
				<p class="indented">
					<button onClick={() => setCount(count + 1)}>
						Click me
					</button>
					<button onClick={() => refreshDate()}>
						Refresh Time
					</button>
					<p></p>
					<p class="indented">{parity}</p>
				</p>
			</div>
		);
	}

export default StateExample;

Hook useRef może być również użyty do śledzenia wartości poprzedniego stanu. Dzieje się tak, ponieważ jesteśmy w stanie zachować wartości useRef pomiędzy renderowaniami.	

.. class:: tag

    Zadanie

Zobacz jak działa powyższy przykład
	
Memo hook
------------

Hook Memo zwraca zapamiętaną wartość.

	| **useMemo** przeliczy zapamiętaną wartość tylko wtedy, gdy zmieni się jedna z zależności. Ta optymalizacja pomaga uniknąć kosztownych obliczeń przy każdym renderowaniu.

Pamiętaj, że funkcja przekazana do **useMemo** działa podczas renderowania. Nie rób tam niczego, czego normalnie nie zrobiłbyś podczas renderowania. Na przykład skutki uboczne należą do useEffect, a nie useMemo.

.. code:: javascript

	const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);

React Hook Form
=================

React Hook Form to prosta biblioteka do tworzenia formularzy w React z łatwym dodawaniem walidacji dla pól.

.. code:: javascript

	import { useForm } from 'react-hook-form';

	function App() {
		const {
			register,
			handleSubmit,
			formState: { errors },
		} = useForm();

	return (
		<form onSubmit={handleSubmit((data) => console.log(data))}>
			<input {...register('firstName')} />
			<input {...register('lastName', { required: true })} />
			{errors.lastName && <p>Last name is required.</p>}
			<input {...register('age', { pattern: /\d+/ })} />
			{errors.age && <p>Please enter number for age.</p>}
			<input type="submit" />
		</form>
	);
	}


.. class:: tag

    Zadanie

Dodaj klase Form do głównej strony App (tzn.  <Form/>), zobacz jej implementację.


    
.. [*] Wykorzystano materiały z:

https://legacy.reactjs.org/docs/hooks-intro.html

https://vimalselvam.com/post/toggle-theme-using-react-hooks/

https://www.w3schools.com/react/showreact.asp?filename=demo2_react_useref2

https://legacy.reactjs.org/docs/hooks-reference.html

https://react.dev/

https://www.freecodecamp.org/news/react-hooks-fundamentals/

https://www.react-hook-form.com/

https://sst.dev/archives/understanding-react-hooks.html
