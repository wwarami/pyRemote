import asyncio
from pyremote.server.key_exchange import base
from pyremote.common.security import dh_key
from pyremote.common import configs


class AsyncDHKeyExchanger(base.KeyExchanger):
    keys_manager_cls: dh_key.DHKeys

    def __init__(self, dh_keys_class: dh_key.DHKeys,
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter
                 ):
        self.keys_manager_cls = dh_keys_class
        self.reader = reader
        self.writer = writer
        self.private_key = self._generate_private_key()
        self.public_key = self._generate_public_key(self.private_key)

    def _generate_private_key(self):
        return self.keys_manager_cls.generate_private_key()

    def _generate_public_key(self, private_key: dh_key.dh.DHPrivateKey):
        return self.keys_manager_cls.generate_public_key(private_key)

    async def get_parameters_public_key_response(self) -> configs.key_exchange_configs.ServerParametersPublicKey:
        return configs.key_exchange_configs.ServerParametersPublicKey(
            parameters=self.keys_manager_cls.get_parameters_bytes().decode(),
            server_public_key=self.keys_manager_cls.
            get_public_key_bytes(
                self.public_key
            ).decode()
            )

    async def get_client_public_key(self) -> dh_key.dh.DHPublicKey:
        raw_data = await self.reader.readuntil(configs.io_configs.ANY_IO_END)
        client_public_key_obj = configs.key_exchange_configs.ClientPublicKey.from_json(raw_data.decode())
        return self.keys_manager_cls.load_public_key_by_bytes(client_public_key_obj.client_public_key.encode())

    async def do_key_exchange(self) -> bytes:
        # Send parameters and public_key to client.
        parameters_and_public_key_data = await self.get_parameters_public_key_response()
        self.writer.write(parameters_and_public_key_data.as_json(end=configs.io_configs.ANY_IO_END).encode())
        await self.writer.drain()

        # Get client's public key
        client_public_key = await self.get_client_public_key()

        # compute and return shared key
        return self.keys_manager_cls.compute_shared_key(self.private_key, client_public_key)
