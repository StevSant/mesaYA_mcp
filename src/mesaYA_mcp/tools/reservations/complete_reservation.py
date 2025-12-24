"""Complete reservation tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.dtos.reservations import ReservationIdDto


@mcp.tool()
async def complete_reservation(dto: ReservationIdDto) -> str:
    """Mark a reservation as completed after guests leave.

    Args:
        dto: Reservation ID parameter.

    Returns:
        Confirmation of completion.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Completing reservation",
        context="complete_reservation",
        reservation_id=dto.reservation_id,
    )

    try:
        response = await http_client.patch(
            f"/api/v1/reservations/{dto.reservation_id}/complete",
            json={},
        )

        if response is None:
            return f"❌ Error: Unable to complete reservation '{dto.reservation_id}'"

        res_id = response.get("id", dto.reservation_id)[:8]

        return f"✅ Reservation #{res_id} has been marked as completed. Thank you!"

    except Exception as e:
        logger.error(
            "Failed to complete reservation",
            error=str(e),
            context="complete_reservation",
        )
        return f"❌ Error completing reservation: {str(e)}"
