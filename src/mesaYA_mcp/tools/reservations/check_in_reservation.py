"""Tool: check_in_reservation - Mark a reservation as checked in."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.reservations._format import format_reservation


@mcp.tool()
async def check_in_reservation(reservation_id: str) -> str:
    """Mark a reservation as checked in when guests arrive.

    Args:
        reservation_id: UUID of the reservation.

    Returns:
        Confirmation of check-in with reservation details.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Checking in reservation",
        context="check_in_reservation",
        reservation_id=reservation_id,
    )

    try:
        if not reservation_id:
            return "❌ Error: reservation_id is required"

        response = await http_client.patch(
            f"/api/v1/reservations/{reservation_id}/check-in",
            json={},
        )

        if response is None:
            return f"❌ Error: Unable to check in reservation '{reservation_id}'"

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
