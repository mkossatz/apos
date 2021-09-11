# apos

The backbone for message-driven applications.

## Summary
This Python library is designed to act as a software-level message broker, enabling a lightweight implementation of the publish-subscribe design pattern.

apos was born to accomplish two objectives:
* Decouple the application layer from any interfaces
* Develop reactive business functions

With apos, you can develop a message-driven application. This means that commands, events, and queries are sent to apos, which in return executes the functions that subscribe to these messages. This means that an adapter providing an external interface, may it be a web-API or a CLI, would not directly call application functions, but would rather send a message to apos, which will in return execute the business functions that subscribe to these messages. Equally, a business function would not call any other business function, but rather publishes an event, which other business functions can subscribe to and execute upon, controlled through apos.

![](https://miro.medium.com/max/652/1*ZTxTLfH0FWRIQLAZFlBGEQ.png)

## Context
See the Medium article linked below to read about why this library was created and how it is intended to be used. 
https://mkossatz.medium.com/a-backbone-for-message-driven-applications-ffdcef67824c


## Installation
The library can be found on PyPi:
https://pypi.org/project/apos/


```shell
pip3 install apos
```

## Getting Started

The code below is a very lightweight example of how you can use apos for commands, queries, and events. 

```python

from apos import apos


class RegisterUserCommand:
    pass


class UserRegisteredEvent:
    pass


class NewUserGreetedEvent:
    pass


class RetrieveUserQuery:
    pass


class RetrieveUserResponse:
    pass


def register_user(command: RegisterUserCommand) -> None:
    # Implementation of user registration
    apos.publish_event(
        UserRegisteredEvent())


def greet_new_user(event: UserRegisteredEvent) -> None:
    # Implementation of user greeting
    apos.publish_event(
        NewUserGreetedEvent())


def retrieve_user(query: RetrieveUserQuery) -> RetrieveUserResponse:
    # Implementation of user retrieval
    return RetrieveUserResponse()


# subscribing to messages (application configuration)
apos.subscribe_command(RegisterUserCommand, register_user)
apos.subscribe_event(UserRegisteredEvent, [greet_new_user])
apos.subscribe_query(RetrieveUserQuery, retrieve_user)

# some interface adapter
apos.publish_command(RegisterUserCommand())
events = apos.get_published_events()
print(events)
response: RetrieveUserResponse = apos.publish_query(RetrieveUserQuery())
print(response)


```



## Complete Examples

You can find examples in the examples directory of the projects repository.
https://github.com/mkossatz/apos/tree/main/examples