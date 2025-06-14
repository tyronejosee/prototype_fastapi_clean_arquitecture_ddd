from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.infrastructure.repositories.user_repository import UserRepository
from app.application.schemas.user import UserCreateSchema
from app.application.schemas.auth import UserLoginSchema
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)


class AuthService:
    def __init__(self, db: Session) -> None:
        self.user_repo = UserRepository(db)

    def register_user(self, user_create: UserCreateSchema) -> User:
        existing_user = self.user_repo.get_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        return self.user_repo.create(user_create)

    def authenticate_user(self, user_login: UserLoginSchema) -> dict:
        user = self.user_repo.get_by_email(user_login.email)
        if not user or not verify_password(
            user_login.password,
            str(user.hashed_password),
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        if not bool(user.is_active):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
            )

        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def refresh_token(self, refresh_token: str) -> dict:
        user_id = verify_token(refresh_token)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        user = self.user_repo.get_by_id(int(user_id))
        if not user or not bool(user.is_active):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )

        access_token = create_access_token(subject=user.id)
        new_refresh_token = create_refresh_token(subject=user.id)

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }

    def get_current_user(self, token: str) -> User:
        user_id = verify_token(token)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        user = self.user_repo.get_by_id(int(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user
