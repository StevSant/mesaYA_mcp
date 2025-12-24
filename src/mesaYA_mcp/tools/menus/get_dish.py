"""Get dish tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools._formatters import format_dish
from mesaYA_mcp.tools.dtos.menus import DishIdDto


@mcp.tool()
async def get_dish(dto: DishIdDto) -> str:
    """Get detailed information about a specific dish.

    Args:
        dto: Dish ID parameter.

    Returns:
        Complete dish details including ingredients and allergens.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info("Getting dish details", context="get_dish", dish_id=dto.dish_id)

    try:
        response = await http_client.get(f"/api/v1/dishes/{dto.dish_id}")

        if response is None:
            return f"❌ Dish with ID '{dto.dish_id}' not found"

        return format_dish(response)

    except Exception as e:
        logger.error("Failed to get dish", error=str(e), context="get_dish")
        return f"❌ Error getting dish: {str(e)}"
