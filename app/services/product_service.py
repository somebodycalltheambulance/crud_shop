from sqlalchemy import and_, asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
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
    async def list(
        db: AsyncSession,
        *,
        limit: int = 10,
        offset: int = 0,
        category_id: int | None = None,
        brand: str | None = None,
        price_min: float | None = None,
        price_max: float | None = None,
        sort: str | None = None,  # "price", "-price", "name", "-name"
    ):
        stmt = select(Product)
        conds = []
        if category_id is not None:
            conds.append(Product.category_id == category_id)
        if brand:
            conds.append(Product.brand.ilike(f"%{brand}%"))
        if price_min is not None:
            conds.append(Product.price >= price_min)
        if price_max is not None:
            conds.append(Product.price <= price_max)
        if conds:
            stmt = stmt.where(and_(*conds))

        if sort:
            col = Product.price if "price" in sort else Product.name
            stmt = stmt.order_by(desc(col) if sort.startswith("-") else asc(col))

        stmt = stmt.limit(limit).offset(offset)
        res = await db.execute(stmt)
        return res.scalars().all()

    @staticmethod
    async def get(db: AsyncSession, id_: int):
        return await product_repo.get(db, id_)

    @staticmethod
    async def update(db: AsyncSession, obj, data: dict):
        return await product_repo.update(db, obj, data)

    @staticmethod
    async def delete(db: AsyncSession, obj):
        return await product_repo.delete(db, obj)
