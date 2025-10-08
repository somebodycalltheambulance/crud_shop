from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.auth.deps import require_admin
from app.models.user import User
from app.schemas.catergory import CategoryCreate, CategoryOut, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: CategoryCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _user: User = Depends(require_admin),
):
    try:
        return await CategoryService.create(db, name=payload.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("", response_model=list[CategoryOut])
async def list_categories(db: Annotated[AsyncSession, Depends(get_db)]):
    return await CategoryService.list(db)


@router.patch("/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _user: User = Depends(require_admin),
):
    cat = await CategoryService.get(db, category_id)
    if not cat:
        raise HTTPException(404, "Category not found")
    return await CategoryService.update(db, cat, payload.model_dump(exclude_unset=True))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _user: User = Depends(require_admin),
):
    cat = await CategoryService.get(db, category_id)
    if not cat:
        raise HTTPException(404, "Category not found")
    await CategoryService.delete(db, cat)
