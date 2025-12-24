"""Get reservation tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools._formatters import format_reservation
from mesaYA_mcp.tools.dtos.reservations import ReservationIdDto


@mcp.tool()
async def get_reservation(dto: ReservationIdDto) -> str:
    """Get detailed information about a specific reservation.

    Args:
        dto: Reservation ID parameter.

    Returns:
        Complete reservation details including status, time, and guest info.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting reservation details",
        context="get_reservation",
        reservation_id=dto.reservation_id,
    )

    try:
        response = await http_client.get(f"/api/v1/reservations/{dto.reservation_id}")

        if response is None:
            return f"❌ Reservation with ID '{dto.reservation_id}' not found"

        return format_reservation(response)

    except Exception as e:
        logger.error(
            "Failed to get reservation", error=str(e), context="get_reservation"
        )
        return f"❌ Error getting reservation: {str(e)}"
