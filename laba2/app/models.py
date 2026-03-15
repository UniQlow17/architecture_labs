from pydantic import BaseModel, Field


class VerifyRequest(BaseModel):
    message: str
    signature: str = Field(..., description="Подпись в base64")
    public_key: str = Field(..., description="Открытый ключ в PEM")


class VerifyResponse(BaseModel):
    verified: bool


class SignedMessageResponse(BaseModel):
    message: str
    signature: str = Field(..., description="Подпись в base64")


class PublicKeyResponse(BaseModel):
    public_key: str = Field(..., description="Открытый ключ в PEM")
