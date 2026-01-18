from typing import Optional
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float, ARRAY, Enum
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base
# from .cart_item import CartItem
# from .user import User


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    total_amount: Mapped[float] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="carts")

    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="cart")