"""Container class - Simple dependency injection container.

Provides a service locator pattern for managing shared dependencies.
"""

from typing import Any


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
