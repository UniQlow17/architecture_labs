from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud import UserManager
from app.models import User
from app.schemas import Token, UserCreate, UserResponse
from app.utils.deps import get_current_user
from app.utils.jwt import create_access_token
from app.utils.password import verify_password

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация пользователя",
)
async def register(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> User:
    manager = UserManager(db)
    if await manager.get_by_username(data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует",
        )
    if await manager.get_by_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )
    return await manager.create(data)


@router.post(
    "/login",
    response_model=Token,
    summary="Вход",
)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    manager = UserManager(db)
    user = await manager.get_by_username(form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь деактивирован",
        )
    return create_access_token(user.username, user.role)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Текущий пользователь",
)
async def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
