from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.category import CategoryRepository
from app.repositories.product import ProductRepository

product_repo = ProductRepository()
category_repo = CategoryRepository()


class ProductService:
    @staticmethod
    async def create(db: AsyncSession, data: dict):
        # простая бизнес-проверка: категория должна существовать
        cat = await category_repo.get(db, data["category_id"])
        if not cat:
            raise ValueError("Category not found")
        return await product_repo.create(db, data)

    @staticmethod
    async def list(db: AsyncSession):
        return await product_repo.list(db)

    @staticmethod
    async def get(db: AsyncSession, id_: int):
        return await product_repo.get(db, id_)

    @staticmethod
    async def update(db: AsyncSession, obj, data: dict):
        return await product_repo.update(db, obj, data)

    @staticmethod
    async def delete(db: AsyncSession, obj):
        return await product_repo.delete(db, obj)
