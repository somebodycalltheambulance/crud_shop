from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.auth.deps import get_current_user
from app.models.user import User
from app.schemas.auth import LoginIn, TokenOut
from app.schemas.user import UserOut
from app.services.auth_service import AuthService

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=TokenOut)
async def login(payload: LoginIn, db: Annotated[AsyncSession, Depends(get_db)]):
    token = await AuthService.authenticate(db, payload.email, payload.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
async def me(current: User = Depends(get_current_user)):
    return current
