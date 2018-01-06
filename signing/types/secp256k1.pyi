from secp256k1 import (
    PrivateKey,
    PublicKey,
)


class Secp256k1Context:
    def __init__(self) -> None: ...
    def get_algorithm_name(self) -> str: ...
    def get_public_key(
        self,
        private_key: Secp256k1PrivateKey
    ) -> Secp256k1PublicKey: ...
    def sign(self, message: bytes, private_key: Secp256k1PrivateKey) -> str: ...
    def verify(self, signature: str, message: bytes, public_key: Secp256k1PublicKey) -> bool: ...


class Secp256k1PrivateKey:
    def __init__(self, secp256k1_private_key: PrivateKey) -> None: ...
    def as_bytes(self) -> bytes: ...
    def as_hex(self) -> str: ...
    @staticmethod
    def from_hex(hex_str: str) -> Secp256k1PrivateKey: ...
    @staticmethod
    def from_wif(wif: str) -> Secp256k1PrivateKey: ...
    def get_algorithm_name(self) -> str: ...
    @property
    def secp256k1_private_key(self) -> PrivateKey: ...


class Secp256k1PublicKey:
    def __init__(self, secp256k1_public_key: PublicKey) -> None: ...
    def as_bytes(self): ...
    def as_hex(self) -> str: ...
    @staticmethod
    def from_hex(hex_str: str) -> Secp256k1PublicKey: ...
    def get_algorithm_name(self) -> str: ...
    @property
    def secp256k1_public_key(self) -> PublicKey: ...
