from typing import Type, Dict, List

from .interfaces import IMessenger
from .interfaces import IEvent
from .interfaces import ICommand
from .interfaces import IQuery
from .interfaces import IResponse
from .interfaces import IEventHandler
from .interfaces import ICommandHandler
from .interfaces import IQueryHandler
from .exceptions import MissingHandler
from .exceptions import OverwritingHandler


class Messenger(IMessenger):

    def __init__(self) -> None:
        self._command_handlers: Dict[str, ICommandHandler] = dict()
        self._event_handlers: Dict[str, List[IEventHandler]] = dict()
        self._query_handlers: Dict[str, IQueryHandler] = dict()
        self._published_events: List[IEvent] = list()

    def get_published_events(self) -> List[IEvent]:
        return self._published_events

    def flush_published_events(self) -> None:
        self._published_events = list()

    def publish_command(
        self,
        command: ICommand
    ) -> None:
        command_name: str = command.__class__.__name__
        if command_name not in self._command_handlers:
            raise MissingHandler(
                "Publishing command {} failed because of missing subscriber.".format(command))
        command_handler: ICommandHandler = self._command_handlers[command_name]
        command_handler(command)

    def subscribe_command(
        self,
        command_cls: Type[ICommand],
        command_handler: ICommandHandler
    ) -> None:
        command_name: str = command_cls.__name__
        if command_name in self._command_handlers:
            raise OverwritingHandler(
                "A handler for the command {} already exists.".format(command_name))
        self._command_handlers[command_name] = command_handler

    def publish_event(
        self,
        event: IEvent
    ) -> None:
        event_name: str = event.__class__.__name__
        self._published_events.append(event)
        event_handlers: List[IEventHandler] = \
            self._event_handlers.get(event_name, [])
        for event_handler in event_handlers:
            event_handler(event)

    def subscribe_event(
        self,
        event_cls: Type[IEvent],
        event_handler: IEventHandler
    ) -> None:
        event_name: str = event_cls.__name__
        if event_name not in self._event_handlers.keys():
            self._event_handlers[event_name] = []
        if event_handler not in self._event_handlers[event_name]:
            self._event_handlers[event_name].append(event_handler)

    def publish_query(
        self,
        query: IQuery
    ) -> IResponse:
        query_name: str = query.__class__.__name__
        if query_name not in self._query_handlers:
            raise MissingHandler(
                "Publishing query {} failed because of missing subscriber.".format(query))
        query_handler: IQueryHandler = self._query_handlers[query_name]
        response: IResponse = query_handler(query)
        return response

    def subscribe_query(
        self,
        query_cls: Type[IQuery],
        query_handler: IQueryHandler
    ) -> None:
        query_name: str = query_cls.__name__
        if query_name in self._query_handlers:
            raise OverwritingHandler(
                "A handler for the query {} already exists.".format(query_name))
        self._query_handlers[query_name] = query_handler
