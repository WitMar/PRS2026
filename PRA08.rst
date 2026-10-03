=======================
Pracownia Programowania
=======================

------------------------
Spring Boot + Hibernate
------------------------

.. class:: important 

    .. class:: important 

    Uwaga! cały kod znajduje się na gałęzi **SpringHibernateStart** w repozytorium https://github.com/WitMar/PRA2025 . Kod końcowy w gałęzi **SpringHibernateStop**.
       
Jeżeli nie widzisz odpowiednich gałęzi na GitHubie wykonaj **Ctr+T**, a jak to nie pomoże to wybierz z menu **VCS->Git->Fetch**. 

Na tych zajęciach pokażemy sobie jak Hibernate łączy się ze Spring Bootem. Wykorzystamy kod końcowy z zajęć SpringBoot.

Pierwszy element to konfiguracja, która zostaje przeniesiona z pliku **persistence.xml** do pliku **application.yaml**.

.. code:: xml

    spring:
	  jpa:
		properties:
		  hibernate:
            dialect: org.hibernate.dialect.HSQLDialect
            ddl-auto: create
        show-sql: true
      database:
        driverClassName: org.hsqldb.jdbcDriver
      datasource:
        url: jdbc:hsqldb:mem:spring
        username: sa
        password:

Naszym celem będzie zamiana Beana **DataSet** na wywołania zapytań do relacyjnej bazy danych.

.. class:: tag

    Zadanie 
   
Dodaj w głównej klasie SpringApp adnotację "EnableJpaRepositories".

Repository
------------

Do zarządzania danymi (wykonywaniem zapytań na bazie danych) w projekcie springowym służą **repozytoria**. Repozytoria będą definiować jakie operacje możemy wykonać na naszych danych. Podstawowe operacje CRUD (Create, Read, Update, Delete) dostajemy od Springa, inne operacje jak wyszukiwanie po polach musimy dodać sami.

Żeby używać repozytoriów musimy do klasy Main musimy dodać adnotację **@EnableJpaRepositories** i (opcjonalnie) określić ścieżkę, w której się znajdują.

Najprostsze repozytoria tworzone są jako interfejsy. Repozytorium definiujemy osobno dla każdej encji - czyli dla każdej tabeli w bazie. Poprawna implementacja interfejsu, która jest potrzebna do wykonania metod jest generowana przez Springa. 

.. code:: java
    
    public interface ProductRepository extends CrudRepository<Product, Integer> 

Definiuje najprostsze repozytorium, które dziedziczy najprostsze operacje CRUD ze springowego repozytorium Crud (nie musimy sami już pisać tych zapytań). 

    | **Product** to klasa (obiekt) jaki chcemy przechowywać - w bazie danych będzie to tabela, u nas w projekcie jest to klasa modelu. 
    | **Integer** to typ klucza dla tabeli productów.   

Lista operacji z interfejsu CRUD:
    | Product save(Product t) – zapisz produkt do bazy danych
    | Iterable save(Iterable t) – zapisanie kolekcji obiektów
    | Product findOne(Integer id) – znajduje wpis z kluczem podanym jako parametr
    | boolean exists(Integer id) – sprawdź czy wpis z kluczem istnieje
    | Iterable findAll() – pobierz wszystkie wpisy z tabli
    | Iterable findAll(Iterable IDs) – znajdź wszystkie elementy z kluczami na liście IDs
    | long count() – policz elementy w tabeli
    | void delete(Integer id) – usuń element z kluczem id
    | void delete(Product r) – usuń obiekt z tabelki
    | void delete(Iterable IDs) – usuń wszystkie obiekty których klucze znajdują się na liście IDs
    | deleteAll() – wyczyść tabelę

Oczywiście możemy dziedziczyć po więcej niż jednym interfejsie, co będziemy robić za chwilę dodając stronnicowane zapytania.

.. class:: tag

    Zadanie 
    
Dodaj katalog repositories i w nim interface ProductRepository. Zauważ, że dla repository nie mamy adnotacji nad klasą!

package com.pracownia.spring.repositories;


.. code:: java

	import com.pracownia.spring.model.Product;
	import org.springframework.data.repository.CrudRepository;

	public interface ProductRepository extends CrudRepository<Product, Integer> {
    }


