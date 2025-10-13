from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=2)
    brand: str = Field(min_length=1)
    price: float = Field(ge=0)  # цена не может быть отрицательной
    description: str | None = None
    category_id: int  # категория обязательна при создании


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    # все поля опциональны, чтобы можно было частично обновлять
    name: str | None = None
    brand: str | None = None
    price: float | None = Field(default=None, ge=0)
    description: str | None = None
    category_id: int | None = None


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
