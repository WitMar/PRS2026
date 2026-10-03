.. role:: todo

.. role:: hold

.. role:: raw-latex(raw)
            :format: latex html

==========================================
Programming Laboratory
==========================================

PROJECT
==========

.. class:: tag
    
Project from the topics : JSON + XML + HIBERNATE + SPRING

Create a program that will read and save a specific data model from/to file to/from database.
 
Each person has to think about what type of data he wants to store in the final application (information about people, movies, cars, footballers, computers, etc.). You should model this data by defining the tables, fields and the relationships between them.

20% points: The data must contain **at least 5 tables**, **one OneToOne relationships** and **one OneToMany (or ManyToMany)** relationships.

10% points: Exemplary data requests should be created for the data (preferably useful in the target project). You have to define at least **5 queries**, each query should be a separate method in the code. One of the queries should be **paginated**.

15% points: Please use the date type field in one of the tables - preferably **ZonedDateTime** or **JodaTime**.

15% points: The target design should read and write modeled data from and into **XML** and **JSON** type files (**both types**!) And write / read them from the database. 

20% points: It must also use a database not stored in memory, eg. one of PostgreQSL, MyQSL, ORACLE etc.

20% points: Application should be divided into server part that receive the data and save them in database as well as allow user to download the data from the database. Separate client application should read the data from file and send request to web server as well as receive data from web server.

You do not need to create any menu for the project, execution can be done by defining the appropriate tests method (in test classes!) For scenarios: reading data from XML / JSON file and writing to the database, reading data from the database and writing to XML / JSON files. You must create the appropriate XML / JSON files for the above mentioned tests.

Attention! **Read and write should properly execute in case of providing partial data (some empty fields) and fail if providing incorrect data**.

Deadline for completion and presentation: **04.I.2021**. No postpone is possible.
