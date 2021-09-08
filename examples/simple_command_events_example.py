from typing import List
from dataclasses import dataclass

import apos


@dataclass
class RegisterUserCommand:
    user_name: str


@dataclass
class UserRegisteredEvent:
    user_name: str


@dataclass
class NewUserGreetedEvent:
    user_name: str


class RegisterUser:

    def __init__(self, messenger) -> None:
        self._messenger = messenger

    def __call__(self, command: RegisterUserCommand) -> None:
        # Implementation of user registration
        self._messenger.publish_event(
            UserRegisteredEvent(command.user_name))


class GreetNewUser:

    def __init__(self, messenger) -> None:
        self._messenger = messenger

    def __call__(self, event: UserRegisteredEvent) -> None:
        # Implementation of user greeting
        self._messenger.publish_event(
            NewUserGreetedEvent(event.user_name))


messenger = apos.Messenger()
register_user = RegisterUser(messenger)
greet_new_user = GreetNewUser(messenger)

# subscribing to messages (application configuration)
messenger.subscribe_command(RegisterUserCommand, register_user)
messenger.subscribe_events(UserRegisteredEvent, [greet_new_user])

# some interface implementation
messenger.publish_command(RegisterUserCommand("Max"))
events = messenger.get_published_events()
print(events)
