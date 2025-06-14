from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class _UserBase(BaseModel):
    email: EmailStr


class UserCreateSchema(_UserBase):
    password: str


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserInDBSchema(_UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserSchema(UserInDBSchema):
    pass
