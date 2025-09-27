from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.repositories.category import CategoryRepository

repo = CategoryRepository()


class CategoryService:
    @staticmethod
    async def create(db: AsyncSession, name: str) -> Category:
        q = await db.execute(select(Category).where(Category.name == name))
        if q.scalar_one_or_none():
            raise ValueError("Category already exists")
        return await repo.create(db, {"name": name})

    @staticmethod
    async def list(db: AsyncSession):
        return await repo.list(db)

    @staticmethod
    async def update(db: AsyncSession, category: Category, data: dict) -> Category:
        return await repo.update(db, category, data)

    @staticmethod
    async def delete(db: AsyncSession, category: Category) -> None:
        return await repo.delete(db, category)

    @staticmethod
    async def get(db: AsyncSession, id_: int):
        return await repo.get(db, id_)
