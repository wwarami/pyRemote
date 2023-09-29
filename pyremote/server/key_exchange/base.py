from typing import Protocol


class SecureKeysClass(Protocol):
    """ A class which key exchanger class will use for better key management."""


class KeyExchanger(Protocol):
    def do_key_exchange(self, *args, **kwargs):
        ...


class AsyncKeyExchanger(Protocol):
    def __init__(self, keys_manager_cls: SecureKeysClass, reader, writer, *args, **kwargs):
        ...

    async def do_key_exchange(self, *args, **kwargs):
        ...
