from pydantic import BaseModel, Field


class ProductsBase(BaseModel):
    name: str = Field(min_length=2)
    brand: str = Field(min_length=1)
    price: float = Field(ge=0)  # Цена не может быть отрицательной
    description: str | None = None
    category_id: int


class ProductCreate(ProductsBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    brand: str | None = None
    price: float | None = Field(default=None, ge=0)
    description: str | None = None
    category_id: int | None = None


class ProductOut(ProductsBase):
    id: int

    class Config:
        from_attributes = True
