"""Configure dependencies - Application startup configuration.

Provides the function to configure all dependencies at application startup.
"""

import logging

from mesaYA_mcp.shared.core.container import Container
from mesaYA_mcp.shared.core.settings import Settings
from mesaYA_mcp.shared.core.get_settings import get_settings


def configure_dependencies(settings: Settings | None = None) -> None:
    """Configure all dependencies in the container.

    This should be called once at application startup to initialize
    all required dependencies.

    Args:
        settings: Optional settings instance. Uses default if not provided.

    Example:
        >>> from mesaYA_mcp.shared.core import configure_dependencies, get_settings
        >>> settings = get_settings()
        >>> configure_dependencies(settings)
    """
    if settings is None:
        settings = get_settings()

    Container.register("settings", settings)

    # Initialize logger
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    from mesaYA_mcp.shared.infrastructure.adapters.logger_adapter import LoggerAdapter

    logger = LoggerAdapter(
        name=settings.app_name,
        level=log_level,
        use_json=settings.log_format_json,
    )
    Container.register("logger", logger)
