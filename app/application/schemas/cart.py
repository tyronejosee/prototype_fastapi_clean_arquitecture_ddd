from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.application.schemas.product import ProductSchema


class _CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemCreateSchema(_CartItemBase):
    pass


class CartItemUpdateSchema(BaseModel):
    quantity: int


class CartItemInDBSchema(_CartItemBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CartItemSchema(CartItemInDBSchema):
    product: ProductSchema


class CartSchema(BaseModel):
    items: list[CartItemSchema]
    total_price: float
    total_items: int
