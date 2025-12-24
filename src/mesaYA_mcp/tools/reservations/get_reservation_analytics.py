"""Get reservation analytics tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.dtos.reservations import ReservationAnalyticsDto


@mcp.tool()
async def get_reservation_analytics(dto: ReservationAnalyticsDto) -> str:
    """Get reservation analytics and statistics.

    Args:
        dto: Analytics parameters including restaurant_id, date_from, date_to.

    Returns:
        Reservation statistics including counts by status, peak times, etc.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting reservation analytics",
        context="get_reservation_analytics",
        restaurant_id=dto.restaurant_id,
        date_from=dto.date_from,
        date_to=dto.date_to,
    )

    try:
        params: dict = {}
        if dto.restaurant_id:
            params["restaurantId"] = dto.restaurant_id
        if dto.date_from:
            params["dateFrom"] = dto.date_from
        if dto.date_to:
            params["dateTo"] = dto.date_to

        response = await http_client.get(
            "/api/v1/reservations/analytics", params=params
        )

        if response is None:
            return "❌ Error: Unable to retrieve reservation analytics"

        total = response.get("total", 0)
        by_status = response.get("byStatus", {})
        avg_party = response.get("averagePartySize", 0)
        peak_hours = response.get("peakHours", [])
        peak_days = response.get("peakDays", [])

        result = "📊 **Reservation Analytics**\n\n"
        result += f"📈 Total Reservations: {total}\n"
        result += f"👥 Average Party Size: {avg_party:.1f}\n\n"

        if by_status:
            result += "📋 **By Status:**\n"
            for status, count in by_status.items():
                pct = (count / total * 100) if total > 0 else 0
                result += f"   • {status.capitalize()}: {count} ({pct:.1f}%)\n"
            result += "\n"

        if peak_hours:
            result += "⏰ **Peak Hours:** "
            result += ", ".join(peak_hours[:5]) + "\n"

        if peak_days:
            result += "📅 **Peak Days:** "
            result += ", ".join(peak_days[:3]) + "\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to get reservation analytics",
            error=str(e),
            context="get_reservation_analytics",
        )
        return f"❌ Error getting reservation analytics: {str(e)}"
