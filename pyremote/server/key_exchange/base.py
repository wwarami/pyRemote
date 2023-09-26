from abc import ABC, abstractmethod


class KeyExchanger(ABC):
    @abstractmethod
    def do_key_exchange(self, *args, **kwargs):
        ...
