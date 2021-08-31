from typing import Type, List
from abc import ABC, abstractmethod
from dataclasses import dataclass


class IMessenger(ABC):

    @abstractmethod
    def publish_command(
        self,
        command: "ICommand"
    ) -> List["IEvent"]:
        pass

    @abstractmethod
    def subscribe_command(
        self,
        command_cls: Type["ICommand"],
        command_handler: "ICommandHandler"
    ):
        pass

    @abstractmethod
    def publish_event(
        self,
        event: "IEvent"
    ):
        pass

    @abstractmethod
    def subscribe_event(
        self,
        event_cls: Type["IEvent"],
        event_handler: "IEventHandler"
    ):
        pass

    @abstractmethod
    def publish_query(
        self,
        query: "IQuery"
    ) -> "IResponse":
        pass

    @abstractmethod
    def subscribe_query(
        self,
        query_cls: Type["IQuery"],
        query_handler: "IQueryHandler"
    ):
        pass


@dataclass
class IEvent(ABC):
    pass


@dataclass
class ICommand(ABC):
    pass


@dataclass
class IQuery(ABC):
    pass


@dataclass
class IResponse(ABC):
    pass


class IEventHandler(ABC):
    def __call__(self, event: IEvent) -> None:
        pass


class ICommandHandler(ABC):
    def __call__(self, command: ICommand) -> None:
        pass


class IQueryHandler(ABC):
    def __call__(self, query: IQuery) -> IResponse:
        pass
