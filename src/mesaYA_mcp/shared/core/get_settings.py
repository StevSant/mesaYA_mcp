"""Settings provider - Cached singleton for Settings access.

Provides a cached function to get the application settings instance.
"""

from functools import lru_cache

from mesaYA_mcp.shared.core.settings import Settings


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Singleton Settings instance.

    Example:
        >>> settings = get_settings()
        >>> print(settings.app_name)
        mesaYA_mcp
    """
    return Settings()
