
# Metamorphosis.

![Metamorphosis.](metamorphosis.jpg?raw=true "Metamorphosis.")

# Table of contents
1. [Project overview.](#overview)
2. [Architecture.](#architecture)
    1. [The value that this approach can provide.](#valueprovide)
    2. [The Clean Architecture.](#cleanarchitecture)
        1. [Entities.](#entities)
        2. [Use cases.](#usecases)
        3. [Interface Adapters.](#interface)
        4. [External interfaces.](#externalint)
4. [Note: API.](#apinote)
5. [Use Cases diagram.](#ucdiagram)
6. [Project structure.](#structure)


1. ## Project overview.<a name="overview"></a>

The goal of the Metamorphosis project is to create a basic "function as a service" platform system on top of a Kafka Message Broker. All the project is based on python language and all its wonders. Also, a CLI is facilitated to make its use simpler.

For the creation of the metamorphosis project, we choose to use a “clean architecture” approach because It provides a lot of benefits and a very auto-described project shape.

**The system have four components.**

* The main component is responsible for orchestrating the rest of the components that belong to the system. 

* The deployer component is responsible for receiving the code through the message broker and compile it, inform the result of the operation and publish the new lambda function.

* The web server is in charge to receive and respond to all requests from external systems and expose lambdas acting like an “API Gateway”.

* The CLI component is a very plain version of the concept and it's responsible for sending commands an report the state of the deployment process of lambdas functions. 

All the components run as an isolated process to avoid bottlenecks. In future versions, this enables us to escalate the system easier.


## Architecture.<a name="architecture"></a>

The clean architecture pattern is strongly oriented on the domain and it uses cases. For this project, we start to use a DDD approach that focuses on a monolithic design. This kind of approach can be changed in the future, slicing the domains in it use-cases logical boundaries. This provides the required flexibility for the evolution of the systems.


### The value that this approach can provide.<a name="valueprovide"></a>

* Describe in better ways the intended usage. When you look at the package structure you get a feel for what the application does rather than seeing technical details.

* All business logic is in a use case so it's easy to find and it's not duplicated anywhere else.

* Frameworks are isolated in individual modules so that when (not if) change our vision we only have to change one place, with the rest of the app not even knowing about.

* The app has use cases rather than being tied to a CRUD system.

* Effective and easy testing strategy.

* Hard to do the wrong thing because modules enforce compilation dependencies.

* Multiple works on stories so that different pairs can easily work on the same story at the same time to complete it quicker.

* Good monolith with clear use cases that you can split in micro-services later one, once you've learned more about them.


### The Clean Architecture.<a name="cleanarchitecture"></a>

As pushed by this architecture model, we are interested in separating the different layers of the system. The architecture is described by four layers, which however can be implemented by more than four actual code modules. Here is a brief description of those layers.

#### Entities.<a name="entities"></a>
This is the level in which the domain models are described. The domain model is a representation of meaningful real-world concepts pertinent to the domain that need to be modeled in software.

#### Use cases.<a name="usecases"></a>
This layer contains the use cases implemented by the system. This place is created the business process to be implemented.

#### Interface Adapters.<a name="interface"></a>
This layer corresponds to the boundary between the business logic and external systems and implements the API used to exchange data with them. Both the storage system and the user interface are external systems that need to exchange data with the use cases and this layer shall provide an interface for this data flow. In this project, the presentation part of this layer is provided by a JSON serializer, on top of which an external web service may be built. The storage adapter shall define here the common API of the storage systems.

#### External interfaces.<a name="externalint"></a>
This part of the architecture is made by external systems that implement the interfaces defined in the previous layer. Here is the web-server that implements (REST) entry points, which access the data provided by use cases through the JSON serializer. Also here is the storage system implementation, for example, a given database such as MongoDB.


>**API**.<a name="apinote"></a>
>
>The word API is of uttermost importance in clean architecture. Every layer may be accessed by an API, >which is a fixed collection of entry points (methods or objects). Here "fixed" means "the same among >every implementation. Every presentation tool, for example, will access the same use cases, and the >same methods, to obtain a set of domain models, which are the output of that particular use case. It >is up to the presentation layer to format data according to the specific presentation media.
>The same concept is valid for the storage layer. Every storage implementation shall provide the same >methods. When dealing with use cases you shall not be concerned with the actual system that stores >data, it may be a MongoDB local installation, a cloud storage system or a trivial in-memory >dictionary.


## Use cases diagram.<a name="ucdiagram"></a>

![Use Cases diagram.](ucdiagram.jpg?raw=true "Use Cases diagram.")

<a href="https://yuml.me/3504e11b.jpg" target="_blank">Yuml.me link.</a>


## Sequence diagram.<a name="sequence"></a>

![Sequence diagram.](seqdiagram.png?raw=true "Sequence diagram.")

<a href="https://sequencediagram.org/index.html#initialData=C4S2BsFMAIFlOAQwLYHsBOAHAFqgziHtHpAI4CukAdgMYwAmIiA5uigHQBQniNwG0AKol0nTInSgaIcVWDQAwgBkAkmIlSZiOXEh48LSACF0qANaRRnYZYC0APmUqAXMSSToVVPUicnDgCoAQUxMVzx3YG4QzECAEUhMcFQAT0tXAB4MmnRIRGBIe3tOBKTUu3tS5LT0cMhwADNoECowaNDAgHVIACMRADd06CycvIKizm6+y0H0BymBoZJG5tao6xEHJ1dmBGhk5jw-VQd4fUMTcyGDo7ODXcuLOcrE6uvUQ847i9MnjNtbFVyrVoLlgOR0FR9h8jk5-rZvg9fu9PhsKttoJhyD1wIRsNAaN5fP57IjjMiQVicXivnp7uSrs8gTVXISfCVXsCHMyhoTkJgQFACUSOWUavNeosQaN8jAggAFNQ89DwhYzIb0VBUXxkx6WeHK1ya7XHFTw3UUo1a3xo54Yqm4vD4yCDOSm050n6M1wu6jrGx21ThfiYTwikkxYOoTCcGLxTks4YZHwRUwpCYp4Bp6DK2MdewBNXoWaZZN6LOpDPl7NF2Z52L2SPEepNLKZtNV1OpaAxbicIA" target="_blank">sequencediagram.org link.</a>


## Project structure.<a name="structure"></a>

The global structure of the package has been built reflecting the layered structure introduced in the previous section, and the structure of the tests directory mirrors this structure so that tests are easily found.

```  
└── metamorphosis
    ├── core
    │   └── shared
    ├── entities
    │   ├── app
    │   ├── deployer
    │   └── gateway
    ├── external_interfaces
    │   ├── cli
    │   └── webserver
    ├── interface_adapters
    │   └── serializers
    └── use_cases
        ├── app
        ├── deployer
        └── gateway
```

## Running the proyect.

### WIP