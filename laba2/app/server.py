import base64
import secrets
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.crypto import KeyPair, Verifier
from app.models import PublicKeyResponse, SignedMessageResponse, VerifyRequest, VerifyResponse

_server_keypair: KeyPair | None = None


def get_server_keypair() -> KeyPair:
    if _server_keypair is None:
        raise RuntimeError("Server keypair not initialized")
    return _server_keypair


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _server_keypair
    _server_keypair = KeyPair()
    yield
    _server_keypair = None


app = FastAPI(title="ЭЦП — сервер", lifespan=lifespan)


@app.post("/verify", response_model=VerifyResponse)
def verify_signature(req: VerifyRequest) -> VerifyResponse:
    """
    Сценарий 1: клиент подписал сообщение своим закрытым ключом.
    Сервер верифицирует подпись с помощью переданного открытого ключа клиента.
    """
    verifier = Verifier(req.public_key.encode())
    message_bytes = req.message.encode()
    signature = base64.b64decode(req.signature)
    verified = verifier.verify(message_bytes, signature)
    return VerifyResponse(verified=verified)


@app.get("/public-key", response_model=PublicKeyResponse)
def get_public_key() -> PublicKeyResponse:
    """Сценарий 2: клиент запрашивает открытый ключ сервера для последующей верификации."""
    pem = get_server_keypair().get_public_key_pem()
    return PublicKeyResponse(public_key=pem.decode())


@app.post("/signed-message", response_model=SignedMessageResponse)
def get_signed_message() -> SignedMessageResponse:
    """
    Сценарий 2: сервер генерирует случайное сообщение, подписывает его своим закрытым ключом
    и возвращает сообщение и подпись клиенту.
    """
    keypair = get_server_keypair()
    message = secrets.token_hex(16)
    signature = keypair.sign(message.encode())
    return SignedMessageResponse(
        message=message,
        signature=base64.b64encode(signature).decode(),
    )


def main() -> None:
    uvicorn.run("app.server:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
