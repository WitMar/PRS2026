.. role:: todo

.. role:: hold

.. role:: raw-latex(raw)
            :format: latex html

==========================================
Programming Laboratory
==========================================

.. class:: important 

    Attention! The code for this classes can be found on the branch **StreamsAndCollectionsStart** in the https://github.com/WitMar/PRA2020-PRA2021 repository. The ending code in the branch **StreamsAndCollectionsEnd**.
    
If you do not see the right branches on GitHub, click **Ctr + T**, and if it does not help, choose **VCS-> Git-> Fetch** from the menu.        

------------------------------
Fluent API
------------------------------

The term Fluent interface was coined by Martin Fowler and Eric Evans. Fluent API means to build an API in such way so that it meets the following criteria:

    | * The API user can understand the API very easily.
    | * The API can perform a series of actions in order to finish a task. In Java, we can do it with a series of method calls (chaining of methods).
    | * Each method's name should use domain-specific terminology.
    | * The API should be suggestive enough to guide API users on what to do next and what possible operations users can take at a particular moment.
    
**The Fluent Interface builder** should be used when the constructor has more than four or five parameters, we create a builder class to help in creating objects.

The main idea is to rather than having something like:

.. class:: highlight

.. code:: java

	Person(String name, Title title) {
		this.name = name;
		this.title = title;
	}
    
	Person adam = new Person("Adam Z.", Title.PROF);
	 
To use more clear to the programmer methods using facade class called **builder**:

.. class:: highlight

.. code:: java

  public class PersonBuilder implements IPersonBuilder {
    Title title;
    String name;

    public Person build() {
        Person person = new Person(this.name, this.title);
        return person;
    }

    @Override
    public IPersonBuilder withName(String name) {
        this.name = name;
        return this;
    }

    @Override
    public IPersonBuilder withTitle(Title title) {
        this.title = title;
        return this;
    }
  }

    PersonBuilder personBuilder = new PersonBuilder();
    Person person = personBuilder.withName("Marcin Witkowski")
            .withTitle(Title.DR)
            .build();

Which makes the code much easier to read.

In above example we also use interfaces which are not necessary in general, see also example : 

 | http://www.javabyexamples.com/builder-vs-fluent-interface/

The same idea can be used not only in the case of building a new object but also for managing objects and their methods.

Most important element here is that implementation of **fluent API** requires passing the same object from one function call to the next (**return this**).

Here again we are using the interface, which is not necessary in general:

.. class:: highlight

.. code:: java

  public class Person implements IPerson {
    List<Person> friends = new ArrayList<>();
    String name;
    Enum title;

    @Override
    public IPerson addFriend(Person friend) {
        this.friends.add(friend);
        return this;
    }
  }

To add friend for a person we execute method addFriend() which returns **Person** object that allows us to use other methods on the result in a chain (similarly to how the pipes in operating systems works).

.. class:: highlight

.. code:: java

	adam.addFriend(Ben).addFriend(Barrack).addFriend(John);
	
.. class:: tag    
    
    Task 1: Builder

Go to class MainFluentApi and create an object of a class Person using the Builder. Check whether you can access constructor of the Person class and create an object via **new Person()**;

.. class:: tag    
    
    Task 2: Friends

Add two more people and add them as friends for first person.

.. class:: tag    
    
    Task 3: Hello

Implement method sayHelloToFriends in class Person so that it writes Hello <person name> on screen. Check if it works.

Function
~~~~~~~~

Function is a special interface in java consisting of three methods. **apply()** - that applies function to given argument.

.. class:: highlight

.. code:: java
  
  Function<Integer, Double> half = a -> a / 2.0; 
    // apply the function to get the result 
  System.out.println(half.apply(10)); 

**addThen()** - it returns a composed function wherein the parameterized function will be executed after the first one. If evaluation of either function throws an error, it is relayed to the caller of the composed function.

.. class:: highlight

.. code:: java

  Function<Integer, Double> half = a -> a / 2.0; 
  // Now treble the output of halffunction 
  half = half.andThen(a -> 3 * a); 
  // apply the function to get the result 
  System.out.println(half.apply(10)); 

**identity()** - This method returns a function which returns its own argument

.. class:: highlight

.. code:: java

  Function<Integer, Double> half = a -> a / 2.0;
  // Now treble the output of halffunction 
  half = half.andThen(Function.identity());
  // apply the function to get the result 
  System.out.println(half.apply(2));

