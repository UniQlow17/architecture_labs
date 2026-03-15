from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Item
from app.schemas import ItemCreate, ItemUpdate


class ItemManager:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get(self, item_id: int) -> Item | None:
        result = await self.db.execute(select(Item).where(Item.id == item_id))
        return result.scalar_one_or_none()

    async def get_list(self, offset: int = 0, limit: int = 100) -> list[Item]:
        result = await self.db.execute(select(Item).offset(offset).limit(limit))
        return list(result.scalars().all())

    async def create(self, data: ItemCreate) -> Item:
        item = Item(title=data.title, description=data.description)
        self.db.add(item)
        await self.db.flush()
        await self.db.refresh(item)
        return item

    async def update(self, item: Item, data: ItemUpdate) -> Item:
        if data.title is not None:
            item.title = data.title
        if data.description is not None:
            item.description = data.description
        await self.db.flush()
        await self.db.refresh(item)
        return item

    async def delete(self, item: Item) -> None:
        await self.db.delete(item)
        await self.db.flush()
