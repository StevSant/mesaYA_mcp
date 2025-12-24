"""Tool: get_user_analytics - Get user activity analytics."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client


@mcp.tool()
async def get_user_analytics(
    user_id: str = "",
    date_from: str = "",
    date_to: str = "",
) -> str:
    """Get user activity analytics and statistics.

    Args:
        user_id: Optional user UUID for individual analytics.
        date_from: Start date for analytics period (YYYY-MM-DD).
        date_to: End date for analytics period (YYYY-MM-DD).

    Returns:
        User activity statistics including reservation counts, favorite restaurants, etc.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting user analytics",
        context="get_user_analytics",
        user_id=user_id,
        date_from=date_from,
        date_to=date_to,
    )

    try:
        params: dict = {}
        if user_id:
            params["userId"] = user_id
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to

        response = await http_client.get("/api/v1/users/analytics", params=params)

        if response is None:
            return "❌ Error: Unable to retrieve user analytics"

        total_users = response.get("totalUsers", 0)
        new_users = response.get("newUsers", 0)
        active_users = response.get("activeUsers", 0)
        by_role = response.get("byRole", {})
        top_customers = response.get("topCustomers", [])

        result = "📊 **User Analytics**\n\n"

        if user_id:
            reservations = response.get("totalReservations", 0)
            completed = response.get("completedReservations", 0)
            cancelled = response.get("cancelledReservations", 0)
            fav_restaurants = response.get("favoriteRestaurants", [])

            result += f"📋 Total Reservations: {reservations}\n"
            result += f"✅ Completed: {completed}\n"
            result += f"❌ Cancelled: {cancelled}\n"

            if fav_restaurants:
                result += "\n🏆 **Favorite Restaurants:**\n"
                for i, rest in enumerate(fav_restaurants[:5], 1):
                    name = rest.get("name", "Unknown")
                    visits = rest.get("visitCount", 0)
                    result += f"   {i}. {name} ({visits} visits)\n"
        else:
            result += f"👥 Total Users: {total_users}\n"
            result += f"🆕 New Users: {new_users}\n"
            result += f"🟢 Active Users: {active_users}\n\n"

            if by_role:
                result += "📁 **By Role:**\n"
                for role, count in by_role.items():
                    pct = (count / total_users * 100) if total_users > 0 else 0
                    result += f"   • {role.capitalize()}: {count} ({pct:.1f}%)\n"
                result += "\n"

            if top_customers:
                result += "🏆 **Top Customers:**\n"
                for i, customer in enumerate(top_customers[:5], 1):
                    name = customer.get("name", "Unknown")
                    reservations = customer.get("reservationCount", 0)
                    result += f"   {i}. {name} ({reservations} reservations)\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to get user analytics", error=str(e), context="get_user_analytics"
        )
        return f"❌ Error getting user analytics: {str(e)}"
