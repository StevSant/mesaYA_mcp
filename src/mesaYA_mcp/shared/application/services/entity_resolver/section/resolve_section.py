"""Resolve section by name or ID."""

from typing import Optional

from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.application.services.entity_resolver.utils import is_uuid


async def resolve_section(
    identifier: str, restaurant_identifier: Optional[str] = None
) -> Optional[dict]:
    """Resolve a section by name or ID.

    If the identifier is a UUID, fetches the section by ID.
    If the identifier is a name and restaurant is provided, searches within that restaurant.

    Args:
        identifier: Section name or UUID.
        restaurant_identifier: Optional restaurant name or ID for context.

    Returns:
        Section data dict if found, None otherwise.
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
                "Resolving section by ID",
                context="section_resolver",
                identifier=identifier,
            )
            response = await http_client.get(f"/api/v1/sections/{identifier}")
            return response if response else None
        else:
            # Section name lookup requires restaurant context
            if not restaurant_identifier:
                logger.warning(
                    "Section name lookup requires restaurant context",
                    context="section_resolver",
                    section_name=identifier,
                )
                return None

            # First resolve the restaurant
            from mesaYA_mcp.shared.application.services.entity_resolver.restaurant import (
                resolve_restaurant_id,
            )

            restaurant_id = await resolve_restaurant_id(restaurant_identifier)
            if not restaurant_id:
                logger.warning(
                    "Could not resolve restaurant for section lookup",
                    context="section_resolver",
                    restaurant=restaurant_identifier,
                )
                return None

            # Get all sections for the restaurant
            logger.debug(
                "Resolving section by name within restaurant",
                context="section_resolver",
                section_name=identifier,
                restaurant_id=restaurant_id,
            )
            response = await http_client.get(
                f"/api/v1/restaurants/{restaurant_id}/sections"
            )

            if response:
                sections = (
                    response if isinstance(response, list) else response.get("data", [])
                )
                # Find section by name (case-insensitive)
                identifier_lower = identifier.lower()
                for section in sections:
                    if section.get("name", "").lower() == identifier_lower:
                        return section

            return None

    except Exception as e:
        logger.error(
            "Failed to resolve section",
            error=str(e),
            context="section_resolver",
            identifier=identifier,
        )
        return None
