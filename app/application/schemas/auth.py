from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshSchema(BaseModel):
    refresh_token: str


class UserLoginSchema(BaseModel):
    email: str
    password: str
