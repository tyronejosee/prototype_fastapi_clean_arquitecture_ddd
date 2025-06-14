from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./ecommerce.db"

    # Security
    secret_key: str = "lorem-ipsum-dolor-sit-amet"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Application
    debug: bool = True

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
