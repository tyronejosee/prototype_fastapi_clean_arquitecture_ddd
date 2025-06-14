from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.application.schemas.product import ProductSchema


class _OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float


class OrderItemInDBSchema(_OrderItemBase):
    id: int
    order_id: int

    model_config = ConfigDict(from_attributes=True)


class OrderItemSchema(OrderItemInDBSchema):
    product: ProductSchema


class _OrderBase(BaseModel):
    total_price: float
    status: str = "pending"


class OrderCreateSchema(BaseModel):
    payment_method: str = "credit_card"


class OrderInDBSchema(_OrderBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderSchema(OrderInDBSchema):
    order_items: List[OrderItemSchema]


class _PaymentBase(BaseModel):
    payment_method: str
    status: str = "pending"


class PaymentInDBSchema(_PaymentBase):
    id: int
    order_id: int
    paid_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaymentSchema(PaymentInDBSchema):
    pass
