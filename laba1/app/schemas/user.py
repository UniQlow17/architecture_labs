from pydantic import BaseModel, EmailStr, Field

from app.core.constants import Role


class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: Role = Role.VIEWER


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Role
    is_active: bool

    model_config = {"from_attributes": True}
