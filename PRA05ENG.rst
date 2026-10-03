.. role:: todo

.. role:: hold

.. role:: raw-latex(raw)
            :format: latex html

==========================================
Programming Laboratory
==========================================

------------------------------
ORM
------------------------------

.. class:: important 

    Attention! The code for this classes can be found on the branch **HibernateStart** in  https://github.com/WitMar/PRA2020-PRA2021 repository.. The ending code in the branch **HibernateEnd**.
    
If you do not see the right branches on GitHub, click **Ctr + T**, and if it does not help, choose **VCS-> Git-> Fetch** from the menu.    

ORM
=====

ORM is a short name for "object-relational mapping". Therefore, it is about providing data (from relations in a database) to objects or in the other direction. As a result, business logic is able to access and manipulate database entities via Java objects. It helps to speed up the overall development process by taking care of aspects such as transaction management, automatic primary key generation, managing database connections and related implementations, and so on.  It is a modern approach to the problem of cooperation with a database, using the object oriented programming philosophy

ORM elements
---------------

    | 1. API for managing object persistence

    | 2. Mechanism of specifying metadata describing the mapping of classes to relations in databases
    
    | 3. Language or API to perform queries. 
    
    
The most popular implementation of object-relational mapping technology for Java applications is Hibernate (for C # to LinQ)

Architecture
=============

.. class:: center
	
	|arch|
	
.. |arch| image:: archHib.png

    
Elements:

    | * Configuration : Generally written in hibernate.properties or hibernate.cfg.xml files. For Java configuration, you may find class annotated with @Configuration. It is used by Session Factory to work with Java Application and the Database. It represents an entire set of mappings of an application Java Types to an SQL database.
    
    | * Session Factory : Any user application requests Session Factory for a session object. Session Factory uses configuration information from above listed files, to instantiates the session object appropriately.
    
    | * Session : This represents the interaction between the application and the database at any point of time. This is represented by the org.hibernate.Session class. The instance of a session can be retrieved from the SessionFactory bean. Session by default is **only flushed when necessary**.
    
    | * Query : It allows applications to query the database for one or more stored objects. Hibernate provides different techniques to query database, including NamedQuery and Criteria API.
    
    | * First-level cache : It represents the default cache used by Hibernate Session object while interacting with the database. It is also called as session cache and caches objects within the current session. All requests from the Session object to the database must pass through the first-level cache or session cache. One must note that the first-level cache is available with the session object until the Session object is live.
    
    | * Transaction : enables you to achieve data consistency, and rollback incase something goes unexpected.
    
    | * Persistent objects : These are plain old Java objects (POJOs), which get persisted as one of the rows in the related table in the database by hibernate.They can be configured in configurations files (hibernate.cfg.xml or hibernate.properties) or annotated with @Entity annotation.
    
    | * Second-level cache : It is used to store objects across sessions. This needs to be explicitly enabled and one would be required to provide the cache provider for a second-level cache. One of the common second-level cache providers is EhCache.

Dependencies
============

To use Hibernate we will need a hibernate-core package and a database driver.

.. class:: highlight

.. code:: xml

        <!-- Hibernate resources -->
        <dependency>
            <groupId>org.hibernate</groupId>
            <artifactId>hibernate-entitymanager</artifactId>
            <version>5.4.0.Final</version>
        </dependency>
        <dependency>
            <groupId>org.hibernate</groupId>
            <artifactId>hibernate-core</artifactId>
            <version>5.4.0.Final</version>
        </dependency>
        <dependency>
            <groupId>org.hibernate</groupId>
            <artifactId>hibernate-search-orm</artifactId>
            <version>5.11.1.Final</version>
        </dependency>
        <dependency>
            <groupId>org.hibernate</groupId>
            <artifactId>hibernate-validator</artifactId>
            <version>5.4.0.Final</version>
        </dependency>
        <dependency>
            <groupId>org.hibernate.common</groupId>
            <artifactId>hibernate-commons-annotations</artifactId>
            <version>4.0.2.Final</version>
            <classifier>tests</classifier>
        </dependency>
        <dependency>
            <groupId>org.hibernate.javax.persistence</groupId>
            <artifactId>hibernate-jpa-2.0-api</artifactId>
            <version>1.0.1.Final</version>
        </dependency>
        <dependency>
            <groupId>com.sun.xml.bind</groupId>
            <artifactId>jaxb-impl</artifactId>
            <version>2.3.0</version>
        </dependency>
        
        <!-- Database driver here POSTGRES!--> - darmowa baza danych
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <version>42.1.1</version>
        </dependency>
        <dependency>
            <groupId>org.hsqldb</groupId>
            <artifactId>hsqldb</artifactId>
            <version>2.5.0</version>
            <scope>test</scope>
        </dependency>
        
In our project, we will use the **HSQL (in-memory) database** (because we do not want to install any additional software), but you should try to run proper database engine like **PostgreSQL** or **MySQL**.

You can also use free online database 
	
	https://remotemysql.com/login.php

.. class:: tag

    Excercise 1
    
Add dependencies to the **pom.xml** file.
    
Hibernate configuration
=======================

We save the Hibernate configurations in the file named **hibernate.cfg.xml**, **hibernate.properties** or **persistence.xml**.

Attention! Depending on what elements we use, the library will automatically search for specific files in the project path to find the configuration.

We must specify:

    | access details of connection to the database, address, password, user, location,
    
    | the language of the sql queries we want to use,
    
    | possibly a list of classes mapped to database tables

    | **dialect** specifies how hibernate is going to communicate with the database
    
    | **show_sql** - true will show us SQL queries created by hibernate (mainly for debugging).

    | **hbm2dll** specifies the behavior of the database schema **create** means that we create the schema from scratch every time. Once we create it, I recommend changing the value to **validate** or **update** - but the update is not recommended because it can cause strange errors like "table not found".

Sample database access settings for the PostgreSQL database:   

.. class:: highlight

.. code:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <persistence version="2.1" xmlns="http://xmlns.jcp.org/xml/ns/persistence"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/persistence
                                     http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
        <persistence-unit name="hibernate-dynamic" transaction-type="RESOURCE_LOCAL">
            <properties>
                <!-- Configuring JDBC properties -->
                <property name="javax.persistence.jdbc.url" value="jdbc:postgresql://localhost:5432/postgres"/>
                <property name="javax.persistence.jdbc.user" value="postgres"/>
                <property name="javax.persistence.jdbc.password" value="postgres"/>
                <property name="javax.persistence.jdbc.driver" value="org.postgresql.Driver" />
    
                <!-- Hibernate properties -->
                <property name="hibernate.dialect" value="org.hibernate.dialect.PostgreSQLDialect"/>
                <property name="hibernate.hbm2ddl.auto" value="create"/>
                <property name="hibernate.format_sql" value="false"/>
                <property name="hibernate.show_sql" value="true"/>
    
            </properties>
        </persistence-unit>
    </persistence>
    
**Note!** In order to run the program with the above settings at home you should have PostgreSQL server installed or change the server address in the settings. You should easily find information about PostgreSQL installation on the internet. To edit data in the postgresql database, I recommend using program called **pgAdmin**.
    
Configuration using the university PostgreSQL database:

.. class:: highlight

.. code:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <persistence version="2.1" xmlns="http://xmlns.jcp.org/xml/ns/persistence"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/persistence
                                    http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
        <persistence-unit name="hibernate-dynamic" transaction-type="RESOURCE_LOCAL">
            <properties>
                <!-- Configuring JDBC properties -->
                <property name="javax.persistence.jdbc.url" value="jdbc:postgresql://psql.wmi.amu.edu.pl:5432/mw?ssl=true&amp;sslfactory=org.postgresql.ssl.NonValidatingFactory"/>
                <property name="javax.persistence.jdbc.user" value="mw"/>
                <property name="javax.persistence.jdbc.password" value="riustsdardswify"/>
                <property name="javax.persistence.jdbc.driver" value="org.postgresql.Driver" />

                <!-- Hibernate properties -->
                <property name="hibernate.dialect" value="org.hibernate.dialect.PostgreSQLDialect"/>
                <property name="hibernate.hbm2ddl.auto" value="create"/>
                <property name="hibernate.format_sql" value="false"/>
                <property name="hibernate.show_sql" value="true"/>
            </properties>
        </persistence-unit>
    </persistence>

During the classes we will use the HSQL database run in the computer's memory, with given settings:

.. class:: highlight

.. code:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <persistence version="2.1" xmlns="http://xmlns.jcp.org/xml/ns/persistence"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/persistence
                                    http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
        <persistence-unit name="hibernate-dynamic" transaction-type="RESOURCE_LOCAL">
            <properties>
                <!-- Configuring JDBC properties -->
                <property name="javax.persistence.jdbc.url" value="jdbc:hsqldb:mem:PRA"/>
                <property name="javax.persistence.jdbc.user" value="sa"/>
                <property name="javax.persistence.jdbc.password" value=""/>
                <property name="javax.persistence.jdbc.driver" value="org.hsqldb.jdbc.JDBCDriver" />
    
                <!-- Hibernate properties -->
                <property name="hibernate.dialect" value="org.hibernate.dialect.HSQLDialect"/>
                <property name="hibernate.hbm2ddl.auto" value="create"/>
                <property name="hibernate.format_sql" value="false"/>
                <property name="hibernate.show_sql" value="true"/>
    
            </properties>
        </persistence-unit>
    </persistence>
    
.. class:: tag 
    
    Exercise 2
    
Add to the directory **resources** subdirectory **META-INF** and in it file **persistence.xml** paste the above content into it.
    
**IMPORTANT** if you see an error :

.. class:: highlight

.. code:: xml

    Initial SessionFactory creation failed.javax.persistence.PersistenceException: No Persistence provider for EntityManager named hibernate-dynamic
    Exception in thread "main" java.lang.NullPointerException
    
Then hibernate can not find your properties file.    
    
Mapping - annotations
=======================

The mapping between the database tables and the class is carried out using the annotation mechanism.

    | **@Entity** annotation used to specify that the given class should be mapped to the database entity.

    | **@Table** specifies the table properties (e.g. name, definition of restrictions, etc.), if this annotation is not the table name will be the name of the class

    | **@Id** denote the main key of the table

    | **@Column** specifies the properties of the table column (eg, the name, whether it must be unique or empty), if it is not defined, the column will have the same name as the class field.

    | **@GeneratedValue** means that the value of this field will be automatically generated
    
Example:    

.. class:: highlight

.. code:: java

    package hibernate.model;

    import javax.persistence.*;

    @Entity
    @Table(name = "EMPLOYEE", uniqueConstraints = {
            @UniqueConstraint(columnNames = {"first_name","last_name"})})
    public class Employee {
    
        @Id @GeneratedValue
        @Column(name = "id")
        private int id;
    
        @Column(name = "first_name")
        private String firstName;
    
        @Column(name = "last_name")
        private String lastName;
    
        @Column(name = "salary")
        private int salary;
    
        @Column(name = "PESEL", nullable = false, unique = true)
        private int pesel;
    
        public Employee() {}
    
        public int getId() {
            return id;
        }
    
        public void setId( int id ) {
                this.id = id;
        }
    
        public String getFirstName() {
             return firstName;
        }

        public void setFirstName( String first_name ) {
            this.firstName = first_name;
        }
    
        public String getLastName() {
            return lastName;
        }
    
        public void setLastName( String last_name ) {
            this.lastName = last_name;
        }
    
        public int getSalary() {
            return salary;
        }

            public void setSalary( int salary ) {
            this.salary = salary;
        }
    
        public int getPesel() {
            return pesel;
        }
    
        public void setPesel(int pesel) {
            this.pesel = pesel;
        }
    }
    
.. class:: tag 

    Exercise 3
    
Add the **hibernate** package and package **model** in it. Create the above class.

Inheritance class mapping
==========================

.. class:: highlight

.. code:: java

    @Entity(name = "Account")
    @Inheritance(strategy = InheritanceType.SINGLE_TABLE)
    public static class Account {

        @Id
        private Long id;

        private String owner;
    
        private BigDecimal balance;

        private BigDecimal interestRate;

        //Getters and setters are omitted for brevity

    }

    @Entity(name = "DebitAccount")
    public static class DebitAccount extends Account {

        private BigDecimal overdraftFee;

        //Getters and setters are omitted for brevity

    }   

    @Entity(name = "CreditAccount")
    public static class CreditAccount extends Account {

        private BigDecimal creditLimit;

        //Getters and setters are omitted for brevity

    }


More : 

    | https://docs.jboss.org/hibernate/orm/5.4/userguide/html_single/Hibernate_User_Guide.html#entity-inheritance

Collections mapping
====================

.. class:: highlight

.. code:: java

    @Entity(name = "Employee")
    public static class Employee {
    
        @Id
        private Long id;
    
        @ElementCollection
        private List<String> phones = new ArrayList<>();

        ...

    }
    
.. class:: tag 

    Exercise 3
    
Add the collection of **phones** to person, see how they are mapped in the database by Hibernate.   

In the log4j.properties file, paste the line

.. class:: highlight

.. code:: java

    log4j.logger.org.hibernate=info

It determines the level of login messages from hibernate. See what has changed.    

Persistence Context
====================

Apart from object-relational mapping itself, one of the problems that Hibernate was intended to solve is the problem of managing entities during runtime. The notion of “persistence context” is Hibernate’s solution to this problem. Persistence context can be thought of as a container or a first-level cache for all the objects that you loaded or saved to a database during a session.

Any entity instance in your application appears in one of the three main states in relation to the Session persistence context:

    | * transient — the entity has just been instantiated and is not associated with a persistence context. It has no persistent representation in the database and typically no identifier value has been assigned (unless the assigned generator was used).
    
    | * managed or persistent — the entity has an associated identifier and is associated with a persistence context. It may or may not physically exist in the database yet.
    
    | * detached — the entity has an associated identifier but is no longer associated with a persistence context (usually because the persistence context was closed or the instance was evicted from the context).

It is important to understand from the beginning that all of the methods (persist, save, update, merge, saveOrUpdate) do not immediately result in the corresponding SQL UPDATE or INSERT statements. The actual saving of data to the database occurs on committing the transaction or flushing the Session.

.. class:: center
	
	|ass10|
	
.. |ass10| image:: hib.png


EntityManager vs SessionManager
=================================

In Hibernate, the persistence context is represented by **org.hibernate.Session instance**. For JPA, it is the **javax.persistence.EntityManager**. When we use Hibernate as a JPA provider and operate via EntityManager interface, the implementation of this interface basically wraps the underlying Session object.

We will be using **Session** in our examples.

If during the work with Entity Manager you need the Session objects you can also get it using:

.. class:: highlight

.. code:: java

    Session session = entityManager.unwrap( Session.class );
    SessionImplementor sessionImplementor = entityManager.unwrap( SessionImplementor.class );

    SessionFactory sessionFactory = entityManager.getEntityManagerFactory().unwrap( SessionFactory.class );


Working with Session object
=============================

Get method
------------

The find method is used to retrieve one object based on its key. The key to search for an object is this field, which has the annotation **@Id**. An example call:

.. class:: highlight

.. code:: java

    session.get(Employee.class, 1L);

    session.byId( Employee.class ).load( 1L );
        
    // get only reference not the whole object
    book.setWorker( session.load( Employee.class, 1L ) );

will download us an Employee type object that has an ID equal to 1.

If this method does not find the object in the database, it returns null.

It’s possible to return a Java 8 Optional as well:

.. class:: highlight

.. code:: java

    Optional<Employee> optionalPerson = session.byId( Employee.class ).loadOptional( 1L );
    
Loading with multiple id's

.. class:: highlight

.. code:: java

    List<Employee> employees = session
		.byMultipleIds( Employee.class )
		.multiLoad( 1L, 2L, 3L );

Save method
---------------

You can use this method to insert a new object into the managed state. Example:

.. class:: highlight

.. code:: java
    
    Employee emp = new Employee();
    session.save( person );

Moves the new object to the *managed* state. The save method makes the object manageable, i.e. any changes made to it (within one method with @Transactional annotation or methods that this method calls) will be persisted in the database.

Merge method
---------------

You can use this method to insert an existing object from the *detached* state to the *managed* state. Example:

.. class:: highlight

.. code:: java
    
    Employee person = session.byId( Employee.class ).load( 1L );
    //Clear the Session so the person entity becomes detached
    session.clear();
    person.setName( "Mr. John Doe" );

    person = (Employee) session.merge( person );
    
Verifying managed state with Hibernate API

.. class:: highlight

.. code:: java

    boolean contained = session.contains( person );    

Delete method
---------------

The delete method is used to remove objects.

.. class:: highlight

.. code:: java

    session.delete( person );

More information:

    | https://docs.oracle.com/javaee/6/api/javax/persistence/EntityManager.html
    
Example
========

A class that writes and reads an element from a database:

.. class:: highlight

.. code:: java

    class Manager {

    public static void main(String[] args) {

        System.out.println("Start");

        EntityManager entityManager = null;

        EntityManagerFactory entityManagerFactory = null;

        try {

            // FACTORY NAME HAS TO MATCHED THE ONE FROM PERSISTED.XML !!!
            entityManagerFactory = Persistence.createEntityManagerFactory("hibernate-dynamic");

            entityManager = entityManagerFactory.createEntityManager();
            Session session = entityManager.unwrap(Session.class);

            //New transaction
            session.beginTransaction();

            Employee emp = new Employee();
            emp.setFirstName("Jan");
            emp.setLastName("Polak" + new Random().nextInt());
            emp.setSalary(100);
            emp.setPesel(new Random().nextInt());

            // Save in First order Cache (not database yet)
            session.save(emp);

            Employee employee = session.get(Employee.class, emp.getId());
            if (employee == null) {
                System.out.println(emp.getId() + " not found! ");
            } else {
                System.out.println("Found " + employee);
            }

            System.out.println("Employee " + employee.getId() + " " + employee.getFirstName() + employee.getLastName());

            changeFirstGuyToNowak(session);

            //Commit transaction to database
            session.getTransaction().commit();

            System.out.println("Done");

            session.close();

        } catch (Throwable ex) {
            // Make sure you log the exception, as it might be swallowed
            System.err.println("Initial SessionFactory creation failed." + ex);
        } finally {
            entityManagerFactory.close();
        }

    }
    
Queries
=======================

Native Query
--------------

You may express queries in the native SQL dialect of your database.

.. class:: highlight

.. code:: java

    List<Object[]> persons = session.createNativeQuery(
        "SELECT * FROM Employee" )
    .getResultList();
    
HQL
-----------    

The Hibernate Query Language (HQL) and Java Persistence Query Language (JPQL) an SQL-like languages to create queries in Hibernate. To execute the query, we must first create it using the **session.createQuery** method and then retrieve the result. To download a list of employees we need to do the following code:

The simplest possible HQL SELECT statement is of the form:

.. class:: highlight

.. code:: java
    
    List<Employee> persons = session.createQuery(
        "from Employee" )
    .list();
    

To define queries with parameters:

.. class:: highlight

.. code:: java

   session.createQuery(
                "SELECT c FROM Employee c WHERE c.lastName LIKE :firstName", Employee.class)
                .setParameter("firstName", "%" + firstName + "%").list();

The query is represented by the Query object:

.. class:: highlight

.. code:: java

    Query query = session.createQuery("SELECT k FROM Employee k");
    List<Employee> employees = query.getResultList();

If our query returns only one element, we can use the **query.getSingleResult()** method.

Attention! If the query to the database does not return results (the result is empty), then:

    | the **getResultList()** method will return **null**!

    | the **getSingleResult()** method throws an exception (NoResultException)! (if we have more than one result, we also get an exception - NonUniqueResultException)

The objects returned in the query are **persisted** that is, all changes made to them will be automatically saved to the database (if they are included in the transaction - objects outside the transaction will not be saved).

.. class:: tag 

   Exercise 5
    
Add the getThemAll() method to the class that retrieves all employees.

Attention! Please note that the query uses a field name such as the name in the class, not the name in the database!

With the exception of names of Java classes and properties, queries are case-insensitive. So SeLeCT is the same as sELEct is the same as SELECT, but org.hibernate.eg.FOO and org.hibernate.eg.Foo are different, as are foo.barSet and foo.BARSET.   

Join query example
-------------------

.. class:: highlight

.. code:: java

    List<Person> persons = session.createQuery(
        "select distinct pr " +
        "from Person pr " +
        "join pr.phones ph " +
        "where ph.type = :phoneType", Person.class )
    .setParameter( "phoneType", PhoneType.MOBILE )
    .getResultList();
    
    
Criteria Query
-----------------

There is a third way to create a query in Hibernate which is called Criteria Query, you can read about it here:

    | https://docs.jboss.org/hibernate/orm/5.4/userguide/html_single/Hibernate_User_Guide.html#criteria

OneToOne dependencies
=================================

Between the database tables we can have dependencies such as 1-1, 1-*, *-*.

Goal: Define the relationship between objects - let one object be the field of the other.

Sometimes our model requires that in addition to simple types, the given entity should contain a reference to another entity. For example, we want to connect an employee with his address.

.. class:: tag 

    Exercise 6

Define the address class having the city, street, nr, houseNumber, postcode fields. So that all except houseNumber could not be empty and the code had at most 5 characters (all fields should be of the String type). Add the autogenerated master key.

.. class:: highlight

.. code:: java

    @Entity
    @Table(name = "ADDRESSES")
    public class Address {

        @Id
        @GeneratedValue(generator = "gen")
        @SequenceGenerator(name = "gen", sequenceName = "author_seq")
        @Column(name = "id")
        private int id;
    
        @Column(nullable = false)
        String street;
    
        @Column(nullable = false)
        String city;
    
        @Column(length = 5, nullable = false)
        String nr;
        
        @Column(length = 5)
        String housenr;
    
        @Column(length = 5, nullable = false)
        String postcode;
    
        public int getId() {
            return id;
        }
    
        public void setId(int id) {
            this.id = id;
        }
    
        public String getStreet() {
            return street;
        }
    
        public void setStreet(String street) {
            this.street = street;
        }
    
        public String getCity() {
            return city;
        }
    
        public void setCity(String city) {
            this.city = city;
        }
    
        public String getNr() {
            return nr;
        }
    
        public void setNr(String nr) {
            this.nr = nr;
        }
    
        public String getHousenr() {
            return housenr;
        }
    
        public void setHousenr(String housenr) {
            this.housenr = housenr;
        }
    
        public String getPostcode() {
            return postcode;
        }
    
        public void setPostcode(String postcode) {
            this.postcode = postcode;
        }
    }
    
    
Add a field in the Employee class, and define in the Manager address for the employee Jan.

.. class:: highlight

.. code:: java

    @OneToOne(cascade = CascadeType.PERSIST)
    @JoinColumn(name="Address_ID", referencedColumnName = "id")
    Address address;    
    
Join column defines the name of our column and we can define the name of the column with which our element connects (this column must be unique). By default, we connect to the table's primary key.

In OneToOne we can define additional options, optional define whether the field is required, **CASCADE** define whether changes in the person's address field will propagate to the Address table (available options MERGE, PERSIST, REFRESH, REMOVE, ALL).

Examples: 

    | http://www.coderpanda.com/jpa-one-to-one-mapping/

    | http://www.logicbig.com/tutorials/java-ee-tutorial/jpa/one-to-one/

Remember to add the Address to the main code to the employee and assign it to him. Attention! If we want **id** generated for addresses to be different than those for employees then between **@Id** and **@Column** we can enter:

.. class:: highlight

.. code:: java

    @GeneratedValue(generator = "gen")
    @SequenceGenerator(name="gen", sequenceName = "author_seq")

If we need a back-to-back mapping between entities, we must use the **@MappedBy** annotation.

.. class:: tag 

    Exercise 7
    
See what happens if you do not define a value for one of the mandatory fields.

What happens when an object in a persisted state performs:

.. class:: highlight

.. code:: java
    
    emp.getAddress().setStreet(null);

OneToMany, ManyToMany dependencies
===================================

In case when we want both classes to have a link to each other (eg. a child to a parent and a parent to a child), in one class we define @OneToMany annotations and in the other we refer to this mapping through the @ManyToOne). The element without mappedBy is the side responsible for the mapping.

The @OneToMany association links a parent entity with one or more child entities. If the @OneToMany doesn’t have a mirroring @ManyToOne association on the child side, the @OneToMany association is unidirectional. If there is a @ManyToOne association on the child side, the @OneToMany association is bidirectional and the application developer can navigate this relationship from both ends.

.. class:: highlight

.. code:: java

    @Entity
    public class Parent {
    // ...
    
        @OneToMany(mappedBy = "parent", fetch = FetchType.LAZY)
        private Set<Child> children = new HashSet<Child>();
    
    // ...
    }
    
    @Entity
    public class Child {
        // ...
    
        @ManyToOne(fetch = FetchType.LAZY)
        private Parent parent;
    
        // ...
    }
    
.. class:: tag 

    Exercise 8

Change the address - person dependency to be ManyToOne.

.. class:: highlight

.. code:: java

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name="address_id", nullable=false)
    Address address;
    
    @OneToMany(mappedBy = "address", cascade = CascadeType.ALL, fetch =FetchType.EAGER)
    Set<Employee> employee = new HashSet<>();
    
