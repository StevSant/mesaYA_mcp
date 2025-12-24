"""Dependency injection container with FastAPI-style Depends pattern.

Provides a simple service locator pattern combined with dependency
injection functions similar to FastAPI's Depends.
"""

import logging
from functools import lru_cache
from typing import Any

from mesaYA_mcp.shared.core.config import Settings, get_settings


class Container:
    """Simple dependency injection container.

    Stores singleton instances for dependency injection across the application.
    Follows the Service Locator pattern for managing shared dependencies.

    Example:
        >>> Container.register("logger", LoggerAdapter())
        >>> logger = Container.resolve("logger")
    """

    _instances: dict[str, Any] = {}

    @classmethod
    def register(cls, key: str, instance: Any) -> None:
        """Register a singleton instance.

        Args:
            key: Unique identifier for the dependency.
            instance: The instance to register.
        """
        cls._instances[key] = instance

    @classmethod
    def resolve(cls, key: str) -> Any:
        """Resolve a registered dependency.

        Args:
            key: Unique identifier for the dependency.

        Returns:
            The registered instance.

        Raises:
            KeyError: If the dependency is not registered.
        """
        if key not in cls._instances:
            raise KeyError(f"Dependency '{key}' not registered in container")
        return cls._instances[key]

    @classmethod
    def has(cls, key: str) -> bool:
        """Check if a dependency is registered.

        Args:
            key: Unique identifier for the dependency.

        Returns:
            True if registered, False otherwise.
        """
        return key in cls._instances

    @classmethod
    def clear(cls) -> None:
        """Clear all registered dependencies.

        Useful for testing to reset state between tests.
        """
        cls._instances.clear()

    @classmethod
    def get_or_none(cls, key: str) -> Any | None:
        """Get a dependency or None if not registered.

        Args:
            key: Unique identifier for the dependency.

        Returns:
            The registered instance or None.
        """
        return cls._instances.get(key)


# ============================================================================
# FastAPI-style Dependency Injection Functions
# ============================================================================


def get_logger():
    """Get the logger instance (FastAPI Depends-style).

    Returns:
        LoggerPort: The configured logger instance.

    Example:
        logger = get_logger()
        logger.info("Message", context="my_function")
    """
    from mesaYA_mcp.shared.application.ports.logger_port import LoggerPort

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


@lru_cache(maxsize=1)
def get_http_client():
    """Get the HTTP client for backend API calls (FastAPI Depends-style).

    Returns:
        HTTPClient: Configured HTTP client instance.
    """
    # TODO: Implement HTTP client adapter
    # For now, return None until we implement the adapter
    return None


def configure_dependencies(settings: Settings | None = None) -> None:
    """Configure all dependencies in the container.

    This should be called once at application startup.

    Args:
        settings: Optional settings instance. Uses default if not provided.
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
