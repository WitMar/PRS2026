=======================
Programming Laboratory
=======================

--------------------
Spring Boot
--------------------

.. class:: important

    Attention! The code for this class is on the branch **SpringBootStart** in the repository https://github.com/WitMar/PRA2020-PRA2021. The ending code in the branch **SpringBootEnd**.
    
If you do not see the right branches on GitHub, do **Ctr + T**, and if it does not help, choose **VCS-> Git-> Fetch** from the menu.

Spring Boot
-------------

Spring Boot is a lightweight framework that allows you to easily create applications based on the Spring framework. Spring Framework is a platform whose main goal is to simplify the process of software development in Java / J2EE technology. Spring's core is a dependency injection container that manages components and their dependencies. The objects managed by Spring are called beans.

You can read about the spring on materials from previous class.

Starters are groups of dependencies that allow you to run Spring projects with minimal effort to configure them.

In our case the main starter will be:

        | **spring-boot-starter-web** is used to build applications based on REST API using Spring MVC and Tomcat.
        
The above-mentioned starter makes the project configured to use:

    | Built-in Tomcat Server
    | Hibernate for Object-Relational Mapping (ORM)
    | Apache Jackson for JSON binding
    | Spring MVC for the REST framework
    
The full list of starters can be found here:

    | https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#using-boot-starter

Applications using Spring are built modularly. Ideally, it fits in the MVC model and allows the iterative growth of our application with subsequent modules.

If you allow (using the **@EnableAutoConfiguration** annotation), Spring Boot will do the automatic configuration of the project in the widest sense - it will search for the appropriate annotations and create objects for life.

We can also use the website to generate the spring application skeleton:

    | http://start.spring.io/
    
Which will produce the skeleton of the maven app with dependencies.  

Configuration
--------------

Configuration is in the application.properties file

The use of **in-memory** HSQL database

.. code:: bash

    ## Spring DATASOURCE (DataSourceAutoConfiguration & DataSourceProperties)
    spring.jpa.show-sql=true

    spring.database.driverClassName=org.hsqldb.jdbcDriver
    spring.datasource.url=jdbc:hsqldb:mem:spring
    spring.datasource.username=sa
    spring.datasource.password=
    
    ## Hibernate Properties
    
    # The SQL dialect makes Hibernate generate better SQL for the chosen database
    spring.jpa.properties.hibernate.dialect = org.hibernate.dialect.HSQLDialect
    
    # Hibernate ddl auto (create, create-drop, validate, update)
    spring.jpa.hibernate.ddl-auto = create

With **PostgeSQL** database
    
.. code:: bash

    ## Spring DATASOURCE (DataSourceAutoConfiguration & DataSourceProperties)
    spring.jpa.database=POSTGRESQL
    spring.datasource.platform=postgres
    spring.jpa.show-sql=true

    spring.database.driverClassName=org.postgresql.Driver
    spring.datasource.url=jdbc:postgresql://localhost:5432/postgres
    spring.datasource.username=postgres
    spring.datasource.password=postgres

    ## Hibernate Properties

    # The SQL dialect makes Hibernate generate better SQL for the chosen database
    spring.jpa.properties.hibernate.dialect = org.hibernate.dialect.PostgreSQL94Dialect

    # Hibernate ddl auto (create, create-drop, validate, update)
    spring.jpa.hibernate.ddl-auto = create

The settings mainly concern access to the database and are the same as for Hibernate.

Attention! for **spring.jpa.hibernate.ddl-auto** again the best option would be an update. If, however, you have problems with running, you should use **create** and **validate**.

It is also important that many settings elements depend on the database engine we use.

In the POM file, we define:

.. code:: bash

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.4.1</version>
    </parent>

This is the definition of the Spring Boot version we use (**2.4.1**) but also the so-called parent POM, thanks to which in our POM file we can inherit versions of libraries from parent, so that there is full compatibility between them.
So we can define in the POM file:

.. code:: bash

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

Without specifying artifactId and version, both parameters will be inherited from the POM parent (if they are defined there).

Attention! If we want to use a different database than PostgreSql then we need to define a dependency in the POM file to the driver of that database.

.. code:: bash

        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
        </dependency>
    
For the building part we use following plugins that build JAR (and then from it) the WAR file. This version should be compatible with all versions of Java.

