"""Tool: get_restaurant_menu - Get restaurant menu with dishes."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client


@mcp.tool()
async def get_restaurant_menu(restaurant_id: str) -> str:
    """Get the menu of a restaurant including all dishes.

    Args:
        restaurant_id: The UUID of the restaurant.

    Returns:
        Complete menu with all dishes, prices, and descriptions.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting restaurant menu",
        context="get_restaurant_menu",
        restaurant_id=restaurant_id,
    )

    try:
        if not restaurant_id:
            return "❌ Error: restaurant_id is required"

        response = await http_client.get(
            f"/api/v1/menus/restaurant/{restaurant_id}", params={"limit": 50}
        )

        if response is None:
            return f"❌ Could not retrieve menu for restaurant '{restaurant_id}'"

        menus = response.get("data", []) if isinstance(response, dict) else response

        if not menus:
            return "🍽️ No menu information available for this restaurant"

        result = "🍽️ **Restaurant Menu:**\n\n"
        for menu in menus:
            menu_name = menu.get("name", "Unnamed Menu")
            menu_desc = menu.get("description", "")
            menu_price = menu.get("price", 0)
            dishes = menu.get("dishes", [])

            result += f"📋 **{menu_name}** - ${menu_price:.2f}\n"
            if menu_desc:
                result += f"   {menu_desc}\n"

            if dishes:
                result += "   Dishes:\n"
                for dish in dishes:
                    dish_name = dish.get("name", "Unknown")
                    dish_price = dish.get("price", 0)
                    dish_desc = dish.get("description", "")
                    result += f"     • {dish_name} - ${dish_price:.2f}\n"
                    if dish_desc:
                        desc_text = (
                            f"{dish_desc[:80]}..." if len(dish_desc) > 80 else dish_desc
                        )
                        result += f"       {desc_text}\n"
            result += "\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to get restaurant menu", error=str(e), context="get_restaurant_menu"
        )
        return f"❌ Error getting restaurant menu: {str(e)}"
