import random

from sqlalchemy.orm import Session


class PaymentService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def process_payment(
        self,
        order_id: int,
        amount: float,
        payment_method: str,
    ) -> dict:
        """
        Simulated payment processing
        In a real application, this would integrate with
        payment processors like Stripe, PayPal, etc.
        """

        # Simulate payment processing delay and random success/failure
        success_rate = 0.9  # 90% success rate for simulation
        transaction_id = f"txn_{order_id}_{random.randint(1000, 9999)}"

        if random.random() < success_rate:
            return {
                "status": "completed",
                "transaction_id": transaction_id,
                "amount": amount,
                "payment_method": payment_method,
            }
        else:
            return {
                "status": "failed",
                "error": "Payment processing failed",
                "amount": amount,
                "payment_method": payment_method,
            }

    def refund_payment(
        self,
        transaction_id: str,
        amount: float,
    ) -> dict:
        """
        Simulated refund processing
        """
        return {
            "status": "refunded",
            "refund_id": f"ref_{transaction_id}_{random.randint(1000, 9999)}",
            "amount": amount,
        }
