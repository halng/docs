# JAVA - OCP

- This docs is my note for my OCP exam
- Book: OCP - Oracle Certified Professional Java SE 17 Developer Study Guide
- This docs will cover all OCP's exam topic.

## Exam topic

### 1. Handling date, time, text, numeric and boolean values

- Use primitives and wrapper classes including Math API, parentheses, type promotion, and casting to evaluate arithmetic and boolean expressions
- Manipulate text, including text blocks, using String and StringBuilder classes
- Manipulate date, time, duration, period, instant and time-zone objects using Date-Time API

### 2. Controlling Program Flow

- Create program flow control constructs including if/else, switch statements and expressions, loops, and break and continue statements

### 3. Utilizing Java Object-Oriented Approach

- Declare and instantiate Java objects including nested class objects, and explain the object life-cycle including creation, reassigning references, and garbage collection
- Create classes and records, and define and use instance and static fields and methods, constructors, and instance and static initializers
- Implement overloading, including var-arg methods
- Understand variable scopes, use local variable type inference, apply encapsulation, and make objects immutable
- Implement inheritance, including abstract and sealed classes. Override methods, including that of Object class. Implement polymorphism and differentiate object type versus reference type. Perform type casting, identify object types using instanceof operator and pattern matching
- Create and use interfaces, identify functional interfaces, and utilize private, static, and default interface methods
- Create and use enumerations with fields, methods and constructors

### 4. Handling Exceptions

- Handle exceptions using try/catch/finally, try-with-resources, and multi-catch blocks, including custom exceptions

### 5. Working with Arrays and Collections

- Create Java arrays, List, Set, Map, and Deque collections, and add, remove, update, retrieve and sort their elements

### 6. Working with Streams and Lambda expressions

- Use Java object and primitive Streams, including lambda expressions implementing functional interfaces, to supply, filter, map, consume, and sort data
- Perform decomposition, concatenation and reduction, and grouping and partitioning on sequential and parallel streams

### 7. Packaging and deploying Java code and use the Java Platform Module System

- Define modules and their dependencies, expose module content including for reflection. Define services, producers, and consumers
- Compile Java code, produce modular and non-modular jars, runtime images, and implement migration using unnamed and automatic modules

### 8. Managing concurrent code execution

- Create worker threads using Runnable and Callable, manage the thread lifecycle, including automations provided by different Executor services and concurrent API
- Develop thread-safe code, using different locking mechanisms and concurrent API
- Process Java collections concurrently including the use of parallel streams

### 9. Using Java I/O API

- Read and write console and file data using I/O Streams
- Serialize and de-serialize Java objects
- Create, traverse, read, and write Path objects and their properties using java.nio.file API

### 10. Accessing databases using JDBC

- Create connections, create and execute basic, prepared and callable statements, process query results and control transactions using JDBC API

### 11. Implementing Localization

- Implement localization using locales, resource bundles, parse and format messages, dates, times, and numbers including currency and percentage values

## Note for the book

Assessment Test

- First time 16/30 🥲

### Chapter 1: Building blocks

1. ***Understading the class structure***
    - **Fields**: more generally known as variables. -> hold the state of the program
    - **Methods**: often called function or procedures -> operate on thatb state

    ```java
    public class Animals {
        String name; // variable
        public Animals(){} // contructor
        public Animals(String name){ // another contructor
            this.name = name;
        }

        public void setName(String newName) { // method
            this.name = newName;
        }

        public String getName() { // another method
            return this.name;
        }

        // this is single-line comment
        /**
         * This is syntax of block comment
         * and so on... 
         */
    }
    ```

    - **Classes and source files**:
        - *top-level type*: is a data structure that can be defined independently within a source file.
            - is often public
            - if don't have a public type, it needs to match filename.

2. ***Writing a `main()` method***
    - The `main()` method lets the `JVM` call out code.  

        ```java
            public class Animals {
                public static void main(String[] args) {
                    System.out.println("Hello World");
                }
            }
        ```

    - Rule for the file name:
        - Each file can contain only one `public` class
        - The filename must match the class name, including case, and have a .java extension
        - If the java class in an entry point for the program, It must contain a vaid `main()` methods

3. ***Understanding package declarations and imports***
    - `Package`: Java classes are grouped into packages.
    - `Wildcards`: classes in the same package are oftern imported together. We can use a shortcut to `import` all the classes in a package

    ```java
    import java.util.*; // imports java.util.Random among other things
    public class NumberPicker {
        public static void main(String[] args) {
            Random r = new Random();
            System.out.println(r.nextInt(10));
        }
    }
    ```

    - `Naming conflicts`: One of the reasons for using packages is so that class names don't have to be unique across all of Java. That means you'll sometimes want to import a class that can be found in multiple places.
    For example:

    ```java
    import java.util.*;
    import java.sql.*;

    public class Conflicts {
        Date date;  // conflict -> cause have 2 class Date in two package imported -> compiler error
        //some code
    }
    ```

    But sometimes, we want to use Date from two different packages. -> import statemaent and use the other's *fully qualified* class name

    ```java
    public class Conflicts {
        java.util.Date utilDate;
        java.sql.Date sqlDate;
        //some code
    }

    // now it compile success
    ```

    | Element | Example | Required ? | Where does it go ? |
    | - | - | - | - |
    Package declaration | package abc; | No | first line in the file (Excluding comments or blank lines)
    | import statements | import java.util.* | No | immediately after the package (if present)
    | `top-level type` declaration | public class Animals | Yes | immediately after the import (if any)
    | field declarations | int value; | No | Any `top-level` element within a class
    | method declarations | void method() | No | Any top-level element within a class

    ```java
    package abc; // package
    import java.util.*; // import

    public class Animals {
        double weight; // field
        public double getWeight() { // method
            return this.weight;
        }
        double height; // another fields
    }
    ```

4. **Creating Objects**

> Out program wouldn't be able to do any thing useful if we didn't have the ability to create new objects. Remember that an objects is an instance of a class. In the following sections, we look at constructors, object fields, instance initializers, and the other in which values are initialized.

- Calling Constructors

```java
Park p = new Park()

// <Declare the type> <variable name> = new  <object's contructors>


// Contructor example:
public class Park {
    public Park(){}
}
```

- The constructor:
  - Have a name matches the name of the class
  - No return type
  - The purpose is to **initialize field**

  - For most classes, if don't have a code for constructor - the `compiler` will supply a **do noting** default constructor.

- Reading and writing member fields

### Chapter 2: Operators

### Chapter 3: Making Decisions

### Chapter 4: Core APIs

### Chapter 5: Methods

### Chapter 6: Class Design

### Chapter 7: Beyond Classes

### Chapter 8: Lambdas and Functional Interfaces

### Chapter 9: Collections and Generics

### Chapter 10: Streams

### Chapter 11: Exception and Localiza~tion

### Chapter 12: Modules

### Chapter 13: Concurrency

### Chapter 14: I/O

### Chapter 15: JDBC
