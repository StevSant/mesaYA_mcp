"""Tool: get_dish - Get details of a specific dish."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.menus._format import format_dish


@mcp.tool()
async def get_dish(dish_id: str) -> str:
    """Get detailed information about a specific dish.

    Args:
        dish_id: The UUID of the dish.

    Returns:
        Complete dish details including price, description, and dietary info.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting dish details",
        context="get_dish",
        dish_id=dish_id,
    )

    try:
        if not dish_id:
            return "❌ Error: dish_id is required"

        response = await http_client.get(f"/api/v1/dishes/{dish_id}")

        if response is None:
            return f"❌ Dish with ID '{dish_id}' not found"

        return format_dish(response)

    except Exception as e:
        logger.error("Failed to get dish", error=str(e), context="get_dish")
        return f"❌ Error getting dish: {str(e)}"
