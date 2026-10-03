=======================
Programming Laboratory
=======================

--------------------
Application servers
--------------------

Apache Tomcat
-------------

Apache Tomcat - web application server developed as part of the Apache project.

The Apache Tomcat® software is an open source implementation of the Java Servlet, JavaServer Pages, Java Expression Language and Java WebSocket technologies. This is one of the most popular Web containers. Tomcat is used in such JEE (J2EE) application servers as Apache Geronimo. It is also a very popular container for standalone applications (not requiring a full application server) written in the Spring Framework environment. 

Tomcat's documentation: `<https://tomcat.apache.org/tomcat-8.5-doc/introduction.html>`_

Key terms:

**Document root** - the main directory of the web application where its resources are located

**Context path** - the relative path to the server resources.

For example, if we put a web application in the /webapps/myapp directory, then we can get to it via the URL link http:/localhost/myapp, and its context path will be equal to /myapp.

**WAR** - is an extension of the package file containing the web application in ZIP format (short for the Web Archive). Typically, Java applications are packaged as WAR before deployment. Usually this file is created by the programming environment.

After uploading the WAR file, Tomcat unpacks it and saves its file in a new subdirectory in the webapps directory.

.. class:: tag

    Exercise 1 - download Tomcat

Download the Tomcat binary distribution version 8.5 appropriate for the system you are using from the page `<https://tomcat.apache.org/download-80.cgi>`_

 - for Windows, select the package `zip <http://ftp.man.poznan.pl/apache/tomcat/tomcat-8/v8.5.47/bin/apache-tomcat-8.5.47.zip>`_
 - for Linux select packae `tar.gz <http://ftp.man.poznan.pl/apache/tomcat/tomcat-8/v8.5.47/bin/apache-tomcat-8.5.47.tar.gz>`_

Unpack the downloaded package to any place.

After unpacking, you will receive folder **apache-tomcat-8.5.2**.

.. class:: tag

    Exercise 2 - Run the server

Start the Tomcat server using the /bin/startup.[sh|bat]

You should expect something like this:

.. code:: bash

    Using CATALINA_BASE:   /home/marcin/Downloads/apache-tomcat-8.5.35
    Using CATALINA_HOME:   /home/marcin/Downloads/apache-tomcat-8.5.35
    Using CATALINA_TMPDIR: /home/marcin/Downloads/apache-tomcat-8.5.35/temp
    Using JRE_HOME:        /usr
    Using CLASSPATH:       /home/marcin/Downloads/apache-tomcat-8.5.35/bin/bootstrap.jar:/home/marcin/Downloads/apache-tomcat-8.5.35/bin/       tomcat-juli.jar
    Tomcat started. 

.. class:: tag

    Exercise 3 - check

Check if there is a sample application in the /webapps/sample/ directory.

Check if the application works. It should be available at: http://localhost:8080/sample/

If not, copy from the page

    | https://tomcat.apache.org/tomcat-6.0-doc/appdev/sample/
    
