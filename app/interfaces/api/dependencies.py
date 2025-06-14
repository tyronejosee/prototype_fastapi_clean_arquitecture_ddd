from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.entities.user import User
from app.application.services.auth_service import AuthService

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    auth_service = AuthService(db)
    return auth_service.get_current_user(credentials.credentials)


def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not bool(current_user.is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource",
        )
    return current_user
