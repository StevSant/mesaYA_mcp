"""Tool: complete_reservation - Mark a reservation as completed."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client


@mcp.tool()
async def complete_reservation(reservation_id: str) -> str:
    """Mark a reservation as completed after guests leave.

    Args:
        reservation_id: UUID of the reservation.

    Returns:
        Confirmation of completion.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Completing reservation",
        context="complete_reservation",
        reservation_id=reservation_id,
    )

    try:
        if not reservation_id:
            return "❌ Error: reservation_id is required"

        response = await http_client.patch(
            f"/api/v1/reservations/{reservation_id}/complete",
            json={},
        )

        if response is None:
            return f"❌ Error: Unable to complete reservation '{reservation_id}'"

        res_id = response.get("id", reservation_id)[:8]

        return f"✅ Reservation #{res_id} has been marked as completed. Thank you!"

    except Exception as e:
        logger.error(
            "Failed to complete reservation",
            error=str(e),
            context="complete_reservation",
        )
        return f"❌ Error completing reservation: {str(e)}"
