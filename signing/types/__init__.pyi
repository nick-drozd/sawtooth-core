from sawtooth_signing.secp256k1 import (
    Secp256k1Context,
    Secp256k1PrivateKey,
)


def create_context(algorithm_name: str) -> Secp256k1Context: ...


class CryptoFactory:
    def __init__(self, context: Secp256k1Context) -> None: ...
    @property
    def context(self) -> Secp256k1Context: ...
    def new_signer(self, private_key: Secp256k1PrivateKey) -> Signer: ...


class Signer:
    def __init__(
        self,
        context: Secp256k1Context,
        private_key: Secp256k1PrivateKey
    ) -> None: ...
    def sign(self, message: bytes) -> str: ...
