"""Get restaurant reservations tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools._formatters import format_reservation_summary
from mesaYA_mcp.tools.dtos.reservations import RestaurantReservationsDto


@mcp.tool()
async def get_restaurant_reservations(dto: RestaurantReservationsDto) -> str:
    """Get all reservations for a specific restaurant.

    Args:
        dto: Restaurant reservations parameters including restaurant_id, date, status, limit.

    Returns:
        List of reservations for the restaurant.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting restaurant reservations",
        context="get_restaurant_reservations",
        restaurant_id=dto.restaurant_id,
        date=dto.date,
    )

    try:
        params: dict = {"limit": dto.limit}
        if dto.date:
            params["date"] = dto.date
        if dto.status:
            params["status"] = dto.status

        response = await http_client.get(
            f"/api/v1/reservations/restaurant/{dto.restaurant_id}",
            params=params,
        )

        if response is None:
            return f"❌ Could not retrieve reservations for restaurant '{dto.restaurant_id}'"

        if isinstance(response, dict):
            reservations = response.get("data", [])
            total = response.get("pagination", {}).get("totalItems", len(reservations))
        else:
            reservations = response
            total = len(reservations)

        if not reservations:
            filter_msg = f" for date {dto.date}" if dto.date else ""
            return f"🔍 No reservations found{filter_msg}"

        result = f"📋 Found {total} reservations:\n\n"
        for r in reservations:
            result += format_reservation_summary(r) + "\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to get restaurant reservations",
            error=str(e),
            context="get_restaurant_reservations",
        )
        return f"❌ Error getting restaurant reservations: {str(e)}"
