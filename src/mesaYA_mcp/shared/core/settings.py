"""Settings class for application configuration.

Uses pydantic-settings for automatic environment variable loading and validation.
"""

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Uses pydantic-settings for automatic env var loading and validation.
    All settings can be overridden via environment variables or .env file.

    Example:
        >>> settings = Settings()
        >>> print(settings.backend_api_url)
        http://localhost:3000
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
    backend_api_host: str = "localhost"
    backend_api_port: int = 3000
    backend_api_timeout: float = 30.0
    backend_api_key: str = ""

    # MCP Gateway configuration (HTTP/SSE transport)
    mcp_gateway_host: str = "0.0.0.0"
    mcp_gateway_port: int = 8002
    mcp_transport: str = "stdio"  # "stdio" or "sse"

    # AI Provider API Keys (for sentiment analysis and vision tools)
    gemini_api_key: str = ""
    openai_api_key: str = ""
    groq_api_key: str = ""

    # Supabase (for image storage)
    supabase_url: str = ""
    supabase_key: str = ""

    @computed_field
    @property
    def backend_api_url(self) -> str:
        """Construct full backend API URL from host and port."""
        return f"http://{self.backend_api_host}:{self.backend_api_port}"

    @computed_field
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    @computed_field
    @property
    def has_vision_model(self) -> bool:
        """Check if a vision-capable model is available."""
        return bool(self.gemini_api_key or self.openai_api_key)
