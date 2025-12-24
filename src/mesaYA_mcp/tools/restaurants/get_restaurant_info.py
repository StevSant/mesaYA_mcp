"""Get restaurant info tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.mappers.adapters.toon_response_adapter import get_response_adapter
from mesaYA_mcp.tools.dtos.restaurants import RestaurantIdDto


@mcp.tool()
async def get_restaurant_info(dto: RestaurantIdDto) -> str:
    """Get detailed information about a specific restaurant.

    Args:
        dto: Restaurant ID parameter.

    Returns:
        Complete restaurant details in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Getting restaurant info",
        context="get_restaurant_info",
        restaurant_id=dto.restaurant_id,
    )

    try:
        response = await http_client.get(f"/api/v1/restaurants/{dto.restaurant_id}")

        if response is None:
            return adapter.map_not_found("restaurant", dto.restaurant_id)

        return adapter.map_success(
            data=response,
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
