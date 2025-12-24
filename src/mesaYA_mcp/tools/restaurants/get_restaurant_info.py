"""Get restaurant info tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools._formatters import format_restaurant
from mesaYA_mcp.tools.dtos.restaurants import RestaurantIdDto


@mcp.tool()
async def get_restaurant_info(dto: RestaurantIdDto) -> str:
    """Get detailed information about a specific restaurant.

    Args:
        dto: Restaurant ID parameter.

    Returns:
        Complete restaurant details including contact, hours, and features.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting restaurant info",
        context="get_restaurant_info",
        restaurant_id=dto.restaurant_id,
    )

    try:
        response = await http_client.get(f"/api/v1/restaurants/{dto.restaurant_id}")

        if response is None:
            return f"❌ Restaurant with ID '{dto.restaurant_id}' not found"

        return format_restaurant(response)

    except Exception as e:
        logger.error(
            "Failed to get restaurant info",
            error=str(e),
            context="get_restaurant_info",
        )
        return f"❌ Error getting restaurant info: {str(e)}"