.. code:: bash

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-assembly-plugin</artifactId>
                <version>2.4.1</version>
                <dependencies>
                    <dependency>
                        <groupId>org.codehaus.plexus</groupId>
                        <artifactId>plexus-archiver</artifactId>
                        <version>2.4.4</version>
                    </dependency>
                </dependencies>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.0.0</version>
                <dependencies>
                    <dependency>
                        <groupId>org.codehaus.plexus</groupId>
                        <artifactId>plexus-archiver</artifactId>
                        <version>2.4.4</version>
                    </dependency>
                </dependencies>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-war-plugin</artifactId>
                <version>3.2.0</version>
                <configuration>
                    <dependencies>
                        <dependency>
                            <groupId>org.codehaus.plexus</groupId>
                            <artifactId>plexus-archiver</artifactId>
                            <version>2.4.4</version>
                        </dependency>
                    </dependencies>
                </configuration>
            </plugin>
        </plugins>
    </build>
    
Test
-----

The project defines a blank test with annotations.

.. code:: java

    @RunWith(SpringRunner.class)
    @SpringBootTest

It causes the spring environment to be started (without connection to the database). Thanks to that, we can easily check at the time of building whether there are any errors in the definition of settings and the Spring environment.   

Start-up
-------------

The main class of the project is the **SpringApp** class. There is a main function in it, in other words it will be the class you want to run.

To run the Spring application, we need an input class with the **@SpringBootApplication** annotation and a static run() method call on the SpringApplication class. The second annotation from our class is related to the database and will be discussed later.

Currently annotation of the main class:

.. code:: java

    @SpringBootApplication
    @EnableJpaRepositories ("com.pracownia.spring.repositories")
    
The first annotation one is really a collection of several other annotations (**@Configuration** (information that we support HTTP requests), **@ EnableAutoConfiguration** (thanks to it, the application will perform the self-configuration according to default values, load the necessary modules, etc.) and **@ComponentScan** (information that it has to scan the project for annotations regarding entity, repository, service and controller and load them)), thus informing that a given class can be a starting class for Spring, and contains a basic configuration.

Attention! It is best to use the distribution of classes and packages as in the example application, in the case of placing classes in different packages, it may be necessary to define an additional parameter in **ComponentScan** - exactly indicate packets to be scanned.
    
Inheritance from the **SpringBootServletInitializer** class and the method

.. code:: java

    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
        return application.sources(SpringBootWebApplication.class);
    }
    
they are used to ensure that our application can be successfully saved and run as **WAR** file. 

To start the service, just right-click on the class **SpringBootWebApplication.java** and select **Run**. Spring Boot starts embedded Tomcat for us and uploads applications there so that we can focus on creating code instead of worrying about technical details.

Tomcat embedded in spring starts by default on port **8080**.

Controller
-----------

A controller is a class responsible for communication with the outside world (data connections with a view). At this point, we will define the REST API, and the manner of responding to communication with external entities.

We put the **@RestController** annotation in front of the controller class name.

In addition, we can define an annotation in the class    

.. code:: java
    
    @RequestMapping("/api")
    
That will cause all pre-defined paths to be prefixed with **"/api"**. 

We define specific API methods by annotations. The name of the annotation indicate the HTTP method.

.. code:: java
    
    @GetMapping(value = "/products", produces = MediaType.APPLICATION_JSON_VALUE)
    
means a set mapping to the URI of our application. ie. if the root address of our site is **http://localhost:8080/myApp**, then in order to download our data we will have to provide such address: **http://localhost:8080/myApp/api/products**. 

Spring uses **Jackson** to serialize and deserialize data.
    
Parameters of the method are the parameters from the header and the body of the HTTP query as well as the query path. If we want to read data from URL path, we will use the parameter definition annotation **@PathVariable** and the name we associate with the name with the value parameters placed in the brackets.    

