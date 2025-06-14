from sqlalchemy.orm import Session, joinedload

from app.domain.entities.cart_item import CartItem
from app.application.schemas.cart import CartItemCreateSchema


class CartRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user_cart(self, user_id: int) -> list[CartItem]:
        return (
            self.db.query(CartItem)
            .filter(CartItem.user_id == user_id)
            .options(joinedload(CartItem.product))
            .all()
        )

    def get_cart_item(self, user_id: int, product_id: int) -> CartItem | None:
        return (
            self.db.query(CartItem)
            .filter(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id,
            )
            .first()
        )

    def add_item(
        self,
        user_id: int,
        cart_item_create: CartItemCreateSchema,
    ) -> CartItem:
        # Check if item already exists in cart
        existing_item = self.get_cart_item(
            user_id,
            cart_item_create.product_id,
        )

        if existing_item:
            # Update quantity if item exists
            existing_item.quantity += cart_item_create.quantity
            self.db.commit()
            self.db.refresh(existing_item)
            return existing_item
        else:
            # Create new cart item
            cart_item = CartItem(
                user_id=user_id,
                **cart_item_create.model_dump(),
            )
            self.db.add(cart_item)
            self.db.commit()
            self.db.refresh(cart_item)
            return cart_item

    def update_item(self, cart_item: CartItem, quantity: int) -> CartItem:
        cart_item.quantity = quantity
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def remove_item(self, cart_item: CartItem) -> None:
        self.db.delete(cart_item)
        self.db.commit()

    def clear_cart(self, user_id: int) -> None:
        self.db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        self.db.commit()
