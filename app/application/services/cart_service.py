from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domain.entities.cart_item import CartItem
from app.infrastructure.repositories.cart_repository import CartRepository
from app.infrastructure.repositories.product_repository import (
    ProductRepository,
)

from app.domain.entities.user import User
from app.application.schemas.cart import (
    CartItemCreateSchema,
    CartSchema,
)


class CartService:
    def __init__(self, db: Session) -> None:
        self.cart_repo = CartRepository(db)
        self.product_repo = ProductRepository(db)

    def get_user_cart(self, user: User) -> CartSchema:
        cart_items = self.cart_repo.get_user_cart(user.id)

        total_price = 0
        total_items = 0

        for item in cart_items:
            total_price += item.product.price * item.quantity
            total_items += item.quantity

        return CartSchema(
            items=list(cart_items),
            total_price=total_price,
            total_items=total_items,
        )

    def add_to_cart(
        self,
        user: User,
        cart_item_create: CartItemCreateSchema,
    ) -> CartItem:
        # Verify product exists and has sufficient stock
        product = self.product_repo.get_by_id(cart_item_create.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        product_id = getattr(product, "id", None)
        if product_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        # Check existing cart item to verify total quantity
        existing_item = self.cart_repo.get_cart_item(
            user.id,
            product_id,
        )
        total_quantity = cart_item_create.quantity
        if existing_item:
            total_quantity += existing_item.quantity

        if total_quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock",
            )

        return self.cart_repo.add_item(user.id, cart_item_create)

    def update_cart_item(
        self,
        user: User,
        product_id: int,
        quantity: int,
    ) -> CartItem | None:
        cart_item = self.cart_repo.get_cart_item(user.id, product_id)
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found",
            )

        # Verify sufficient stock
        if quantity > cart_item.product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock",
            )

        if quantity <= 0:
            self.cart_repo.remove_item(cart_item)
            return None

        return self.cart_repo.update_item(cart_item, quantity)

    def remove_from_cart(self, user: User, product_id: int) -> None:
        cart_item = self.cart_repo.get_cart_item(user.id, product_id)
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found",
            )

        self.cart_repo.remove_item(cart_item)

    def clear_cart(self, user: User) -> None:
        self.cart_repo.clear_cart(user.id)
