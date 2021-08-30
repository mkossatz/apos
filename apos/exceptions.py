from .interfaces import ICommand

class MissingHandler(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class OverwritingHandler(Exception):
    def __init__(self, message: str):
        super().__init__(message)