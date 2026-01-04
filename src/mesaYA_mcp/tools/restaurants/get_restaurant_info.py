"""Get restaurant info tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.shared.application.services.entity_resolver import resolve_restaurant
from mesaYA_mcp.tools.dtos.restaurants import RestaurantIdDto


@mcp.tool()
async def get_restaurant_info(dto: RestaurantIdDto) -> str:
    """Get restaurant details by name or UUID.

    Args:
        dto: Restaurant identifier (name or UUID).

    Returns:
        Restaurant details in TOON format.
    """
    logger = get_logger()
    adapter = get_response_adapter()

    logger.info(
        "Getting restaurant info",
        context="get_restaurant_info",
        restaurant=dto.restaurant,
    )

    try:
        # Resolve restaurant by name or ID
        restaurant = await resolve_restaurant(dto.restaurant)

        if restaurant is None:
            return adapter.map_not_found("restaurant", dto.restaurant)

        return adapter.map_success(
            data=restaurant,
            entity_type="restaurant",
            operation="get",
        )

    except Exception as e:
        logger.error(
            "Failed to get restaurant info",
            error=str(e),
            context="get_restaurant_info",
        )
        return adapter.map_error(
            message=str(e),
            entity_type="restaurant",
            operation="get",
        )
