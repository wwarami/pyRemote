"""Diffie-Hellman key exchange.
-> https://cryptography.io/en/latest/hazmat/primitives/asymmetric/dh/
"""
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat import backends
from cryptography.hazmat.primitives import serialization


class DHKeys:
    @staticmethod
    def get_bytes_parameters(parameters: dh.DHParameters):
        return parameters.parameter_bytes(encoding=serialization.Encoding.PEM,
                                          format=serialization.ParameterFormat.PKCS3)

    @staticmethod
    def load_parameters_by_bytes(param_bytes: bytes) -> dh.DHParameters:
        return serialization.load_pem_parameters(param_bytes, backend=backends.default_backend())

    def generate_private_key(self) -> dh.DHPrivateKey:
        return self.parameters.generate_private_key()

    def _set_parameters(self, parameters: dh.DHParameters) -> None:
        self.parameters = parameters

    @staticmethod
    def generate_public_key(private_key: dh.DHPrivateKey) -> dh.DHPublicKey:
        return private_key.public_key()

    @staticmethod
    def _generate_dh_parameters(key_size: int) -> dh.DHParameters:
        return dh.generate_parameters(generator=2, key_size=key_size)

    @staticmethod
    def get_public_key_bytes(public_key: dh.DHPublicKey) -> bytes:
        return public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                       format=serialization.PublicFormat.PKCS1)

    @staticmethod
    def load_public_key_by_bytes(public_key_bytes: bytes) -> dh.DHPublicKey:
        return serialization.load_pem_public_key(public_key_bytes, backend=backends.default_backend())
