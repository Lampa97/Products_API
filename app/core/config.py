from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Игнорируем дополнительные поля из .env
    )

    # Database settings
    database_url: str = Field(
        default="postgresql://postgres:password@localhost:5432/products_db",
        description="PostgreSQL database connection URL",
    )

    redis_url: str = Field(default="redis://localhost:6379/0", description="Redis connection URL for Celery")

    # JWT authentication settings
    secret_key: str = Field(
        default="your-super-secret-key-change-in-production", description="Secret key for JWT tokens"
    )
    algorithm: str = Field(default="HS256", description="JWT encryption algorithm")
    access_token_expire_minutes: int = Field(default=30, description="JWT token lifetime in minutes")

    backend_cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"], description="Allowed CORS origins"
    )

    external_api_url: str = Field(
        default="https://dummyjson.com/products", description="External API URL for products synchronization"
    )

    external_api_provider: str = Field(
        default="dummyjson", description="External API provider type (dummyjson, custom, etc.)"
    )

    default_page_size: int = Field(default=20, description="Default page size")
    max_page_size: int = Field(default=100, description="Maximum page size")


settings = Settings()
