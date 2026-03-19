from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserCreate
from app.utils.password import hash_password


class UserManager:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_username(self, username: str) -> User | None:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, data: UserCreate) -> User:
        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
            role=data.role,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
