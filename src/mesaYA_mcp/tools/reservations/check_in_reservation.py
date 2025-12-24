"""Check-in reservation tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools._formatters import format_reservation
from mesaYA_mcp.tools.dtos.reservations import ReservationIdDto


@mcp.tool()
async def check_in_reservation(dto: ReservationIdDto) -> str:
    """Mark a reservation as checked in when guests arrive.

    Args:
        dto: Reservation ID parameter.

    Returns:
        Confirmation of check-in with reservation details.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Checking in reservation",
        context="check_in_reservation",
        reservation_id=dto.reservation_id,
    )

    try:
        response = await http_client.patch(
            f"/api/v1/reservations/{dto.reservation_id}/check-in",
            json={},
        )

        if response is None:
            return f"❌ Error: Unable to check in reservation '{dto.reservation_id}'"

        result = "🔵 Guests have been checked in!\n\n"
        result += format_reservation(response)

        return result

    except Exception as e:
        logger.error(
            "Failed to check in reservation",
            error=str(e),
            context="check_in_reservation",
        )
        return f"❌ Error checking in reservation: {str(e)}"
