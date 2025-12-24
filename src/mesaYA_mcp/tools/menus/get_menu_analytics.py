"""Tool: get_menu_analytics - Get menu performance analytics."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client


@mcp.tool()
async def get_menu_analytics(
    restaurant_id: str,
    date_from: str = "",
    date_to: str = "",
) -> str:
    """Get menu and dish performance analytics.

    Args:
        restaurant_id: UUID of the restaurant.
        date_from: Start date for analytics period (YYYY-MM-DD).
        date_to: End date for analytics period (YYYY-MM-DD).

    Returns:
        Menu statistics including popular dishes, revenue data, etc.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting menu analytics",
        context="get_menu_analytics",
        restaurant_id=restaurant_id,
        date_from=date_from,
        date_to=date_to,
    )

    try:
        if not restaurant_id:
            return "❌ Error: restaurant_id is required"

        params: dict = {"restaurantId": restaurant_id}
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to

        response = await http_client.get("/api/v1/menus/analytics", params=params)

        if response is None:
            return "❌ Error: Unable to retrieve menu analytics"

        total_dishes = response.get("totalDishes", 0)
        total_menus = response.get("totalMenus", 0)
        top_dishes = response.get("topDishes", [])
        avg_price = response.get("averageDishPrice", 0)
        categories = response.get("categoryCounts", {})

        result = "📊 **Menu Analytics**\n\n"
        result += f"📋 Total Menus: {total_menus}\n"
        result += f"🍽️ Total Dishes: {total_dishes}\n"
        result += f"💰 Average Dish Price: ${avg_price:.2f}\n\n"

        if top_dishes:
            result += "🏆 **Top Dishes:**\n"
            for i, dish in enumerate(top_dishes[:5], 1):
                name = dish.get("name", "Unknown")
                orders = dish.get("orderCount", 0)
                result += f"   {i}. {name} ({orders} orders)\n"
            result += "\n"

        if categories:
            result += "📁 **By Category:**\n"
            for cat, count in categories.items():
                result += f"   • {cat}: {count} dishes\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to get menu analytics", error=str(e), context="get_menu_analytics"
        )
        return f"❌ Error getting menu analytics: {str(e)}"
