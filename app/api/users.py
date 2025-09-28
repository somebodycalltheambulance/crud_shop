from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        user = await UserService.create_user(db, email=payload.email, password=payload.password)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("", response_model=list[UserOut])
async def list_users(db: Annotated[AsyncSession, Depends(get_db)]):
    return await UserService.list_users(db)