see how this code behaves:

In Employee class addition

.. class:: highlight

.. code:: java

    public static Employee copyEmployee(Employee emp, int i) {
        Employee person = new Employee();
        person.setAddress(emp.getAddress());
        person.setLastName(emp.getLastName() + i);
        person.setFirstName(emp.getFirstName());
        person.setPesel(i);
        person.setSalary(emp.getSalary());
        return person;
    }

In main method add    
    
.. class:: highlight

.. code:: java

    for (int i = 1; i < 100; i++) {
        entityManager.persist(Employee.copyEmployee(emp));
    }
            
    \\ old session
    Set<Employee> listInAddress = session.get(Address.class, 1).getEmployee();

    session.getTransaction().commit();
    session.clear();

    session.getTransaction().begin();
    \\ new session
    listInAddress = session.get(Address.class, 1).getEmployee();
    
You can also do refresh ,to synchronize object

.. class:: highlight

.. code:: java

    ((SessionImpl) session).refresh(emp.getAddress());
    emp.getAddress()


FetchType determines whether in the case of downloading one of the tables we have to poll the database about the object connected to it (select from other table), this is called FetchType.EAGER if we do not want it and the query is to be performed only when we refer to a specific value, select FetchType.LAZY.

Transactions
------------

Attention! There are transactions in the Session, they mean that the database is synchronized with the items in memory only after the transaction is completed.

