from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.entities.order import Order
from app.application.services.payment_service import PaymentService
from app.infrastructure.repositories.cart_repository import CartRepository
from app.infrastructure.repositories.order_repository import OrderRepository
from app.infrastructure.repositories.product_repository import (
    ProductRepository,
)
from app.application.schemas.order import OrderCreateSchema


class CheckoutService:
    def __init__(self, db: Session) -> None:
        self.cart_repo = CartRepository(db)
        self.order_repo = OrderRepository(db)
        self.product_repo = ProductRepository(db)
        self.payment_service = PaymentService(db)

    def create_order_from_cart(
        self, user: User, order_create: OrderCreateSchema
    ) -> Order:
        # Get user's cart items
        cart_items = self.cart_repo.get_user_cart(user.id)
        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty"
            )

        # Verify stock availability and calculate total
        total_price = 0
        order_items_data = []

        for cart_item in cart_items:
            product = cart_item.product

            # Check stock availability
            if cart_item.quantity > product.stock:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for product: {product.name}",
                )

            item_total = product.price * cart_item.quantity
            total_price += item_total

            order_items_data.append(
                {
                    "product_id": product.id,
                    "quantity": cart_item.quantity,
                    "price": product.price,
                }
            )

        # Create order
        order = self.order_repo.create(user.id, total_price)

        # Add order items
        self.order_repo.add_order_items(order, order_items_data)

        # Create payment record
        payment = self.order_repo.create_payment(
            order.id,
            order_create.payment_method,
        )

        # Process payment (simulated)
        payment_result = self.payment_service.process_payment(
            order.id, total_price, order_create.payment_method
        )

        if payment_result["status"] == "completed":
            # Update payment status
            self.order_repo.update_payment_status(payment, "completed")

            # Update order status
            self.order_repo.update_order_status(order, "confirmed")

            # Update product stock
            for cart_item in cart_items:
                product = cart_item.product
                product.stock -= cart_item.quantity

            # Clear user's cart
            self.cart_repo.clear_cart(user.id)
        else:
            # Handle payment failure
            self.order_repo.update_payment_status(payment, "failed")
            self.order_repo.update_order_status(order, "cancelled")

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment processing failed",
            )

        # Return updated order with items
        return self.order_repo.get_by_id(order.id)
