"""Logger Port - Abstract interface for logging.

This port defines the contract for logger adapters, enabling
dependency inversion and easy switching between logging implementations.
"""

from abc import ABC, abstractmethod
from typing import Any


class LoggerPort(ABC):
    """Abstract interface for logging providers.

    Implementations of this port handle actual logging to different
    destinations (console, file, external services, etc.).

    This abstraction allows:
    - Easy switching between logging implementations
    - Testing with mock loggers
    - Clean separation of concerns
    - Consistent logging interface across the application
    """

    @abstractmethod
    def info(self, message: str, context: str | None = None, **meta: Any) -> None:
        """Log an informational message.

        Args:
            message: The log message.
            context: Optional context identifier (e.g., class/function name).
            **meta: Additional metadata to include in the log.
        """
        pass

    @abstractmethod
    def warn(self, message: str, context: str | None = None, **meta: Any) -> None:
        """Log a warning message.

        Args:
            message: The warning message.
            context: Optional context identifier.
            **meta: Additional metadata to include in the log.
        """
        pass

    @abstractmethod
    def error(
        self,
        message: str,
        error: Exception | None = None,
        context: str | None = None,
        **meta: Any,
    ) -> None:
        """Log an error message.

        Args:
            message: The error message.
            error: Optional exception instance.
            context: Optional context identifier.
            **meta: Additional metadata to include in the log.
        """
        pass

    @abstractmethod
    def debug(self, message: str, context: str | None = None, **meta: Any) -> None:
        """Log a debug message.

        Args:
            message: The debug message.
            context: Optional context identifier.
            **meta: Additional metadata to include in the log.
        """
        pass

    @abstractmethod
    def verbose(self, message: str, context: str | None = None, **meta: Any) -> None:
        """Log a verbose message.

        Args:
            message: The verbose message.
            context: Optional context identifier.
            **meta: Additional metadata to include in the log.
        """
        pass
