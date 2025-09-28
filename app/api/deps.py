from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session


async def get_db(session: Annotated[AsyncSession, Depends(get_session)]) -> AsyncSession:
    return session