As you notice you can use **lamba expression** notation **x->x** in order to define functions in java. Left side of an arrow denotes arguments (in this case single argument) and the right side denotes function which can be one or more statements (in latter case you need to use \{\}).

.. class:: tag    
    
    Task 4: Process

Implement function processFriends() that will clear the friends list.

Read about Consumer interface

    | https://www.geeksforgeeks.org/java-8-consumer-interface-in-java-with-examples/

.. class:: tag    
    
    Task 5: Process

Implement function processFriendsInPlace() that will clear the friends list, but would not return anything.

.. class:: tag    
    
    Task 6: Best friend

Implement function of choosing best friend to be the first person that became my friends and check if it works. Check what will happen if the friend list would be empty.

----------------
Collections
----------------

Collections in Java:

.. class:: center
	
	|col|
	
.. |col| image:: coll.png	

.. class:: center
	
	|map|
	
.. |map| image:: map.png	

Examples:

.. class:: highlight

.. code:: java

	List<Integer> list = new ArrayList<>();
	Set<Integer> list = new HashSet<>();
		
------------------------------
Streams
------------------------------
        
Traditionally in Java we use the iterators explicitly specified in the code to navigate the collections:

.. class:: highlight

.. code:: java

    List <String> names = new ArrayList <>();
    for (Student student: students) {
        if (student.getName ().startsWith("A")) {
            names.add (student.getName ());
        }
    }

Using streams, we use the so-called **internal iterations**, that is, the logic of iteration after elements is hidden for us and we focus on their processing.
        
.. class:: highlight

.. code:: java

  List <String> namesNewJava = students.stream()
                .map(student -> student.getName())
                .filter (name-> name.startsWith("A"))
                .collect (Collectors.toList());

Operations on streams
~~~~~~~~~~~~~~~~~~~~~~

The operation on the streams are divided into **intermediate** and **final** (terminal). 

Intermediate operations return the stream as a result of the action. In the above example, such operations are *map ans filter*. Terminal operations terminate processing, usually they aggregate results, count values, or do nothing (eg. foreach operation may be terminal), in the above example such operation is *collect*.

Special streams have been created for numerical operations **IntStream, DoubleStream, and LongStream**.

.. class:: highlight

.. code:: java

	IntStream.rangeClosed(1, 10).forEach(num -> System.out.print(num));
	// ->12345678910
	IntStream.range(1, 10).forEach(num -> System.out.print(num));
	// ->123456789

Structure construction
-------------------------

Stream of constants and array elements:

.. class:: highlight

.. code:: java

  Stream.of("This", "is", "Java8", "Stream").forEach(System.out::println);
  
  String[] stringArray = new String[]{"Streams", "can", "be", "created", "from", "arrays"};
	
  Arrays.stream(stringArray).forEach(System.out::println);

Stream methods
--------------------

**Map**
~~~~~~~~

It changes the processed element to something else, i.e. it takes an element of one type and returns another type of element. In practice, it is usually used to extract some attributes from objects.

.. class:: highlight

.. code:: java

	students.stream()
		.map(Student::getName)
		.forEach(System.out::println);

The *Student::getName* is a short reference to the method from the class. So on a student object that comes from stream, we call the *getName()* method.

It can be written also as:

.. class:: highlight

.. code:: java

	students.stream()
		.map(student -> student.getName())
		.forEach(System.out::println);

**Filter**
~~~~~~~~~~

Selects elements from the stream relative to a given condition

.. class:: highlight

.. code:: java

	students.stream()
			.filter(student -> student.getScore() >= 60)
			.collect(Collectors.toList());

**Distinct**
~~~~~~~~~~~~~~~~
			
Removes repetitions from collection

.. class:: highlight

.. code:: java

	students.stream()
			.map(Student::getName)
			.distinct()
			.collect(Collectors.toList());

**Limit**	
~~~~~~~~~~~~~~~

Limits the number of elements in the stream to the given number.
	
**Sorted**	
~~~~~~~~~~~~~~~~

Sorts elements in a natural order.

.. class:: highlight

.. code:: java

	students.stream()
			.map(Student::getName)
			.sorted()
			.collect(Collectors.toList());	

With the help of the Comparator class, you can define sorts of different types

.. class:: highlight

