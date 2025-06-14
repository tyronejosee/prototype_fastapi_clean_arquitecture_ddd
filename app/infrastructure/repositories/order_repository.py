from sqlalchemy.orm import Session, joinedload

from app.domain.entities.order import Order
from app.domain.entities.order_item import OrderItem
from app.domain.entities.payment import Payment


class OrderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user_orders(self, user_id: int) -> list[Order]:
        return (
            self.db.query(Order)
            .filter(Order.user_id == user_id)
            .options(
                joinedload(Order.order_items).joinedload(OrderItem.product),
            )
            .order_by(Order.created_at.desc())
            .all()
        )

    def get_by_id(self, order_id: int) -> Order:
        return (
            self.db.query(Order)
            .filter(Order.id == order_id)
            .options(
                joinedload(Order.order_items).joinedload(OrderItem.product),
            )
            .first()
        )

    def create(self, user_id: int, total_price: float) -> Order:
        order = Order(user_id=user_id, total_price=total_price)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def add_order_items(self, order: Order, order_items_data: list) -> None:
        for item_data in order_items_data:
            order_item = OrderItem(order_id=order.id, **item_data)
            self.db.add(order_item)

        self.db.commit()

    def create_payment(self, order_id: int, payment_method: str) -> Payment:
        payment = Payment(order_id=order_id, payment_method=payment_method)
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def update_order_status(self, order: Order, status: str) -> Order:
        order.status = status
        self.db.commit()
        self.db.refresh(order)
        return order

    def update_payment_status(self, payment: Payment, status: str) -> Payment:
        payment.status = status
        if status == "completed":
            from datetime import datetime

            payment.paid_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(payment)
        return payment
