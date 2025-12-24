"""TOON Response Adapter - Maps responses to TOON format.

Implements the ResponsePort interface using TOON format for
LLM-optimized output (40% fewer tokens than JSON).
"""

from typing import Any

from toon_format import encode

from mesaYA_mcp.mappers.ports.response_port import ResponsePort


class ToonResponseAdapter(ResponsePort):
    """Adapter that maps responses to TOON format.

    TOON (Token-Oriented Object Notation) is optimized for LLM consumption,
    providing 40% fewer tokens than JSON while maintaining readability.
    """

    def map_success(
        self,
        data: Any,
        entity_type: str,
        operation: str,
        count: int | None = None,
    ) -> str:
        """Map successful response to TOON format.

        Creates a consistent envelope structure:
        - status: success
        - entity: entity type
        - operation: operation performed
        - count: number of items (for lists)
        - data: the actual data in TOON format
        """
        envelope = {
            "status": "success",
            "entity": entity_type,
            "operation": operation,
        }

        if count is not None:
            envelope["count"] = count

        envelope["data"] = data

        return encode(envelope)

    def map_error(
        self,
        message: str,
        entity_type: str,
        operation: str,
        error_code: str | None = None,
    ) -> str:
        """Map error response to TOON format."""
        envelope = {
            "status": "error",
            "entity": entity_type,
            "operation": operation,
            "message": message,
        }

        if error_code:
            envelope["code"] = error_code

        return encode(envelope)

    def map_not_found(
        self,
        entity_type: str,
        identifier: str,
    ) -> str:
        """Map not found response to TOON format."""
        return encode(
            {
                "status": "not_found",
                "entity": entity_type,
                "identifier": identifier,
                "message": f"{entity_type} with ID '{identifier}' not found",
            }
        )

    def map_empty(
        self,
        entity_type: str,
        operation: str,
    ) -> str:
        """Map empty result to TOON format."""
        return encode(
            {
                "status": "empty",
                "entity": entity_type,
                "operation": operation,
                "count": 0,
                "data": [],
                "message": f"No {entity_type}s found",
            }
        )


# Singleton instance for use across the application
_adapter_instance: ToonResponseAdapter | None = None


def get_response_adapter() -> ToonResponseAdapter:
    """Get the singleton response adapter instance."""
    global _adapter_instance
    if _adapter_instance is None:
        _adapter_instance = ToonResponseAdapter()
    return _adapter_instance
