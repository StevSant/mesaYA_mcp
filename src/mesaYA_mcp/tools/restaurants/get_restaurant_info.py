"""Tool: get_restaurant_info - Get detailed restaurant information."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.restaurants._format import format_restaurant


@mcp.tool()
async def get_restaurant_info(restaurant_id: str) -> str:
    """Get detailed information about a specific restaurant.

    Args:
        restaurant_id: The UUID of the restaurant.

    Returns:
        Detailed restaurant information including name, cuisine, address, rating.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting restaurant info",
        context="get_restaurant_info",
        restaurant_id=restaurant_id,
    )

    try:
        if not restaurant_id:
            return "❌ Error: restaurant_id is required"

        response = await http_client.get(f"/api/v1/restaurants/{restaurant_id}")

        if response is None:
            return f"❌ Restaurant with ID '{restaurant_id}' not found"

        return format_restaurant(response)

    except Exception as e:
        logger.error(
            "Failed to get restaurant info", error=str(e), context="get_restaurant_info"
        )
        return f"❌ Error getting restaurant info: {str(e)}"
