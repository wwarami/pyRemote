from abc import ABC, abstractmethod
from typing import Any


class RequestManager(ABC):
    """
    Request manager base class.
    """
    def create_io_handler(self, *args, **kwargs):
        ...


class IOHandler(ABC):
    """
    Io handler base class which all types of IO handlers will inherent from it.
    """

    @abstractmethod
    def new_connection(self, *args, **kwargs) -> Any:
        ...
