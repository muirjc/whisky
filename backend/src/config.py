"""Application configuration using pydantic-settings."""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: str = "postgresql+asyncpg://whisky:whisky@localhost:5432/whisky"
    database_url_test: str = (
        "postgresql+asyncpg://whisky_test:whisky_test@localhost:5433/whisky_test"
    )

    # Authentication
    jwt_secret_key: str = "change-this-to-a-secure-random-string-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Application
    debug: bool = True
    log_level: str = "DEBUG"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # Rate Limiting
    rate_limit_login_per_minute: int = 5
    rate_limit_register_per_hour: int = 3
    rate_limit_password_reset_per_hour: int = 3

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
