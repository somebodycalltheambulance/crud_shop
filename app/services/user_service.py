from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import UserRepository

# Создаем репозиторий который умеет общаться с таблицей users
repo = UserRepository()


class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, email: str, password: str) -> User:
        # проверка уникальности email без учёта регистра
        existing = await db.execute(select(User.id).where(func.lower(User.email) == email.lower()))
        if existing.scalar_one_or_none():
            raise ValueError("Email already registered")

        # создаём пользователя
        return await repo.create(
            db,
            {
                "email": email,
                "hashed_password": hash_password(password),
                # "username": username  # если решишь передавать — добавь аргумент и прокинь сюда
            },
        )

    @staticmethod
    async def list_users(db: AsyncSession) -> list[User]:
        return await repo.list(db)

    @staticmethod
    async def get_user(db: AsyncSession, user_id: int) -> User | None:
        return await repo.get(db, user_id)
