import os
from abc import ABC, abstractmethod
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Cryptographer(ABC):
    """Base cryptography class. All cryptographers will inherent from it."""
    @classmethod
    @abstractmethod
    def encrypt(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def decrypt(cls, *args, **kwargs):
        pass


class AESCryptographer(Cryptographer):
    """Encryption using AES"""
    @classmethod
    def _generate_iv(cls, size: int = 16) -> bytes:
        """Generate Initialization Vector."""
        return os.urandom(size)

    @classmethod
    def add_padding(cls, data: bytes) -> bytes:
        """ Add padding to the data to make it a multiple of 16 bytes"""
        padding_length = 16 - (len(data) % 16)
        return data + bytes([padding_length] * padding_length)

    @classmethod
    def remove_padding(cls, data: bytes) -> bytes:
        """ Remove padding from the data"""
        padding_length = data[-1]
        return data[:-padding_length]

    @classmethod
    def _separate_data_text(cls, data: bytes, iv_size: int = 16):
        return data[:iv_size], data[iv_size:]

    @classmethod
    def encrypt(cls, key: bytes, data: bytes, iv_size: int = 16) -> bytes:
        iv = cls._generate_iv(iv_size)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encrypter = cipher.encryptor()
        ciphertext = encrypter.update(cls.add_padding(data)) + encrypter.finalize()
        return iv + ciphertext

    @classmethod
    def decrypt(cls, key: bytes, data: bytes, iv_size: int = 16) -> bytes:
        iv, data = cls._separate_data_text(data, iv_size)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decrypter = cipher.decryptor()
        plaintext = decrypter.update(data) + decrypter.finalize()
        return cls.remove_padding(plaintext)

