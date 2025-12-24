"""Confirm reservation tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools._formatters import format_reservation
from mesaYA_mcp.tools.dtos.reservations import ReservationIdDto


@mcp.tool()
async def confirm_reservation(dto: ReservationIdDto) -> str:
    """Confirm a pending reservation.

    Args:
        dto: Reservation ID parameter.

    Returns:
        Confirmation message with updated reservation details.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Confirming reservation",
        context="confirm_reservation",
        reservation_id=dto.reservation_id,
    )

    try:
        response = await http_client.patch(
            f"/api/v1/reservations/{dto.reservation_id}/confirm",
            json={},
        )

        if response is None:
            return f"❌ Error: Unable to confirm reservation '{dto.reservation_id}'"

        result = "✅ Reservation confirmed successfully!\n\n"
        result += format_reservation(response)

        return result

    except Exception as e:
        logger.error(
            "Failed to confirm reservation", error=str(e), context="confirm_reservation"
        )
        return f"❌ Error confirming reservation: {str(e)}"
