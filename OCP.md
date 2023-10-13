# Oracel Certificate Professional - Java 17
- Link: https://mylearn.oracle.com/ou/learning-path/java-explorer/79726
- Course name: Java Explorer

---

> ***Overview***
- Java is cross-platform - because each java program only needs to be written and compiled once
- No platform-specific changs has to be applied to the source-code
- Java programs are executed within a Java Virtual Machine - JVM

```
code -> compile -> byte code -> deploy
```

> ***Java Ecosystem***
- Java Card
- Java ME Micro-Edition
- Java SE Standard-Edition
- Java MP Micro-Profile
- Java EE Enterprise-Edition

> ***Java Language***
- `class`: 
    - Basic units of code
    - Describe data and logic of program
- `package`:    
    - Intermediate logical code aggregation
    - Group of classes
- `module` - java 9
    - High-level physical code aggregation
    - Group of packages
- `syntax`
    - Java code is grouped into classes
    - Classes contain methods and variables that fulfill their purpose
    ```java
    public class Car {
        private double v; // variable

        public Car() {} // constructor

        public void run() { // method
            System.out.Println("Car is running")
        }

        public void stop() { // method
            System.out.Println("Car is stopping")
        }
    }
    ```
- `Exception Handling`
    - Interrupt normal program execution when problems occur.
    - Decide what your program should do in case of an error
    - Write flexible code that can handle adverse circumstances
    ```java
    public class LoadData {
        public void load(Path filePath) {
            try {
                Files.readLines(filePath); // file path doesn't exits
            } catch(IOException e) {
                // error corrections
            }
        }
    }
    ```

> ***Java Design***
- `Classes` and `Objects`
    - Class represents a type of things or a concept
    - Object is an instance - a specific example of a class

    ```java
    class Car {
        //variables
        ...
        // constructor
        ...
        // method
    }

    class App {
        public static void main(args) {
            Car toyota = new Car();
        }
    }

    /*
    * Car is a class
    * toyota is a object
    */
    ```
- `Inheritance`
    - Reuse attributes and behaviors across the class hierarchy
    - Top level classes contain generic code reused by the descendants

- Achieve flexible design:
    - `Interfaces`
    - `Enumerations`
    - `Generics`

> ***Java APIs***
- Java Arrays and Colelctions
     - Java array is a simple group of elements
     ```java
     {1, 2, 3, 4,}
     ```
     - The collection API provides more flexible capabilities for managing group of elements
     ```java
     add 5
     update 5
     remove 5
     search 2
     rearrage 4
    ```
- Java Streams APIs
    - They efficiently filter, amn and reduce large streams of data.
    - They perform actions upon data using `lambda` expressions
    - `lambda` expressions are a form of functional programming
    ```java
    List<Pet> pets = new ArrayList<>();
    pets.stream().parallel()
                    .filter(p -> p.getFood() == "milk")
                    .forEach(e -> e.calculateWeight());
    ```

- Java IO API
    - Transfer data throughh a series of interconnected streams
    - Read information from vairous sources - input direction
    - Write information to various destinations - output direction

- Java Concurrency API
    - Takes advantage of multi-CPU-core architecture
    - Executes code concurrently to achive better performance and user experience
    ```java
    Callable<BigDecimal> taxCalculation = new Callable<>(){
        public BigDecimal call throws Exception {
            // perform concurrent calculation 
            return tax; 
        }
    };

    ExecutorService es = Executors.newCachedThreadPool();
    Future<BigDecimal> result = es.submit(taxCalculation);
    ```

- Java Persistence API 
    - Java Database Connectivity Protocol - `JDBC` enables database connectivity and SQL statement execution
    - Java Persistence `API` - JPA enables java object-relational mappings
    ```
    application logic -> JPA -> JDBC API provider neutral -> Provider JDBC Driver -> native database protocal -> database any provider
    ```