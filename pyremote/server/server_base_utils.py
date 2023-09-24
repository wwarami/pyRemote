import asyncio
from typing import Callable, Any


async def start_asyncio_server(
        host: str,
        port: int,
        connection_handler: Callable[[asyncio.StreamReader, asyncio.StreamWriter], Any]) -> None:
    server = await asyncio.start_server(
        connection_handler, host, port)

    address = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {address}')

    async with server:
        await server.serve_forever()
