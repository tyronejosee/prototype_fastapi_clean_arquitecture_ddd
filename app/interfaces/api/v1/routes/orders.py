from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.domain.entities.order import Order
from app.domain.entities.user import User
from app.infrastructure.repositories.order_repository import OrderRepository
from app.application.services.checkout_service import CheckoutService
from app.application.schemas.order import OrderSchema, OrderCreateSchema
from app.interfaces.api.dependencies import get_current_user

router = APIRouter()


@router.get("/", response_model=list[OrderSchema])
async def get_user_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Order]:
    order_repo = OrderRepository(db)
    return order_repo.get_user_orders(current_user.id)


@router.get("/{order_id}", response_model=OrderSchema)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Order:
    order_repo = OrderRepository(db)
    order = order_repo.get_by_id(order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Ensure user can only access their own orders
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this order",
        )

    return order


@router.post(
    "/checkout",
    response_model=OrderSchema,
    status_code=status.HTTP_201_CREATED,
)
async def checkout(
    order_create: OrderCreateSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    checkout_service = CheckoutService(db)
    return checkout_service.create_order_from_cart(current_user, order_create)