Zapytania SQL możemy w Springu tworzyć na 4 sposoby:

    | * Zapytania "nazwane"
    | * Query DSL
    | * Z nazw metod
    | * @Query Annotation
    
DSL to zapytania tworzone w kodzie:

.. code:: java
    
    queryFactory.selectFrom(person)
        .where(
            person.firstName.eq("John"),
            person.lastName.eq("Doe"))
        .fetch();
        
Więcej przykładów na https://www.baeldung.com/querydsl-with-jpa-tutorial .          
    
Poniżej przedstawimy dwa ostatnie sposoby:    

Definiowanie własnych zapytań odbywa się poprzez:
    
    | Zdefiniowanie metody w interfejsie

.. code:: java

    List<Product> findByName(String name); 
    
Spring automatycznie zmienia metodę na zapytanie SQL (za nas) jeżeli stosujemy się do odpowiedniej konwencji nazewniczej.    

Kluczowe frazy to **find…By, read…By, and get…By** możemy do tego używać nazw pól oraz logicznych spójników **And** i **Or**. 

Tutaj Spring domyśla się co ma zrobić po nazwie metody. Można by w podobny sposób zapisać findByName(String name). Możemy również łączyć warunki i tworzyć nazwy takie jak findByDoneAndName(Boolean done, String name). Przykład:

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
    
Więcej przykładowych słów kluczowych w użyciu:

    | http://www.thejavageek.com/2017/02/25/spring-data-jpa-query-methods/
    | https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#jpa.query-methods.query-creation

.. class:: tag

    Zadanie 

Dodaj plik SellerRepository. Usuń Beana i klasę Data z projektu i zamień wywołania korzystające z tego beana w servicach na wywołania metod z repository.

Klasa SellerServiceImpl powinna wyglądać następująco:

.. code:: java

	package com.pracownia.spring.services;

	import com.pracownia.spring.model.DataSet;
	import com.pracownia.spring.model.Seller;
	import com.pracownia.spring.model.Product;
	import com.pracownia.spring.repositories.ProductRepository;
	import com.pracownia.spring.repositories.SellerRepository;
	import org.springframework.beans.factory.annotation.Autowired;
	import org.springframework.stereotype.Service;

	import java.util.ArrayList;
	import java.util.List;
	import java.util.Optional;
	import java.util.Random;
	import java.util.stream.Collectors;

	@Service
	public class SellerServiceImpl implements SellerService {

    @Autowired
    SellerRepository data;

    @Autowired
    ProductRepository dataPr;

    @Autowired
    ProductService productService;

    @Override
    public Iterable<Seller> listAllSellers() {
        return data.findAll();
    }

    @Override
    public Optional<Seller> getSellerById(Integer id) {
        return data.findById(id);
    }

    @Override
    public Seller saveSeller(Seller seller) {
        data.save(seller);
        return seller;
    }

    @Override
    public void deleteSeller(Integer id) {
        data.deleteById(id);
    }

    @Override
    public List<Seller> getByName(String name) {
        return data.findByName(name);
    }

    @Override
    public Integer getNumberOfProducts(Integer id) {
        return  data.countProductsById(id);
    }

    @Override
    public Optional<Seller> getBestSeller() {
        double max = 0;
        int maxId = 0;
        Iterable<Seller> sellers = data.findAll();
        for(Seller s : sellers) {
            double sum = 0.0;
            List<Product> products = dataPr.findBySellerId(s.getId());
            for(Product pid : products) {
                sum += pid.getPrice().doubleValue();
            }
            if (sum > max) {
                max = sum;
                maxId = s.getId();
            }
        }
        return data.findById(maxId);
    }
	}



Jeżeli podaliśmy w repository metodę findBySeller(Seller seller) to powinniśmy zobaczyć błąd. W tym wypadku hibernate nie radzi sobie dobrze z zapytaniem, w przypadku joinów łatwiej będzie nam wykorzystać drugi sposób definiowania zapytań.

Drugi sposób to zdefiniowanie zapytania samemu korzystając z adnotacji **@Query** przed nazwą metody w interfejsie. Zapytania definiujemy w znanym z Hibernate standardzie JPQL, który jest wzorowany na HQL i w większości jest jego podzbiorem.