Important! If an error occurs while processing the transaction, **none** of the operations performed in the code that was transferred to the database. That is why it is worth creating separate transactions for selected functionalities.

The important thing is that in Hibernate, database operations do not have to be executed in the order as they appear in the code at the time of the transaction. In particular, it causes that in one transaction we can not delete and then add an object with the same main key.

.. class:: tag 

    Exercise 9
    
Commit the transaction then delete and add an employee with the same Id, see what happens.

Pagination
================

Purpose: Define the query that return paged data.

It often happens that having many records we do not want to download all of the database every time but we would like to divide them into smaller parts (pages).

The simplest paging software method is the query query configuration

.. class:: highlight

.. code:: java

    Query query = entityManager.createQuery("From EMPLOYEE");
    int pageNumber = 1;
    int pageSize = 10;
    query.setFirstResult((pageNumber-1) * pageSize); 
    query.setMaxResults(pageSize);
    List <Foo> empList = query.getResultList();

We use the methods:

    | **setFirstResult(int)**: sets the position from which we want to download data
    | **setMaxResults(int)**: sets the number of records we want to retrieve from the database

Knowledge about the number of pages to which data is shared is also useful

.. class:: highlight

.. code:: java

    Query queryTotal = entityManager.createQuery ("Select count(e.id) from EMPLOYEE e");
    long countResult = (long)queryTotal.getSingleResult();
    int pageSize = 10;
    int pageNumber = (int) ((countResult / pageSize) + 1);

