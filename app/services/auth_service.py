from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, needs_rehash, verify_password
from app.models.user import User


class AuthService:
    @staticmethod
    async def authenticate(db: AsyncSession, email: str, password: str) -> str | None:
        q = await db.execute(select(User).where(User.email == email))
        user = q.scalar_one_or_none()
        if not user or not verify_password(password, user.hashed_password):
            return None
        if needs_rehash(user.hashed_password):
            user.hashed_password = hash_password(password)
            await db.commit
        return create_access_token(str(user.id))
