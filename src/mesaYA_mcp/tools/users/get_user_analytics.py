"""Get user analytics tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.dtos.users import UserAnalyticsDto


@mcp.tool()
async def get_user_analytics(dto: UserAnalyticsDto) -> str:
    """Get user analytics and statistics.

    Args:
        dto: Analytics parameters including restaurant_id, date_from, date_to.

    Returns:
        User statistics including counts by role, activity metrics, etc.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting user analytics",
        context="get_user_analytics",
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

        response = await http_client.get("/api/v1/users/analytics", params=params)

        if response is None:
            return "❌ Error: Unable to retrieve user analytics"

        total = response.get("totalUsers", 0)
        by_role = response.get("byRole", {})
        active = response.get("activeUsers", 0)
        new_this_month = response.get("newThisMonth", 0)
        top_customers = response.get("topCustomers", [])

        result = "📊 **User Analytics**\n\n"
        result += f"👥 Total Users: {total}\n"
        result += f"✅ Active Users: {active}\n"
        result += f"🆕 New This Month: {new_this_month}\n\n"

        if by_role:
            result += "📋 **By Role:**\n"
            for role, count in by_role.items():
                pct = (count / total * 100) if total > 0 else 0
                result += f"   • {role.capitalize()}: {count} ({pct:.1f}%)\n"
            result += "\n"

        if top_customers:
            result += "⭐ **Top Customers:**\n"
            for i, cust in enumerate(top_customers[:5], 1):
                name = cust.get("name", "Unknown")
                reservations = cust.get("reservationCount", 0)
                result += f"   {i}. {name} ({reservations} reservations)\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to get user analytics", error=str(e), context="get_user_analytics"
        )
        return f"❌ Error getting user analytics: {str(e)}"
