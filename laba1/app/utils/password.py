from passlib.context import CryptContext

_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return _context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return _context.verify(plain, hashed)
