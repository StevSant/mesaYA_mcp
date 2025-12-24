"""Tool: get_reservation - Get details of a specific reservation."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.reservations._format import format_reservation


@mcp.tool()
async def get_reservation(reservation_id: str) -> str:
    """Get detailed information about a specific reservation.

    Args:
        reservation_id: The UUID of the reservation.

    Returns:
        Complete reservation details including status, time, and guest info.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting reservation details",
        context="get_reservation",
        reservation_id=reservation_id,
    )

    try:
        if not reservation_id:
            return "❌ Error: reservation_id is required"

        response = await http_client.get(f"/api/v1/reservations/{reservation_id}")

        if response is None:
            return f"❌ Reservation with ID '{reservation_id}' not found"

        return format_reservation(response)

    except Exception as e:
        logger.error(
            "Failed to get reservation", error=str(e), context="get_reservation"
        )
        return f"❌ Error getting reservation: {str(e)}"
