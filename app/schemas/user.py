from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints

Pwd = Annotated[str, StringConstraints(min_length=8, max_length=72)]


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    email: EmailStr = Field(description="user email")
    password: Pwd


class UserOut(UserBase):
    id: int
    email: EmailStr

    class Config:
        model_config = ConfigDict(from_attributes=True)  # Позволяет возвращать ORM-обьекты
