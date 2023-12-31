import asyncio
from pyremote.server.server_base_utils import start_asyncio_server
from pyremote.common.security.dh_key import DHKeys
from pyremote.server.io_handler.asyncio_handler import AsyncIOHandler, AsyncIORequestsManager
from pyremote.server.key_exchange.dh import AsyncDHKeyExchanger


async def main() -> None:
    dh_keys_manager_cls = DHKeys(DHKeys.generate_dh_parameters())
    request_manager = AsyncIORequestsManager(io_handler=AsyncIOHandler,
                                             secure_keys_cls=dh_keys_manager_cls,
                                             key_exchanger=AsyncDHKeyExchanger)
    await start_asyncio_server(
        host='127.0.0.1',
        port=2000,
        connection_handler=request_manager.start_new)

if __name__ == "__main__":
    asyncio.run(main())
