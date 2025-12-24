"""Tool: get_restaurant_reservations - Get reservations for a specific restaurant."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.reservations._format import format_reservation_summary


@mcp.tool()
async def get_restaurant_reservations(
    restaurant_id: str,
    date: str = "",
    status: str = "",
    limit: int = 50,
) -> str:
    """Get all reservations for a specific restaurant.

    Args:
        restaurant_id: UUID of the restaurant.
        date: Optional date filter in YYYY-MM-DD format.
        status: Optional status filter.
        limit: Maximum number of results (default 50).

    Returns:
        List of reservations for the restaurant.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting restaurant reservations",
        context="get_restaurant_reservations",
        restaurant_id=restaurant_id,
        date=date,
    )

    try:
        if not restaurant_id:
            return "❌ Error: restaurant_id is required"

        params: dict = {"limit": limit}
        if date:
            params["date"] = date
        if status:
            params["status"] = status

        response = await http_client.get(
            f"/api/v1/reservations/restaurant/{restaurant_id}",
            params=params,
        )

        if response is None:
            return (
                f"❌ Could not retrieve reservations for restaurant '{restaurant_id}'"
            )

        if isinstance(response, dict):
            reservations = response.get("data", [])
            total = response.get("pagination", {}).get("totalItems", len(reservations))
        else:
            reservations = response
            total = len(reservations)

        if not reservations:
            filter_msg = f" for date {date}" if date else ""
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
