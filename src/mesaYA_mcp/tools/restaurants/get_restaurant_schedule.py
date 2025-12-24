"""Tool: get_restaurant_schedule - Get restaurant operating hours."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client


DAYS_MAP = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
}


@mcp.tool()
async def get_restaurant_schedule(restaurant_id: str) -> str:
    """Get the operating hours/schedule of a restaurant.

    Args:
        restaurant_id: The UUID of the restaurant.

    Returns:
        Weekly schedule showing opening and closing times for each day.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting restaurant schedule",
        context="get_restaurant_schedule",
        restaurant_id=restaurant_id,
    )

    try:
        if not restaurant_id:
            return "❌ Error: restaurant_id is required"

        response = await http_client.get(
            f"/api/v1/restaurants/{restaurant_id}/schedule-slots"
        )

        if response is None:
            return f"❌ Could not retrieve schedule for restaurant '{restaurant_id}'"

        slots = response if isinstance(response, list) else []

        if not slots:
            return "📅 No schedule information available for this restaurant"

        result = "📅 **Restaurant Schedule:**\n\n"
        for slot in slots:
            day_num = slot.get("dayOfWeek", 0)
            day_name = DAYS_MAP.get(day_num, f"Day {day_num}")
            open_time = slot.get("openTime", "N/A")
            close_time = slot.get("closeTime", "N/A")
            is_closed = slot.get("isClosed", False)

            if is_closed:
                result += f"   {day_name}: Closed\n"
            else:
                result += f"   {day_name}: {open_time} - {close_time}\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to get restaurant schedule",
            error=str(e),
            context="get_restaurant_schedule",
        )
        return f"❌ Error getting restaurant schedule: {str(e)}"
