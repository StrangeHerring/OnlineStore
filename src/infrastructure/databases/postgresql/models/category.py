from typing import Optional
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float, ARRAY, Enum
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base
from .product import Product

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    products: Mapped[list["Product"]] = relationship(back_populates="category")