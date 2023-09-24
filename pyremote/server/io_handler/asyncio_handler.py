import asyncio
from typing import Type
from .base import IOHandler, RequestManager


class AsyncIORequestsManager(RequestManager):
    """This class will be used for managing and creating IOHandlers."""
    def __init__(self, io_handler: Type[IOHandler]):
        self.io_handler_cls = io_handler

    async def create_io_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        io_handler = self.io_handler_cls(reader, writer)
        await io_handler.new_connection()


class AsyncIOHandler(IOHandler):
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
