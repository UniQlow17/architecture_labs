from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from app.core.config import settings
from app.core.constants import Role
from app.schemas import Token, TokenPayload


def create_access_token(username: str, role: Role) -> Token:
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": username, "role": role.value, "exp": expire}
    return Token(
        access_token=jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm),
        exp=expire,
        token_type="bearer"
    )


def verify_token(token: str) -> TokenPayload | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return TokenPayload(sub=payload["sub"], role=payload["role"], exp=payload.get("exp"))
    except JWTError:
        return None
