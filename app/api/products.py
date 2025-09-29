from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        return await ProductService.create(db, payload.model_dump())
    except ValueError as e:
        raise HTTPException(400, detail=str(e)) from e


@router.get("", response_model=list[ProductOut])
async def list_products(db: Annotated[AsyncSession, Depends(get_db)]):
    return await ProductService.list(db)


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    prod = await ProductService.get(db, product_id)
    if not prod:
        raise HTTPException(404, "Product not found")
    return prod


@router.patch("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int, payload: ProductUpdate, db: Annotated[AsyncSession, Depends(get_db)]
):
    prod = await ProductService.get(db, product_id)
    if not prod:
        raise HTTPException(404, "Product not found")
    return await ProductService.update(db, prod, payload.model_dump(exclude_unset=True))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    prod = await ProductService.get(db, product_id)
    if not prod:
        raise HTTPException(404, "Product not found")
    await ProductService.delete(db, prod)
