# app/repositories/base.py
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base


class BaseRepository[T: Base]:
    def __init__(self, model: type[T]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> T | None:
        return await db.get(self.model, id)

    async def list(self, db: AsyncSession) -> list[T]:
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: dict[str, Any]) -> T:
        obj = self.model(**obj_in)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, db_obj: T, obj_in: dict[str, Any]) -> T:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, db_obj: T) -> None:
        await db.delete(db_obj)
        await db.commit()
