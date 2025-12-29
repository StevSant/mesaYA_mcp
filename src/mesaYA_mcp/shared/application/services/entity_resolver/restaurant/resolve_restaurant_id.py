"""Resolve restaurant identifier to UUID."""

from typing import Optional

from mesaYA_mcp.shared.application.services.entity_resolver.utils import is_uuid
from mesaYA_mcp.shared.application.services.entity_resolver.restaurant.resolve_restaurant import (
    resolve_restaurant,
)


async def resolve_restaurant_id(identifier: str) -> Optional[str]:
    """Resolve a restaurant identifier to its UUID.

    Args:
        identifier: Restaurant name or UUID.

    Returns:
        Restaurant UUID if found, None otherwise.
    """
    if not identifier or not identifier.strip():
        return None

    identifier = identifier.strip()

    # If already a UUID, return as-is (but validate it exists)
    if is_uuid(identifier):
        restaurant = await resolve_restaurant(identifier)
        return identifier if restaurant else None

    # Otherwise resolve by name
    restaurant = await resolve_restaurant(identifier)
    if restaurant and isinstance(restaurant, dict):
        return restaurant.get("id")

    return None
