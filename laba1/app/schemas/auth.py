from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    exp: datetime | None = None


class TokenPayload(BaseModel):
    sub: str
    role: str
    exp: datetime | None = None
