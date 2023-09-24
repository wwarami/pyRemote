import asyncio
from server_base_utils import start_asyncio_server
from io_handler.asyncio_handler import AsyncIOHandler, AsyncIORequestsManager


async def main() -> None:
    request_manager = AsyncIORequestsManager(io_handler=AsyncIOHandler)
    await start_asyncio_server(
        host='127.0.0.1',
        port=2000,
        connection_handler=request_manager.create_io_handler)

if __name__ == "__main__":
    asyncio.run(main())
