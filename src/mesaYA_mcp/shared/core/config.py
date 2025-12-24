"""Application configuration using pydantic-settings.

Centralizes all configuration in a single place using pydantic-settings
for validation and environment variable loading.
"""

from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Uses pydantic-settings for automatic env var loading and validation.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "mesaYA_mcp"
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    log_format_json: bool = True

    # Backend API configuration
    backend_api_url: str = "http://localhost:3000"
    backend_api_timeout: float = 30.0
    backend_api_key: str = ""

    @computed_field
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Singleton Settings instance.
    """
    return Settings()
