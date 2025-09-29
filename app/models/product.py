from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    brand = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    description = Column(String)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", backref="products")
