"""Resolve restaurant by name or ID."""

from typing import Optional

from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.application.services.entity_resolver.utils import is_uuid


async def resolve_restaurant(identifier: str) -> Optional[dict]:
    """Resolve a restaurant by name or ID.

    If the identifier is a UUID, fetches the restaurant by ID.
    If the identifier is a name, searches for the restaurant by name.

    Args:
        identifier: Restaurant name or UUID.

    Returns:
        Restaurant data dict if found, None otherwise.
    """
    logger = get_logger()
    http_client = get_http_client()

    if not identifier or not identifier.strip():
        return None

    identifier = identifier.strip()

    try:
        if is_uuid(identifier):
            # Direct ID lookup
            logger.debug(
                "Resolving restaurant by ID",
                context="restaurant_resolver",
                identifier=identifier,
            )
            response = await http_client.get(f"/api/v1/restaurants/{identifier}")
            return response if response else None
        else:
            # Name lookup - first try search which handles encoding properly
            logger.debug(
                "Resolving restaurant by name using search",
                context="restaurant_resolver",
                name=identifier,
            )

            # Use search endpoint with name filter - httpx handles query param encoding
            search_response = await http_client.get(
                "/api/v1/restaurants", params={"name": identifier, "limit": 1}
            )

            logger.debug(
                "Restaurant search response",
                context="restaurant_resolver",
                response_type=type(search_response).__name__,
                response_is_none=search_response is None,
            )

            if search_response:
                if isinstance(search_response, dict):
                    restaurants = search_response.get(
                        "data", search_response.get("results", [])
                    )
                    if restaurants:
                        return restaurants[0]
                elif isinstance(search_response, list) and search_response:
                    return search_response[0]

            return None

    except Exception as e:
        logger.error(
            "Failed to resolve restaurant",
            error=str(e),
            context="restaurant_resolver",
            identifier=identifier,
        )
        return None
