from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend


class KeyPair:
    """Пара RSA-ключей для подписания и верификации."""

    def __init__(
        self,
        private_key: rsa.RSAPrivateKey | None = None,
        *,
        key_size: int = 2048,
    ) -> None:
        if private_key is not None:
            self._private_key = private_key
        else:
            self._private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size,
                backend=default_backend(),
            )

    def sign(self, message: bytes) -> bytes:
        """Подписывает сообщение: SHA-256(message) -> подпись закрытым ключом."""
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(message)
        message_hash = digest.finalize()
        return self._private_key.sign(
            message_hash,
            padding.PKCS1v15(),
            hashes.SHA256(),
        )

    def verify(self, message: bytes, signature: bytes) -> bool:
        """Проверяет подпись открытым ключом; возвращает True при успехе."""
        public_key = self._private_key.public_key()
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(message)
        expected_hash = digest.finalize()
        try:
            public_key.verify(
                signature,
                expected_hash,
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
            return True
        except Exception:
            return False

    def get_public_key_pem(self) -> bytes:
        """Экспорт открытого ключа в PEM для передачи по сети."""
        return self._private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )


class Verifier:
    """Верификация подписи по открытому ключу (без закрытого)."""

    def __init__(self, public_key_pem: bytes) -> None:
        self._public_key = serialization.load_pem_public_key(
            public_key_pem, backend=default_backend()
        )
        if not isinstance(self._public_key, rsa.RSAPublicKey):
            raise ValueError("Expected RSA public key")

    def verify(self, message: bytes, signature: bytes) -> bool:
        """Проверяет подпись сообщения."""
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(message)
        expected_hash = digest.finalize()
        try:
            self._public_key.verify(
                signature,
                expected_hash,
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
            return True
        except Exception:
            return False
