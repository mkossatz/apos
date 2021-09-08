# apos

The backbone for message-driven applications.

## Summary
This library is designed to act as a software-level message broker, enabling a lightweight implementation of the publish-subscribe design pattern.

apos was born to accomplish two objectives:
* Decouple the application layer from any interfaces
* Develop reactive business functions

With apos you can develop a message-driven application. This means that commands, events, and queries are sent to apos, which in return executes the functions that subscribe to these messages. This means that an interface implementation, may it be a web-api or a CLI, would not directly call  application functions, but would rather send a message to apos, which will in return execute the business functions that subscribe to these messages. Equally, a business function would not call any other business function, but rather publishes an event, which other business functions can subscribe to and execute upon, controlled through apos.


## Installation
The library can be found on PyPi:
https://pypi.org/project/apos/


```shell
pip3 install apos
```

## Decoupling the application layer
In this particular case we are looking at the boundry between the interface, which can be anything like a web-api or a AMQP endpoint, and the application layer, which is a bit more ambigious but lets say it contains the business functions/services that your application offers. Using apos, an interface implementation would not be aware of any business functions. This is the case because it would not call functions directly but rather publish a command, event, or query object to apos. Apos will in return execute the functions that subscribe to these messages. This decouples the interfaces almost completely from the business logic. In practice, this means that most of the application layer can be extended, refactored, or replaced without having to change any dependencies in any interface implementations. The interface implementations would only depend on the message objects and would rely on the application layer to provide the logic to react to these messages.

### Publishing

```python
messenger.publish_command(CreateUserCommand(user_name="Max"))
events: List[apos.IEvent] = messenger.get_published_events()
```
The example above shows how an interface implementation can use the apos.Messenger to publish a command. The apos.Messenger will execute the Callable mapped to the name of the command Class. At the same time, it will record the event published by the executed business function, as well as any other events that are published by business functions that are executed as a result of subscribing to the prior events. These events can be retrieved from the apos.Messenger using the get_published_events method. It is up to the interface implementation what it wants to do with these events, but an example would be returning them in a HTTP response or publishing the messages to an external message broker like Kafka or RabbitMQ.

```python
response: RetrievedUserResponse = messenger.publish_query(
            RetrieveUserQuery(user_name="Max"))
```
The example above shows that the apos.Messenger equally supports query messages. Publishing queries works like publishing commands, the only difference being that it will return the response object returned by the business function that subscribes to the query.

### Subscribing

```python
messenger.subscribe_command(CreateUserCommand, create_user)
messenger.subscribe_events(UserCreatedEvent, [email_user])
messenger.subscribe_query(RetrieveUserQuery, retrieve_user)
```
The example above shows how the apos.Messenger is used to subscribe functions to message Classes. The apos.Messenger will record these subscriptions by mapping the Class names to the according Callables. Be mindful of the following restrictions:
* Commands and queries are mapped one-to-one, only allowing one subscription per command
* Events are mapped one-to-many, allowing multiple subscriptions per event



## Reactive Business Functions
Looking at a typical straight forward implementation of an application layer, you will usually see business functions calling other business functions. This becomes funny when its done across domain core aggregate boundries. For example, lets say we have a recruitment platform, where deactivating a user additionally requires a withdrawal of the users job applications an alert email to be sent. In this case, we would likely have a business function for deactivating a user, which would call the business functions for withdrawing job applications and sending an alert email. With this, we coupled the user deactivation to everying else that should happen as a consequence. The other way of doing this would be by having reactive business functions, where the completion of one function would emit an event, which other business functions can subscribe to aka react to. Coming back to the example, withdrawing the job applications and sending an alert email would be business functions that happen as a reaction to the user being deactivated. This way of developing reactive application increases maintainability and extendability because any business function can be added, removed, or refactored independent of any other function, as long as the events are defined. 

### Publishing

```python
messenger.publish_event(
    UserDeactivatedEvent(user_name="Max"))
```
The example above shows how an event can be published. In this case, the business function for deactivating a user would publish the UserDeactivatedEvent upon completion.

### Subscribing

```python
messenger.subscribe_events(
    UserDeactivatedEvent, [withdraw_job_applications])
```
The example above shows how the apos.Messenger can be used to subscribe a business function to an event. In this case, the business function for withdrawing job applications subscribes to the UserDeactivatedEvent. This means that if the user deactivation business function in the earlier example completes by publishing a UserDeactivatedEvent, the apos.Messenger would react by executing the business function for withdrawing the job applications. Upon calling the function, the event would be passed as an object as a parameter.


## Complete Examples

You can find examples in the examples directory of the projects repository.
https://github.com/mkossatz/apos/tree/main/examples