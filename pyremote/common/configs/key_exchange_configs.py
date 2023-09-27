from pyremote.common.model import BaseModel


class ServerParametersPublicKey(BaseModel):
    parameters: str
    server_public_key: str


class ClientPublicKey(BaseModel):
    client_public_key: str
