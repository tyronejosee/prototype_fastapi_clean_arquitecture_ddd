from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.entities.user import User
from app.application.services.auth_service import AuthService
from app.application.schemas.user import UserCreateSchema, UserSchema
from app.application.schemas.auth import (
    TokenSchema,
    TokenRefreshSchema,
    UserLoginSchema,
)

router = APIRouter()


@router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_create: UserCreateSchema,
    db: Session = Depends(get_db),
) -> User:
    auth_service = AuthService(db)
    return auth_service.register_user(user_create)


@router.post("/login", response_model=TokenSchema)
async def login(
    user_login: UserLoginSchema,
    db: Session = Depends(get_db),
) -> dict:
    auth_service = AuthService(db)
    return auth_service.authenticate_user(user_login)


@router.post("/refresh", response_model=TokenSchema)
async def refresh_token(
    token_refresh: TokenRefreshSchema,
    db: Session = Depends(get_db),
) -> dict:
    auth_service = AuthService(db)
    return auth_service.refresh_token(token_refresh.refresh_token)