.. class:: tag 

    Exercise 10

Add a query to the code that downloads all employees broken down into pages.

.. class:: highlight

.. code:: java
    
    public List<Employee> getAllEmployeeByPage(int pagenr) {
        //calculate total number
        Query queryTotal = entityManager.createQuery
                ("Select count(e) from Employee e");
        long countResult = (long)queryTotal.getSingleResult();

        //create query
        Query query = entityManager.createQuery("Select e FROM Employee e");
        //set pageSize
        int pageSize = 10;
        //calculate number of pages
        int pageNumber = (int) ((countResult / pageSize) + 1);

        if (pagenr > pageNumber) pagenr = pageNumber;
        query.setFirstResult((pagenr-1) * pageSize);
        query.setMaxResults(pageSize);

        return query.getResultList();
    }


.. [*] References used to create this materials:

https://kobietydokodu.pl/13-2-baza-danych-z-jpa-cz-2/
	
http://math.uni.lodz.pl/~kowalcr/Bazy/Temat8.pdf

https://docs.jboss.org/hibernate/orm/4.2/quickstart/en-US/html/index.html

http://www.baeldung.com/hibernate-save-persist-update-merge-saveorupdate

http://www.mkyong.com/hibernate/hibernate-one-to-one-relationship-example-annotation/

https://www.javaworld.com/article/2077819/java-se/understanding-jpa-part-2-relationships-the-jpa-way.html

http://www.baeldung.com/jpa-pagination

https://howtodoinjava.com/hibernate-tutorials/

https://docs.jboss.org/hibernate/orm/5.4/userguide/html_single/Hibernate_User_Guide.html
