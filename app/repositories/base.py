from collections.abc import Mapping, Sequence
from typing import Any, TypeVar

from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy import update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository:
    model: type[T]

    def __init__(self, model: type[T]):
        self.model = model

    async def update(
        self,
        db: AsyncSession,
        db_obj: T,
        obj_in: BaseModel | Mapping[str, Any],
        *,
        ignore_none: bool = True,
        protected: Sequence[str] = ("id", "created_at"),
        force_touch_when_empty: bool = True,
    ) -> T:
        if isinstance(obj_in, BaseModel):
            data = obj_in.model_dump(exclude_unset=True)
        else:
            data = dict(obj_in)

        data = {
            k: v
            for k, v in data.items()
            if k not in protected and (v is not None or not ignore_none)
        }

        try:
            if not data:
                if force_touch_when_empty and hasattr(self.model, "updated_at"):
                    await db.execute(
                        sa_update(self.model)
                        .where(self.model.id == db_obj.id)
                        .values(updated_at=func.now())
                    )
                    await db.commit()
                    await db.refresh(db_obj)
                return db_obj

            for field, value in data.items():
                setattr(db_obj, field, value)

            await db.flush()
            await db.commit()
            await db.refresh(db_obj)
            return db_obj

        except Exception:
            await db.rollback()
            raise