.. code:: java

    @Query("select u from User u where u.age = ?1")
    List<User> findUsersByAge(int age);

    @Query("select u from User u where u.firstname = :#{#customer.firstname}")
    List<User> findUsersByCustomersFirstname(@Param("customer") Customer customer);
    
Parametry zapytań są definiowane poprzez adnotacje **@Param** lub poprzez numer parametru w definicji **?1**.    

.. class:: tag

    Zadanie 
    
Dodaj dla ProductRepository zapytanie:


.. code:: java

    @Query("select p from Product p join p.sellers s where s.id = ?1")
    List<Product> findBySellerId(Integer id);    
    
Uruchom program, dodaj dane za pomocą swaggera i wywołaj endpoint **/api/seller/best**.    

Zapytania join są najtrudniejsze do wykonania, poniżej przykłady dwóch różnych implementacji join dla połączenia Product - Seller :
   
**>** Zapytanie wyszukujące produkty które sprzedaje sprzedawca.

.. code:: java

    @Query("select p from Seller s join s.productsOb p where s.id = ?1")
    List<Product> getProductsById(Integer id);
    
**>** Druga wersja tego zapytania (przy wykorzystaniu tablicy productId):

.. code:: java

    @Query("select p from Seller s join s.products ps, Product p where p.productId = ps.id and s.id = ?1")
    List<Product> getProductsById(Integer id);  
    
.. class:: tag

    Zadanie 
        
Sprawdź czy endpoint **/api/seller/products/{id}** zwraca to co powinien.    
    
**>** Dodaj do repository Seller zapytanie podające liczbę produktów danego sprzedawcy

.. code:: java

    @Query("select count(*) from Seller s join s.productsOb p where s.id = ?1")
    Long countProductsObById(Integer id);  
    
Stronnicowanie
----------------
    
.. class:: tag

    Zadanie 
    
Dodaj do Product repository : PagingAndSortingRepository. 

