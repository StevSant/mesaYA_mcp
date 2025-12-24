"""Get restaurant schedule tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.dtos.restaurants import RestaurantIdDto


DAYS_MAP = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}


@mcp.tool()
async def get_restaurant_schedule(dto: RestaurantIdDto) -> str:
    """Get the operating hours schedule for a restaurant.

    Args:
        dto: Restaurant ID parameter.

    Returns:
        Weekly schedule with opening and closing times for each day.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting restaurant schedule",
        context="get_restaurant_schedule",
        restaurant_id=dto.restaurant_id,
    )

    try:
        response = await http_client.get(
            f"/api/v1/restaurants/{dto.restaurant_id}/schedule"
        )

        if response is None:
            return f"❌ Schedule not found for restaurant '{dto.restaurant_id}'"

        schedules = response if isinstance(response, list) else response.get("data", [])

        if not schedules:
            return "📅 No schedule information available for this restaurant"

        result = "🕐 **Restaurant Schedule:**\n\n"

        for schedule in sorted(schedules, key=lambda x: x.get("dayOfWeek", 0)):
            day_num = schedule.get("dayOfWeek", 0)
            day_name = DAYS_MAP.get(day_num, f"Day {day_num}")
            open_time = schedule.get("openTime", "??:??")
            close_time = schedule.get("closeTime", "??:??")
            is_closed = schedule.get("isClosed", False)

            if is_closed:
                result += f"   {day_name}: 🔴 Closed\n"
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