.. code:: java

	//Sorting names if the Students in descending order
	students.stream()
			.map(Student::getName)
			.sorted(Comparator.reverseOrder())
			.collect(Collectors.toList());
	//Sorting names if the Students in descending order
	students.stream()
			.map(Student::getName)
			.sorted(Comparator.reverseOrder())
			.collect(Collectors.toList());
	//Sorting students by First Name and Last Name both
	students.stream()
			.sorted(Comparator.comparing(Student::getFirstName).
					thenComparing(Student::getLastName))
			.map(Student::getName)
			.collect(Collectors.toList());
	//Sorting students by First Name Descending and Last Name Ascending
	students.stream()
			.sorted(Comparator.comparing(Student::getFirstName)
					.reversed()
					.thenComparing(Student::getLastName))
			.map(Student::getName)
			.collect(Collectors.toList());

**FlatMap**
~~~~~~~~~~~~~~

It works like a map, only as a result it returns a stream of processed items.

.. class:: highlight

.. code:: java

	List<Integer> numbers = Arrays.asList(1, 2, 3, 4);
	List<List<Integer>> mapped = 
					numbers.stream()
					.map(number -> Arrays.asList(number -1, number, number +1))
					.collect(Collectors.toList());
	
	System.out.println(mapped); //:> [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5]]
	
	List<Integer> flattened = 
					numbers.stream()
					.flatMap(number -> Arrays.asList(number -1, number, number +1).stream())
					.collect(Collectors.toList());
					
	System.out.println(flattened);  //:> [0, 1, 2, 1, 2, 3, 2, 3, 4, 3, 4, 5]


Terminals
--------------------

**Match**	
~~~~~~~~~~~~

Match is used when we are interested in appearing in the stream of an element with given properties.

.. class:: highlight

.. code:: java

	//Check if at least one student has got distinction
	Boolean hasStudentWithDistinction = students.stream()
			.anyMatch(student -> student.getScore() > 80);
	
	//Check if All of the students have distinction
	Boolean hasAllStudentsWithDistinction = students.stream()
			.allMatch(student -> student.getScore() > 80);
	
	//Return true if None of the students are over distinction
	Boolean hasAllStudentsBelowDistinction = students.stream()
			.noneMatch(student -> student.getScore() > 80);	

**Find**	
~~~~~~~~~~

Allows you to find an object in the stream with given properties, we can choose any matching object or the first one matched.

.. class:: highlight

.. code:: java	

	//Returns any student that matches to the given condition
	students.stream().filter(student -> student.getAge() > 20)
				.findAny();
	//Returns first student that matches to the given condition
	students.stream().filter(student -> student.getAge() > 20)
				.findFirst();

**Reduce**
~~~~~~~~~~~~

It allows you to reduce the data stream to a single value.

.. class:: highlight

.. code:: java	

	//Summing without passing an identity
	Optional<integer> sum = numbers.stream()
			.reduce((x, y) -> x + y);
	//Product without passing an identity
	Optional<integer> product = numbers.stream()
			.reduce((x, y) -> x * y);

**Collect**	
~~~~~~~~~~~~~~

Collects stream elements in the list.

.. class:: highlight

.. code:: javascript

    students.stream()
        .filter(student -> student.getScore() >= 60)
		.collect(Collectors.toList());

.. class:: important 		

    Hint: Collect return a new object! New list, map, set etc. But the values are the same as in the processed collection. 			

**RemoveIf**
~~~~~~~~~~~~~

Removing elements from list base on filter condition.

			
.. class:: highlight

.. code:: java

	students.removeIf(student -> student.getScore() >= 60)    
    
.. class:: tag    
    
    Task 7: Streams

Implement using streams empty methods in class **Task**. Run **TasksTest** to check if you had implemented methods properly.


Local variables
----------------

This won't compile:


.. class:: highlight

.. code:: java

  int i = 0;
  IntStream.range(1, 10).forEach(number -> {
      if (number < i) {
          System.out.println("Smaller");
          i++;
      }
  });

The basic reason this won't compile is that the lambda is capturing the value of **i**, meaning making a copy of it. Forcing the variable to be final avoids giving the impression that incrementing **i** inside the lambda could actually modify the **i** method parameter.

Whereas this will compile:

.. class:: highlight

.. code:: java

 private int i =0;
 
 public void method() {
    IntStream.range(1, 10).forEach(number -> {
         if (number < i) {
             System.out.println("Smaller");
             i++;
         }
     });
  }

Simply put, it's about where member variables are stored. Local variables are on the stack, but member variables are on the heap. Because we're dealing with heap memory, the compiler can guarantee that the lambda will have access to the latest value of variable **i**.

On the other hand changing values of variables inside stream can bring problems when you execute them in parallel:

