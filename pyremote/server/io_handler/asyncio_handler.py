import asyncio
from typing import Type, Protocol
from pyremote.server.io_handler import base
from pyremote.server.key_exchange import base as key_ex_base


class SecureKeysClass(Protocol):
    """ A class which key exchanger class will use."""


class AsyncIORequestsManager(base.RequestManager):
    """This class will be used for managing and creating AsyncIOHandlers."""

    def __init__(self, io_handler: Type[base.IOHandler],
                 key_exchanger: Type[key_ex_base.AsyncKeyExchanger],
                 secure_keys_cls: SecureKeysClass):
        self.io_handler_cls = io_handler
        self.key_exchanger = key_exchanger
        self.secure_keys_cls = secure_keys_cls

    async def start_new(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        key_exchanger = self.key_exchanger(keys_manager_cls=self.secure_keys_cls,
                                           reader=reader,
                                           writer=writer)
        shared_secret = await key_exchanger.do_key_exchange()
        # TODO: ...


class AsyncIOHandler(base.IOHandler):
    def __init__(self,
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter) -> None:
        self.reader = reader
        self.writer = writer

    async def _read(self, size: int = -1) -> bytes:
        return await self.reader.read(n=size)

    async def _write(self, data: bytes) -> None:
        self.writer.write(data)
        await self.writer.drain()

    async def echo_message(self):
        """
        This is used for testing server.
        :return: None
        """
        message = await self._read(128)
        await self._write(message)

    async def new_connection(self):
        await self.echo_message()