.. code:: java

    public interface ProductRepository extends CrudRepository<Product, Integer>, PagingAndSortingRepository<Product, Integer> {

Dodaj do serwisu zapytanie stronnicowane o produkty (zwróć uwagę, że teraz findAll może przyjmować parametr PageRequest - nr strony, wielkość strony). Uwaga strony są numerowane od **zera**!   

.. code:: java

    @Override
    public Iterable<Product> listAllProductsPaging(Integer pageNr, Integer howManyOnPage) {
        return productRepository.findAll(PageRequest.of(pageNr,howManyOnPage));
    }

Dodaj kontroler:

.. code:: java

    @GetMapping(value = "/products/{page}", produces = MediaType.APPLICATION_JSON_VALUE)
    public Iterable<Product> list(@PathVariable("page") Integer pageNr,@RequestParam(value = "size",required = false) Optional<Integer> howManyOnPage) {
        return productService.listAllProductsPaging(pageNr, howManyOnPage.orElse(2));
    }

Zwróć uwagę na parametr size, który jest opcjonalny (i przy nie podaniu żadnej wartości ustawiamy go jako 2).


Criteria Query
-----------------

Istnieje trzeci sposób tworzenia zapytania w Hibernate, który nazywa się Criteria Query. Możemy go wykorzystać w repozytorium ale musimy wtedy zbudować własne zapytanie w oparciu o EntityManager.

Musimy dodać interface

.. code:: java

	package com.pracownia.spring.repositories;

	import com.pracownia.spring.model.Product;

	import java.util.List;

	public interface ProductRepositoryCustomInterface {
    
			List<Product> listAffordableProducts(Integer price);
	}

Oraz implementację

.. code:: java

	package com.pracownia.spring.repositories;

	import com.pracownia.spring.model.Product;
	import jakarta.persistence.EntityManager;
	import jakarta.persistence.criteria.CriteriaBuilder;
	import jakarta.persistence.criteria.CriteriaQuery;
	import jakarta.persistence.criteria.Predicate;
	import jakarta.persistence.criteria.Root;
	import org.springframework.beans.factory.annotation.Autowired;
	import org.springframework.stereotype.Component;
	
	import java.util.ArrayList;
	import java.util.List;
	
	@Component
	public class ProductRepositoryCustom implements ProductRepositoryCustomInterface {

    @Autowired
    EntityManager em;

    @Override
    public List<Product> listAffordableProducts(Integer price) {
        CriteriaBuilder cb = em.getCriteriaBuilder();
        CriteriaQuery<Product> cq = cb.createQuery(Product.class);

        Root<Product> product = cq.from(Product.class);
        List<Predicate> predicates = new ArrayList<>();

        predicates.add(cb.lessThanOrEqualTo(product.get("price"), price));

        cq.where(predicates.toArray(new Predicate[0]));

        return em.createQuery(cq).getResultList();
		}
	}


Możemy teraz użyć go w service i controlerze.

.. code:: java

	@Autowired
    ProductRepositoryCustom productRepositoryWithCQ;

    @Override
    public Iterable<Product> listAllBelowPrice(Integer price) {
        return productRepositoryWithCQ.listAffordableProducts(price);
    }

.. code:: java
    
    @GetMapping(value = "/products/promo/{price}", produces = MediaType.APPLICATION_JSON_VALUE)
    public Iterable<Product> list(@PathVariable("price") Integer price) {
        return productService.listAllBelowPrice(price);
    }    
    
Audytowanie danych w bazie danych
====================================

Audytowanie danych w bazie danych polega na śledzeniu i zapisywaniu zmian w danych, 
takich jak tworzenie, aktualizacja czy usuwanie rekordów. Celem audytowania jest zapewnienie 
możliwości odtworzenia historii zmian dla danego obiektu lub rekordu oraz wspieranie procesów 
kontroli, zgodności z regulacjami (compliance) i debugowania.

Typowe zastosowania audytu:
- Śledzenie zmian danych użytkowników
- Odzyskiwanie przypadkowo zmodyfikowanych lub usuniętych informacji
- Analizowanie działań użytkowników w systemie
- Spełnienie wymogów prawnych dotyczących przechowywania historii zmian

Hibernate Envers
=================

Hibernate Envers to moduł biblioteki Hibernate, który automatycznie zarządza audytem danych.
Envers zapisuje zmiany w specjalnych tabelach audytowych i umożliwia łatwe odczytywanie
wersji historycznych encji.

Jak działa Envers:
- Dla każdej audytowanej encji tworzona jest osobna tabela (np. ``user_AUD``).
- Każda zmiana (INSERT, UPDATE, DELETE) jest rejestrowana w tabeli audytowej.
- Zapytania mogą być kierowane na konkretne wersje danych.

Przykład użycia Hibernate Envers
=================================

Konfiguracja
------------

Aby włączyć Envers, należy dodać odpowiednią zależność Maven:

.. code-block:: xml

    <dependency>
        <groupId>org.hibernate.orm</groupId>
        <artifactId>hibernate-envers</artifactId>
        <version>6.4.4.Final</version> <!-- przykład wersji -->
    </dependency>

Audytowanie encji
-----------------

Oznacz encję adnotacją ``@Audited``:

.. code-block:: java

    import jakarta.persistence.Entity;
    import jakarta.persistence.Id;
    import org.hibernate.envers.Audited;

    @Entity
    @Audited
    public class User {
        @Id
        private Long id;

        private String username;

        private String email;

        // Gettery i settery
    }

Tabela audytowa
---------------

Hibernate Envers automatycznie stworzy tabelę ``User_AUD``, zawierającą:
- Kolumny odpowiadające polom z encji ``User``
- Kolumnę ``REV`` wskazującą na identyfikator rewizji
- Kolumnę ``REVTYPE`` określającą typ operacji (0 = dodanie, 1 = modyfikacja, 2 = usunięcie)

Pobieranie historii zmian
--------------------------

Do pobierania wersji obiektów służy ``AuditReader``:

.. code-block:: java

    import org.hibernate.envers.AuditReader;
    import org.hibernate.envers.AuditReaderFactory;

    // Wewnątrz transakcji Hibernate
    AuditReader auditReader = AuditReaderFactory.get(entityManager);

    // Pobierz wszystkie rewizje danego użytkownika
    List<Number> revisions = auditReader.getRevisions(User.class, userId);

    // Pobierz konkretną wersję użytkownika
    User userAtRevision = auditReader.find(User.class, userId, revisionNumber);

.. class:: tag

    Zadanie 
    
Zobacz jakie tabele tworzą audyty i jak wygląda tworzenie danych przy włączonym audytowaniu.    
    

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

https://sites.google.com/site/telosystutorial/springmvc-jpa-springdatajpa/presentation/architecture
