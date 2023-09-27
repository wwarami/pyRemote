"""Diffie-Hellman key exchange.
-> https://cryptography.io/en/latest/hazmat/primitives/asymmetric/dh/
"""
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat import backends
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


class DHKeys:
    """ A class for handling generate and security part of Diffie-Hellman key exchange."""

    def __init__(self, parameters: dh.DHParameters):
        self.parameters = parameters

    def get_parameters_bytes(self) -> bytes:
        return self.parameters.parameter_bytes(encoding=serialization.Encoding.PEM,
                                               format=serialization.ParameterFormat.PKCS3)

    @classmethod
    def generate_dh_parameters(cls, key_size: int = 2048) -> dh.DHParameters:
        return dh.generate_parameters(generator=2, key_size=key_size)

    @classmethod
    def load_parameters_by_bytes(cls, param_bytes: bytes) -> dh.DHParameters:
        return serialization.load_pem_parameters(param_bytes, backend=backends.default_backend())

    def generate_private_key(self) -> dh.DHPrivateKey:
        return self.parameters.generate_private_key()

    @classmethod
    def generate_public_key(cls, private_key: dh.DHPrivateKey) -> dh.DHPublicKey:
        return private_key.public_key()

    @classmethod
    def get_public_key_bytes(cls, public_key: dh.DHPublicKey) -> bytes:
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    @classmethod
    def load_public_key_by_bytes(cls, public_key_bytes: bytes) -> dh.DHPublicKey:
        return serialization.load_pem_public_key(public_key_bytes, backend=backends.default_backend())

    @classmethod
    def compute_shared_key(cls, private_key: dh.DHPrivateKey,
                           peer_public_key: dh.DHPublicKey,
                           salt: str = None) -> bytes:
        shared_secret = private_key.exchange(peer_public_key)
        derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt).derive(shared_secret)
        return derived_key

