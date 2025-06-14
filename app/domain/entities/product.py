from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.domain.entities.cart_item import CartItem
    from app.domain.entities.order_item import OrderItem


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[float] = mapped_column(nullable=False)
    stock: Mapped[int] = mapped_column(default=0)
    category: Mapped[Optional[str]] = mapped_column()
    image_url: Mapped[Optional[str]] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    cart_items: Mapped[list["CartItem"]] = relationship(
        back_populates="product",
    )
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product",
    )
