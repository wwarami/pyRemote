import asyncio
from pyremote.server.key_exchange import base
from pyremote.common.security import dh_key


class AsyncDHKeyExchanger(base.KeyExchanger):
    def __init__(self, dh_keys_class: dh_key.DHKeys,
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter):
        self.keys_manager_cls = self.validate_keys_manager_cls(dh_keys_class)
        self.reader = reader
        self.writer = writer

    @staticmethod
    def validate_keys_manager_cls(dh_keys_class: dh_key.DHKeys) -> dh_key.DHKeys:
        if not hasattr(dh_keys_class, 'parameters'):
            # TODO: Add a custom exception.
            raise Exception
        return dh_keys_class

    async def do_key_exchange(self):
        # TODO: This will be completed when serialization part is done.
        ...