.. class:: highlight

.. code:: java

     IntStream stream = IntStream.range(1, 100);
     stream.parallel().forEach(number -> {
        if (number > i) {
            System.out.println(i + " smaller than + number);
            i+=2;
        }
      });
      
Examples of how to stream with indexes through the collection can be found here:

    | https://www.baeldung.com/java-stream-indices
    
------------------------------
Laziness
------------------------------

In programming language theory, lazy evaluation, or call-by-need is an evaluation strategy which delays the evaluation of an expression until its value is needed. In the Java 8 Streams API, the pipeline is constructed lazily, stored as a set of instructions. Only when we invoke a terminal operation, the pipeline is started.

In other words streams are **lazy** because intermediate operations are not evaluated until terminal operation is invoked (maybe even never if the streams does not contain a terminal!). This allows streams to process big-data with high performance.

When a terminal operation completes in final time even if the input from a stream is infinite, then it is called short-circuiting. Java 8 Streams API optimises stream processing with the help of short circuiting operations. Short Circuit methods ends the stream processing as soon as their conditions are satisfied.

.. class:: highlight

.. code:: java

        // lazy evaluation - it does not matter where you put the limit
        IntStream.range(1, 100)
                .map(a -> {
                    if (a > 10) {
                        try {
                            Thread.sleep(5000);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                    return a;
                }).limit(5)
                .forEach(a -> System.out.println(a));

Intermediate operations are divided into stateless and stateful operations. Stateless operations, such as filter and map, retain no state from previously seen element when processing a new element -- each element can be processed independently of operations on other elements. Stateful operations, such as distinct and sorted, may incorporate state from previously seen elements when processing new elements.

Stateful operations may need to process the entire input before producing a result.

.. class:: tag    
    
    Task 8: Sorting

Check if the behaviour changes if you sort the stream.


.. class:: highlight

.. code:: java

    Stream.of("Sun", "Set", "Run", "Stream").filter(word -> {
            System.out.println(word);
            return word.startsWith("S");
        }).limit(2).forEach(System.out::println);
        
Does it change with the change in place of sorted() ? Now the place of limit is important!


------------------------------
Eclipse Collections
------------------------------

Collection are used to store elements in specific order that allows to find the elements efficiently, safe memory space or order elements in specific sequence. The examples are Sets, Maps, Queues etc.

Eclipse Collections are collections implementation that provides memory efficient implementation of Sets and Maps as well as primitive collections.    
     
The origin of Eclipse Collections was started off as a collections framework named Caramel at a bank Goldman Sachs in 2004. To maximize the best nature of open source project, GS Collections has been migrated to the Eclipse Foundation, re-branded as Eclipse Collections in 2015. Now the framework is fully open to the community, accepting contributions.

Maven dependencies: 

.. class:: highlight

.. code:: java

    <dependency>
        <groupId>org.eclipse.collections</groupId>
        <artifactId>eclipse-collections-api</artifactId>
        <version>9.2.0</version>
    </dependency>

    <dependency>
        <groupId>org.eclipse.collections</groupId>
        <artifactId>eclipse-collections</artifactId>
        <version>9.2.0</version>
    </dependency>

Structures implemented in Eclipse Collections are usually faster and more memory-efficient that from java.util. You can find in Eclipse collections an additional structures which can not be found in java.util. One of the most usefull is **MultiMap**.

MultiMap is a map for which every key can be assigned more than one value. Values in the map are then stored as a list connected with the key.

Example:

.. class:: highlight

.. code:: java

    FastListMultimap<String, String> citiesToPeople = FastListMultimap.newMultimap();

    citiesToPeople.put("Poznan", "Nowak");
    citiesToPeople.put("Poznan", "Kowalski");
    
    citiesToPeople.get("Poznan").forEach(name -> System.out.println(name));
            
More examples:

    | https://www.baeldung.com/eclipse-collections   
    
.. class:: tag    
    
    Task 9: MultiMap

Implement function partitioningAdults in **MainEclipseCollection** so that it pass the test. Use google to find how to collect to EclipseCollection.          

.. [*] Used materials from:
	
	| https://www.eclipse.org/collections/
	| https://dzone.com/articles/java-fluent-api-design
	| https://kamiljozwiak.net/fluent-api/
	| https://www.baeldung.com/java-lambda-effectively-final-local-variables
	| https://github.com/vfarcic/java-8-exercises
	| https://www.javatpoint.com/collections-in-java
