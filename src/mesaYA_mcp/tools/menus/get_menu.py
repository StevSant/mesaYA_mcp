"""Tool: get_menu - Get a specific menu by ID."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.menus._format import format_menu, format_dish


@mcp.tool()
async def get_menu(menu_id: str) -> str:
    """Get detailed information about a specific menu.

    Args:
        menu_id: The UUID of the menu.

    Returns:
        Complete menu details including all dishes.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting menu details",
        context="get_menu",
        menu_id=menu_id,
    )

    try:
        if not menu_id:
            return "❌ Error: menu_id is required"

        response = await http_client.get(f"/api/v1/menus/{menu_id}")

        if response is None:
            return f"❌ Menu with ID '{menu_id}' not found"

        result = format_menu(response)
        dishes = response.get("dishes", [])

        if dishes:
            result += "\n📋 **Dishes:**\n"
            for dish in dishes:
                result += "\n" + format_dish(dish)

        return result

    except Exception as e:
        logger.error("Failed to get menu", error=str(e), context="get_menu")
        return f"❌ Error getting menu: {str(e)}"
