from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import UserRepository

# Создаем репозиторий который умеет общаться с таблицей users
repo = UserRepository()


class UserService:
    @staticmethod
    async def create_user(
        db: AsyncSession, email: str, password: str
    ) -> User:  # Создаем нового пользователя
        # Проверка уникальности email
        exists = await db.execute(select(User).where(User.email == email))
        if exists.scalar_one_or_none():  # Проверяем есть ли в базу пользователь с таким email
            raise ValueError("Email already registered")
        return await repo.create(db, {"email": email, "hashed_password": hash_password(password)})

    @staticmethod
    async def list_users(db: AsyncSession):
        return await repo.list(db)

    @staticmethod
    async def get_user(db: AsyncSession, user_id: int):
        return await repo.get(db)
