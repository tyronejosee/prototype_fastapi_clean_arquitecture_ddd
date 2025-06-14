from fastapi import APIRouter, Depends

from app.domain.entities.user import User
from app.application.schemas.user import UserSchema
from app.interfaces.api.dependencies import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserSchema)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user