.. code:: java
    
    @GetMapping(value = "/product/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
    public Product getByPublicId(@PathVariable("id") Integer publicId)
    
In the case when we pass data through the HTTP query parameter, we use the **@RequestParam** annotation and the name of the parameter as it will be in the HTTP message.

.. code:: java

    @GetMapping(value = "/product", produces = MediaType.APPLICATION_JSON_VALUE)
    public Product getByParamPublicId(@RequestParam("id") Integer publicId) {
    
If we want to read the body of an HTTP query, we use the **@RequestBody** annotation. In addition, we can specify elements such as @Valid and @NotNull, which check the content of the body of the method (because any content may appear anyway).    

.. code:: java

    @PostMapping(value = "/product")
    public ResponseEntity<Product> create(@RequestBody @NonNull @Validated(Product.class)
                                                                 Product product) {
       
For output parameters **Iterable<>** is a universal interface representing data collections that we can return. We can also return class objects and specify parameter **produces** to set how to deserialize them or add annotation **@ResponseBody** (says the returned object is for example JSON and writes it to the body of the HTTP message). We can also define standard HTTP messages using the **ResponseEntity<>(HttpStatus.XXX);** or in the response, redirect to another endpoint by using **new RedirectView("/ api / products", true);**. Be careful as RedirectView does not change the HTTP method, i.e. redirecting from DELETE method sends DELETE request to redirected URL.

.. code:: java

    @DeleteMapping(value = "/product/{id}")
    public RedirectView delete(@PathVariable Integer id) {
        productService.deleteProduct(id);
        return new RedirectView("/api/products", true);
    }    
    
Entity
-------

The data model is a class containing classes and fields such as in the case of a Hibernate project and is marked with the annotation **@Entity** in front of the class name.

Reminder: Hibernate needs a no argument constructor in class!

Repository
------------

**Data repositories** are used to manage data (tables) in the spring project. Repositories will define what operations we can perform on our data. We get the basic operations of CRUD (Create, Read, Update, Delete) from Spring, other queries like selecting by chosen fields we have to add by ourself.

To use repositories we need to add Main class annotation **@EnableJpaRepositories** and select path where those repositories can be found.

The simplest repositories are created as interfaces. All code that is needed to perform the action is generated by Spring.

.. code:: java
    
    public interface ProductRepository extends CrudRepository<Product, Integer> 

Defines the simplest repository that inherits the simplest CRUD operations from the spring Crud repository (we do not have to write these queries ourselves).

    | **Product** is class (model of objects) that we want to store in the database. 
    | **Integer** is the primary key for the table.  

List of operations from the CRUD interface:
    | Product save(Product t) - save the task to the database
    | Iterable save(Iterable t) - saving the collection of objects
    | Product findOne(Integer id) - finds the entry with the key given as a parameter
    | boolean exists(Integer id) - check if the entry with the key exists
    | Iterable findAll() - get all entries from the database
    | Iterable findAll(Iterable IDs) - find all elements with keys in the IDs list
    | long count() - count the elements in the table
    | void delete(Integer id) - delete the element with the id key
    | void delete(Product r) - remove the object from the table
    | void delete(Iterable IDs) - delete all objects whose keys are on the IDs list
    | deleteAll() - clear the table

Of course, we can inherit from more than one interface. Please pay attention to **PagingAndSortingRepository** interface facilitating pagination when downloading objects from the database.

We can create SQL queries in Spring in four ways:

    | * "Named" queries
    | * DSL Query 
    | * From method names
    | * @Query Annotation
    
DSL query is for example:

.. code:: java
    
    queryFactory.selectFrom(person)
        .where(
            person.firstName.eq("John"),
            person.lastName.eq("Doe"))
        .fetch();

See more in https://www.baeldung.com/querydsl-with-jpa-tutorial .        
        
Below we present the last two methods:

Define your own queries by:

    | Defining the method in the interface

.. code:: java

    List<Product> findByName(String name); 
    
Spring automatically changes the method to an SQL query (for us) if we follow the appropriate naming convention.
The key phrases are **find ... To, read ... To, and get ... By** we can use field names and logical conjunctions **And** and **Or**.
Here, Spring guesses what to do after the name of the method. You could save the findByName(String name) in a similar way. We can also combine conditions and create names such as findByDoneAndName(Boolean done, String name). Example:

.. code:: java

    public interface PersonRepository extends Repository<User, Long> {
    
        List<Person> findByEmailAddressAndLastname(EmailAddress emailAddress, String lastname);
    
        // Enables the distinct flag for the query
        List<Person> findDistinctPeopleByLastnameOrFirstname(String lastname, String firstname);
        List<Person> findPeopleDistinctByLastnameOrFirstname(String lastname, String firstname);

        // Enabling ignoring case for an individual property
        List<Person> findByLastnameIgnoreCase(String lastname);
        // Enabling ignoring case for all suitable properties
        List<Person> findByLastnameAndFirstnameAllIgnoreCase(String lastname, String firstname);

        // Enabling static ORDER BY for a query
        List<Person> findByLastnameOrderByFirstnameAsc(String lastname);
        List<Person> findByLastnameOrderByFirstnameDesc(String lastname);
    }
    
More examples and keywords that you can use:

    | http://www.thejavageek.com/2017/02/25/spring-data-jpa-query-methods/
    | https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#jpa.query-methods.query-creation

The second way is to define the query yourself using the **@Query** annotation before the method name in the interface.

.. code:: java

    @Query("select u from User u where u.age = ?1")
    List<User> findUsersByAge(int age);

    @Query("select u from User u where u.firstname = :#{#customer.firstname}")
    List<User> findUsersByCustomersFirstname(@Param("customer") Customer customer);
    
Query parameters are defined by the **@Param** annotations or by the parameter number **?1** in the definition.  
    
Service
---------

As we noted above, repository defines direct access to data through database queries. From an engineering point of view, the repository therefore contains no logic but simple database queries. If we need to pack our interaction with the database through business logic, we will use the so-called **service** - an intermediate layer between data and view.

In order to define the site before the name of the class, we put the **@Service** annotation.

Spring uses the so-called mechanism of dependency injection. This means that the spring engine is responsible for managing the components and transferring them to other components so that they can be used together. The key annotation here is

.. code:: java
    
    @Autowired

It tells spring that we want to get a component object defined in the system to be available in this class.

For example, in the case of a website, we will need the Repository component on which we want to perform queries.

.. code:: java

    @Autowired
    private ProductRepository productRepository;
    
This annotation will cause that in the Spring service object, the productRepository variable will be initialized in a way "for us" and we will be able to continue using it.

More precisely, what we define is an interface that we can use in our class and Spring injects into it the implementation of this interface. Hence, to create a website, we define the interface:

.. code:: java

    public interface ProductService 

with method headers. If we want to use this class in a different class we will define it as 

.. code:: java

    @Autowired 
    private ProductService productService;

The implementation of the methods will be included in the **ProductServiceImpl** class. 

.. code:: java
    
    @Service
    public class ProductServiceImpl implements ProductService 
    
Tasks
--------

Attention!! If we run the spring through the main class with Intellij, our service will be available at **http://localhost:8080/** directly, because within the built-in Tomcat there is only one application so we do not have to give the name of the project. Therefore, if you would like to use a postman to communicate with the service, use only this address + path within the project.

.. class:: tag

    Task 
    
*Swagger 2 is an open-source project for RESTful APIs.*
Swagger provides a very simple and clear description of our API for other developers, it also generates automatically from our code and allows testing of our endpoints. In order to add Swagger to the project please add it to POM:    

.. code:: xml

        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger2</artifactId>
            <version>2.6.1</version>
        </dependency>
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger-ui</artifactId>
            <version>2.6.1</version>
            <scope>compile</scope>
        </dependency>
        
and to the main class 

.. code:: java

    @Bean
    public Docket productApi() {
        return new Docket(DocumentationType.SWAGGER_2)
                .select().apis(RequestHandlerSelectors.basePackage("com.pracownia.spring.controllers"))
                .build();
    }
    
and **@EnableSwagger2** annotation before the class name.

Run the class **SpringBootWebApplication** check in the browser for **http://localhost:8080/swagger-ui.html#/** if swagger works.    
    
.. class:: tag

    Task 
    
When you try to list all products there is an infinity loop on serialization. You can deal with this problem by uncommenting **JSONIdentityInfo** annotation in class **Product** and **Seller** or by deleting from **Seller** methods **setProductsOb()** and **getProductsOb()**. Then product will "see" sellers but sellers would not "see" products.   

Check how the serialization looks like in both scenarios.
  
.. class:: tag

    Task

Try to add a JSON with an object which is not a proper Product object, compare it to non validated put.
  
.. class:: tag

    Task
    
See how the date object are serialized (call GET for all objects).

Add your own definition of Jackson to the project.

Add to POM:

.. code:: java

  <dependency>
      <groupId>com.fasterxml.jackson.datatype</groupId>
      <artifactId>jackson-datatype-joda</artifactId>
      <version>2.0.4</version>
  </dependency>


And to the main class **SpringBootWebApplication**:
        
.. code:: java

    @Bean
    public MappingJackson2HttpMessageConverter mappingJackson2HttpMessageConverter() {
        MappingJackson2HttpMessageConverter jsonConverter = new MappingJackson2HttpMessageConverter();
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.registerModule(new JodaModule());
        objectMapper.enable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        jsonConverter.setObjectMapper(objectMapper);
        return jsonConverter;
    }

see how date is serialized now (restart the application and call GET for all objects).
    
.. class:: tag

    Task
    
A good practice when creating objects in REST API is to return the path to the object, or the whole object in the response (as confirmation / to provide the user with the id of the created object). Replace the response to the POST query with the following line:


.. code:: java

    ResponseEntity.ok().body(product);
    
See the differences in the answers between POST and PUT.
    
   
.. class:: tag

    Task 
    
Uncomment controller **SellerController** for loading, adding and deleting Sellers.

Uncomment **SellerRepository**

Uncomment service for seller.
    
As you can see the Seller's object "pulls" all information about products. Because of this, the object can quickly become very big, which we do not want. To prevent this, we can store only information about the **public_id** of the product in the seller. In this case, the Seller should have a field that is a list of Strings. To create simple type lists in Hibernate, use the **@ElementCollection** annotation.    

Add given entry in the Seller's model:

.. code:: java

    @ElementCollection
    @CollectionTable(name = "products")
    @Column(name = "product_id")
    private List<String> products = new ArrayList<>();

and make other necessary corrections. 
    
.. class:: tag

    Task 
    
**>** Add a query to the seller repository that searches for the seller by name.


**>** Add a question to the repository Seller searching for the seller who sells the most products.

.. code:: java

    @Query("select count(*) from Seller s join s.products p where s.id = ?1")
    Integer countProductsById(Integer id);

**>** Add a question to the Seller repository that searches for the seller who sells the products with the highest cost.

.. code:: java

    @Query("select p from Seller s join s.products p where s.id = ?1")
    List<Product> getProductsById(Integer id);
       
.. class:: tag

    Task 
    
Add to the Product repository : PagingAndSortingRepository.

.. code:: java

    public interface ProductRepository extends CrudRepository<Product, Integer>, PagingAndSortingRepository<Product, Integer> {

Add a product paginated query in service (note that now findAll can take the PageRequest parameter - page number, page size). Note pages are numbered from **zero**!

.. code:: java

    @Override
    public Iterable<Product> listAllProductsPaging(Integer pageNr, Integer howManyOnPage) {
        return productRepository.findAll(PageRequest.of(pageNr,howManyOnPage));
    }

Add controller:

.. code:: java

    @GetMapping(value = "/products/{page}", produces = MediaType.APPLICATION_JSON_VALUE)
    public Iterable<Product> list(@PathVariable("page") Integer pageNr,@RequestParam("size") Optional<Integer> howManyOnPage) {
        return productService.listAllProductsPaging(pageNr, howManyOnPage.orElse(2));
    }

Pay attention to the size parameter, which is optional (and if no value is given, set it to 2).
    
.. class:: tag

    Task 
    
Change the query **seller/{id}** to return XML, not JSON. To do this, set the Media Type:

.. code:: java

    @GetMapping(value = "/seller/{id}", produces = MediaType.APPLICATION_ATOM_XML_VALUE)
    @ResponseBody
    public Seller getByPublicId(@PathVariable("id") Integer publicId) {
        return sellerService.getSellerById(publicId);
    }

and add dependence to POM

.. code:: xml

    <dependency>
        <groupId>com.fasterxml.jackson.dataformat</groupId>
        <artifactId>jackson-dataformat-xml</artifactId>
    </dependency>
    
.. [*] Wykorzystano materiały z:

http://silversableprog.blogspot.com/2015/11/javaspring-boot-jak-rozpoczac-pisanie-w.html

http://blog.mloza.pl/spring-boot-szybkie-tworzenie-aplikacji-web-w-javie/

http://blog.mloza.pl/spring-boot-interakcja-z-baza-danych-czyli-spring-data-jpa/#more-70

https://www.callicoder.com/spring-boot-rest-api-tutorial-with-mysql-jpa-hibernate/

https://spring.io/guides/tutorials/bookmarks/

https://fastfoodcoding.com/tutorials/1505105199524/crud-operations-using-spring-boot-jpa-hibernate-postgresql

https://shakeelosmani.wordpress.com/2017/02/13/step-by-step-spring-boot-hibernate-crud-web-application-tutorial/

https://github.com/Zianwar/springboot-crud-demo

https://kobietydokodu.pl/09-spring-mvc/

https://www.ibm.com/developerworks/library/j-spring-boot-basics-perry/index.html
