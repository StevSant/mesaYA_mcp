"""Response Port - Abstract interface for response mapping.

Defines the contract that all response adapters must implement.
"""

from abc import ABC, abstractmethod
from typing import Any


class ResponsePort(ABC):
    """Abstract port for mapping responses to output format.

    All response adapters must implement this interface to ensure
    consistent output format across the application.
    """

    @abstractmethod
    def map_success(
        self,
        data: Any,
        entity_type: str,
        operation: str,
        count: int | None = None,
    ) -> str:
        """Map successful response data to output format.

        Args:
            data: The data to map (dict, list, or primitive).
            entity_type: Type of entity (restaurant, reservation, menu, user).
            operation: Operation performed (get, list, create, update, delete).
            count: Optional count for list operations.

        Returns:
            Formatted string representation.
        """
        pass

    @abstractmethod
    def map_error(
        self,
        message: str,
        entity_type: str,
        operation: str,
        error_code: str | None = None,
    ) -> str:
        """Map error response to output format.

        Args:
            message: Error message.
            entity_type: Type of entity involved.
            operation: Operation that failed.
            error_code: Optional error code.

        Returns:
            Formatted error string.
        """
        pass

    @abstractmethod
    def map_not_found(
        self,
        entity_type: str,
        identifier: str,
    ) -> str:
        """Map not found response.

        Args:
            entity_type: Type of entity not found.
            identifier: The identifier that was searched.

        Returns:
            Formatted not found string.
        """
        pass

    @abstractmethod
    def map_empty(
        self,
        entity_type: str,
        operation: str,
    ) -> str:
        """Map empty result response.

        Args:
            entity_type: Type of entity.
            operation: Operation performed.

        Returns:
            Formatted empty result string.
        """
        pass
