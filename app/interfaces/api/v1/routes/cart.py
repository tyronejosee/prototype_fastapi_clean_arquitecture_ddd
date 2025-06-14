from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.entities.cart_item import CartItem
from app.domain.entities.user import User
from app.application.services.cart_service import CartService
from app.application.schemas.cart import (
    CartSchema,
    CartItemSchema,
    CartItemCreateSchema,
    CartItemUpdateSchema,
)
from app.interfaces.api.dependencies import get_current_user

router = APIRouter()


@router.get("/", response_model=CartSchema)
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CartSchema:
    cart_service = CartService(db)
    return cart_service.get_user_cart(current_user)


@router.post(
    "/items",
    response_model=CartItemSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_to_cart(
    cart_item_create: CartItemCreateSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CartItem:
    cart_service = CartService(db)
    return cart_service.add_to_cart(current_user, cart_item_create)


@router.put("/items/{product_id}")
async def update_cart_item(
    product_id: int,
    cart_item_update: CartItemUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart_service = CartService(db)
    result = cart_service.update_cart_item(
        current_user, product_id, cart_item_update.quantity
    )

    if result is None:
        return {"message": "Item removed from cart"}

    return result


@router.delete("/items/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    cart_service = CartService(db)
    cart_service.remove_from_cart(current_user, product_id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    cart_service = CartService(db)
    cart_service.clear_cart(current_user)
