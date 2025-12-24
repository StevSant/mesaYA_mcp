"""Get menu analytics tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.dtos.menus import MenuAnalyticsDto


@mcp.tool()
async def get_menu_analytics(dto: MenuAnalyticsDto) -> str:
    """Get menu and dish analytics.

    Args:
        dto: Analytics parameters including restaurant_id, date_from, date_to.

    Returns:
        Menu statistics including popular dishes, revenue, etc.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting menu analytics",
        context="get_menu_analytics",
        restaurant_id=dto.restaurant_id,
    )

    try:
        params: dict = {}
        if dto.restaurant_id:
            params["restaurantId"] = dto.restaurant_id
        if dto.date_from:
            params["dateFrom"] = dto.date_from
        if dto.date_to:
            params["dateTo"] = dto.date_to

        response = await http_client.get("/api/v1/menus/analytics", params=params)

        if response is None:
            return "❌ Error: Unable to retrieve menu analytics"

        total_dishes = response.get("totalDishes", 0)
        total_menus = response.get("totalMenus", 0)
        avg_price = response.get("averagePrice", 0)
        popular = response.get("popularDishes", [])
        by_category = response.get("byCategory", {})

        result = "📊 **Menu Analytics**\n\n"
        result += f"📚 Total Menus: {total_menus}\n"
        result += f"🍽️ Total Dishes: {total_dishes}\n"
        result += f"💰 Average Price: ${avg_price:.2f}\n\n"

        if popular:
            result += "⭐ **Most Popular Dishes:**\n"
            for i, dish in enumerate(popular[:5], 1):
                name = dish.get("name", "Unknown")
                orders = dish.get("orderCount", 0)
                result += f"   {i}. {name} ({orders} orders)\n"
            result += "\n"

        if by_category:
            result += "📁 **By Category:**\n"
            for category, count in by_category.items():
                result += f"   • {category.capitalize()}: {count} dishes\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to get menu analytics", error=str(e), context="get_menu_analytics"
        )
        return f"❌ Error getting menu analytics: {str(e)}"
