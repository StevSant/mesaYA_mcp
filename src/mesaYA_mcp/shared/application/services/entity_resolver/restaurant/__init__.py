"""Restaurant resolver module."""

from mesaYA_mcp.shared.application.services.entity_resolver.restaurant.resolve_restaurant import (
    resolve_restaurant,
)
from mesaYA_mcp.shared.application.services.entity_resolver.restaurant.resolve_restaurant_id import (
    resolve_restaurant_id,
)

__all__ = ["resolve_restaurant", "resolve_restaurant_id"]
