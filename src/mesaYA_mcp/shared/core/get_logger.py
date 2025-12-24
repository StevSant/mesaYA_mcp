"""Logger provider - Dependency injection function for logger.

Provides a FastAPI-style dependency injection function for getting the logger instance.
"""

import logging

from mesaYA_mcp.shared.core.container import Container
from mesaYA_mcp.shared.core.get_settings import get_settings


def get_logger():
    """Get the logger instance (FastAPI Depends-style).

    Lazily initializes and registers the logger on first call.

    Returns:
        LoggerPort: The configured logger instance.

    Example:
        >>> logger = get_logger()
        >>> logger.info("Message", context="my_function")
    """
    if not Container.has("logger"):
        from mesaYA_mcp.shared.infrastructure.adapters.logger_adapter import (
            LoggerAdapter,
        )

        settings = get_settings()
        log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
        logger = LoggerAdapter(
            name=settings.app_name,
            level=log_level,
            use_json=settings.log_format_json,
        )
        Container.register("logger", logger)

    return Container.resolve("logger")
