from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import Role
from app.core.database import get_db
from app.crud import ItemManager
from app.models import User
from app.schemas import ItemCreate, ItemResponse, ItemUpdate
from app.utils.deps import require_roles

router = APIRouter(prefix="/items", tags=["Сущности"])


@router.get(
    "",
    response_model=list[ItemResponse],
    summary="Список сущностей",
)
async def list_items(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(Role.VIEWER, Role.MODERATOR, Role.ADMIN)),
) -> list[ItemResponse]:
    manager = ItemManager(db)
    return await manager.get_list(offset=offset, limit=limit)


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Получить сущность по ID",
)
async def get_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(Role.VIEWER, Role.MODERATOR, Role.ADMIN)),
) -> ItemResponse:
    manager = ItemManager(db)
    item = await manager.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сущность не найдена")
    return item


@router.post(
    "",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать сущность",
)
async def create_item(
    data: ItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(Role.MODERATOR, Role.ADMIN)),
) -> ItemResponse:
    manager = ItemManager(db)
    return await manager.create(data)


@router.patch(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Обновить сущность",
)
async def update_item(
    item_id: int,
    data: ItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(Role.MODERATOR, Role.ADMIN)),
) -> ItemResponse:
    manager = ItemManager(db)
    item = await manager.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сущность не найдена")
    return await manager.update(item, data)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить сущность",
)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(Role.ADMIN)),
) -> None:
    manager = ItemManager(db)
    item = await manager.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сущность не найдена")
    await manager.delete(item)