file **Sample.war** file to the **/webapps/** directory

Restart Tomcat running 

.. code:: bash
    
    shutdown.[sh|bat]
    
.. code:: bash
    
    startup.[sh|bat]

Check if both `JSP page <http://localhost:8080/sample/hello.jsp>`_ as well as `Servlet <http://localhost:8080/sample/hello>`_ works.

If "JSP page" does not work, then most likely you have to set the **JAVA_HOME** system variable to the JDK Java 8 path:

.. code:: bash
    
    tomek@tomek-Lubuntu:~$ java -version
    openjdk version "9-internal"
    tomek@tomek-Lubuntu:~$ which java
    /usr/bin/java
    tomek@tomek-Lubuntu:~$ realpath /usr/bin/java
    /usr/lib/jvm/java-9-openjdk-amd64/bin/java
    tomek@tomek-Lubuntu:~$ ls /usr/lib/jvm/
    java-1.8.0-openjdk-amd64  java-1.9.0-openjdk-amd64  java-8-openjdk-amd64  java-9-openjdk-amd64
    tomek@tomek-Lubuntu:~$ export JAVA_PATH=/usr/lib/jvm/java-8-openjdk-amd64/

Turn Tomcat off and on again and check if JSP started working correctly after setting **JAVA_HOME**:

Restart Tomcat running 

.. code:: bash
    
    shutdown.[sh|bat]
    
.. code:: bash
    
    startup.[sh|bat]

If everything works, you should also have access to Tomcat's documentation, which is provided with it and by default provided by the server itself: `<http://localhost:8080/docs/index.html>`_

Access configuration
-----------------------

Tomcat allows you to control access to applications launched on the server. Applications may (but do not have to) use the authentication method provided by Tomcat.

To allow access control, Tomcat uses a user database called *Realm*.

*Realm* contains a list of usernames, their passwords and roles.

Roles allow granting user rights to groups. They are similar to Linux *groups*  of users.

One user can have several roles assigned.

.. class:: tag

    Exercise 4 - configure access

Go to the default page provided with Tomcat: `<http://localhost:8080/>`_

Try to view the server status by clicking on `"Server Status" <http://localhost:8080/manager/status>`_

A window asking for the username and password should appear.

For security reasons, Tomcat has no default users defined.

The roles that allow access to the Manager application are explained here: http://localhost:8080/docs/manager-howto.html#Configuring_Manager_Application_Access

When editing the /conf/tomcat-users.xml file, add the "guest" user, assign a password to it (it can be empty) and add the "manager-status" role:

.. code:: xml

    <tomcat-users xmlns="http://tomcat.apache.org/xml"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://tomcat.apache.org/xml tomcat-users.xsd"
              version="1.0">
    <!--
      NOTE:  By default, no user is included in the "manager-gui" role required
      to operate the "/manager/html" web application.  If you wish to use this app,
      you must define such a user - the username and password are arbitrary. It is
      strongly recommended that you do NOT use one of the users in the commented out
      section below since they are intended for use with the examples web
      application.
    -->
      <user username="guest" password="" roles="manager-status"/>

    </tomcat-users>

Try once again to log in to the application `"manager/status" <http://localhost:8080/manager/status>`_.

.. class:: tag

    Exercise 5a - manage, first step.
    
Manager is an application that allows you to manage Tomcat from the browser.

It is delivered by default launched with Tomcat.

Its part is the `Server Status <http://localhost:8080/manager/status>`_ page that we visited in the previous task.

Try to visit the manager's website: `<http://localhost:8080/manager/html>`_

Edit the /conf/tomcat-users.xml file again this time adding the **admin** user and assigning it a role that grants access to the manager page (what role should it have?).

Check if you have access to the manager after logging in as an admin.

If you are logged in as guest, try another browser or restart your browser (the whole application not only the tab).    

.. class:: tag
    
    Exercise 5b - manage, second step.
    
When we set up our server, we do not want users to have access to the sample applications provided with Tomcat, so it's worth turning them off.

One of such applications is the "sample" application that we opened in task 3. (`<http://localhost:8080/sample/>`_)
We will now try to disable this application.

Go to the manager's website: `<http://localhost:8080/manager/html>`_

Stop ("Stop") the "sample" application that you opened in task 3. (`<http://localhost:8080/sample/>`_)

Check if the site is available.

Stop and restart the server and check if the sample application is now available.

Use "Undeploy" to stop and remove our *sample* application.

Stop and restart the server and check if the sample application is now available.

Note that the application has been removed from the /webapps/sample directory and is not in the list of applications in the Tomcat manager.    

.. class:: tag

    Exercise 6 - Add new application to Tomcat
    
Adding new applications ("Deployment") is done automatically after copying them to the directory /webapps/
We can also do it from the Tomcat manager level.

Download files to your local hard drive

    | http://mw.home.amu.edu.pl/zajecia/PRA2017/SimpleServlet.zip

Extract to the directory and start Intellij

Choose **Project -> Open** and find the selected directory.

Select the Maven window to refresh (add a pom file if necessary) and run **clean, install**.

The target directory should appear in the project tree window and the file **SimpleServlet-1.war** should appear in it.

Copy this file to the Tomcat's webapps directory. Check if it works by going to `<http://localhost:8080/SimpleServlet-1/hello>`_

If it does not work, enter the manager again, select **WAR file to deploy** by providing the above-mentioned file.

.. class:: tag

    Exercise 7 - monitor

Look at the logs in /logs

Examine catalina.out file content.


.. class:: tag

    Exercise 8 - crash

Add to application line 

.. code:: java

    throw new OutOfMemoryError("blad");

Build application with maven and deploy on the server. Run the application. See if you can find an error in the logs.

.. class:: tag

    Exercise 9 - ports

By default, Tomcat works on port **8080**. If any other process already occupies this port then we get an error when starting the server.

To change the port enter the settings in the file **server.xml** located in /conf/server.xml.

Change port to **8081**, run Tomcat for the second time. Check in the browser whether applications are running on port 8081? Check what has happened in the logs.

Change ports in the **server.xml** file that need to be changed.

Re-start tomcat so that there are two separate instances.   

.. class:: tag
    
    Exercise 10 - debugging of the deployed application
    
Turn off Tomcat and turn on using

     | export JPDA_ADDRESS = 8000
     | export JPDA_TRANSPORT = dt_socket
     | /bin/catalina.sh jpda start

On windows:

     | set JPDA_ADDRESS = 8000
     | set JPDA_TRANSPORT = dt_socket
     | bin/catalina.bat jpda start
    
JPDA address is a port for listening when debugging the app running on Tomcat.

In intellij, select **Run -> Debug** then **Edit Configurations**, in the Select pane on the left **plus** and the **Remote** option.

In the newly opened window, change the port to **8000** and click on debug. From that moment on, you are connected to the debugger for a deployed Tomcat application.

Add a breakpoint in the **16th** line of the SimpleServlet.java file and refresh the page. You should get a breakpoint on this line!
