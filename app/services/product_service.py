from sqlalchemy import and_, asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.repositories.category import CategoryRepository
from app.repositories.product import ProductRepository

product_repo = ProductRepository()
category_repo = CategoryRepository()


class ProductService:
    @staticmethod
    async def create(db: AsyncSession, data: dict) -> Product:
        """Создать товар. Категория обязана существовать."""
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
    ) -> dict:
        """Список товаров с фильтрами, сортировкой и пагинацией. Возвращает items + total."""
        # фильтры
        conds = []
        if category_id is not None:
            conds.append(Product.category_id == category_id)
        if brand:
            conds.append(Product.brand.ilike(f"%{brand.strip()}%"))
        if price_min is not None:
            conds.append(Product.price >= price_min)
        if price_max is not None:
            conds.append(Product.price <= price_max)
        if price_min is not None and price_max is not None and price_min > price_max:
            raise ValueError("price_min не может быть больше price_max")

        base_stmt = select(Product)
        if conds:
            base_stmt = base_stmt.where(and_(*conds))

        # total считаем от базового запроса (без limit/offset)
        total_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = (await db.execute(total_stmt)).scalar_one()

        # сортировка
        if sort:
            sort_map = {
                "price": Product.price,
                "-price": Product.price,
                "name": Product.name,
                "-name": Product.name,
            }
            col = sort_map.get(sort)
            if col is None:
                raise ValueError(
                    'Некорректный sort. Разрешено: "price", "-price", "name", "-name".'
                )
            order = desc(col) if sort.startswith("-") else asc(col)
            base_stmt = base_stmt.order_by(order)

        # пагинация
        page_stmt = base_stmt.limit(limit).offset(offset)

        res = await db.execute(page_stmt)
        items = res.scalars().all()
        return {"items": items, "total": total}

    @staticmethod
    async def get(db: AsyncSession, id_: int) -> Product | None:
        return await product_repo.get(db, id_)

    @staticmethod
    async def update(db: AsyncSession, obj: Product, data: dict) -> Product:
        return await product_repo.update(db, obj, data)

    @staticmethod
    async def delete(db: AsyncSession, obj: Product) -> None:
        return await product_repo.delete(db, obj)
