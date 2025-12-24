"""Tool: cancel_reservation - Cancel a reservation."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client


@mcp.tool()
async def cancel_reservation(
    reservation_id: str,
    reason: str = "",
) -> str:
    """Cancel a reservation.

    Args:
        reservation_id: UUID of the reservation to cancel.
        reason: Optional reason for cancellation.

    Returns:
        Confirmation of the cancellation.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Cancelling reservation",
        context="cancel_reservation",
        reservation_id=reservation_id,
        reason=reason,
    )

    try:
        if not reservation_id:
            return "❌ Error: reservation_id is required"

        payload = {}
        if reason:
            payload["reason"] = reason

        response = await http_client.patch(
            f"/api/v1/reservations/{reservation_id}/cancel",
            json=payload,
        )

        if response is None:
            return f"❌ Error: Unable to cancel reservation '{reservation_id}'"

        res_id = response.get("id", reservation_id)[:8]

        result = f"🔴 Reservation #{res_id} has been cancelled.\n"
        if reason:
            result += f"   Reason: {reason}\n"

        return result

    except Exception as e:
        logger.error(
            "Failed to cancel reservation", error=str(e), context="cancel_reservation"
        )
        return f"❌ Error cancelling reservation: {str(e)}"
