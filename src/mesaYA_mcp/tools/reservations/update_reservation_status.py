"""Tool: update_reservation_status - Update reservation status."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.reservations._format import format_reservation


VALID_STATUSES = [
    "pending",
    "confirmed",
    "cancelled",
    "completed",
    "no_show",
    "checked_in",
]


@mcp.tool()
async def update_reservation_status(
    reservation_id: str,
    new_status: str,
    reason: str = "",
) -> str:
    """Update the status of a reservation.

    Args:
        reservation_id: UUID of the reservation to update.
        new_status: New status (pending, confirmed, cancelled, completed, no_show, checked_in).
        reason: Optional reason for the status change.

    Returns:
        Confirmation of the status update.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Updating reservation status",
        context="update_reservation_status",
        reservation_id=reservation_id,
        new_status=new_status,
    )

    try:
        if not reservation_id:
            return "❌ Error: reservation_id is required"

        if new_status.lower() not in VALID_STATUSES:
            return (
                f"❌ Error: Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"
            )

        payload = {"status": new_status.lower()}
        if reason:
            payload["reason"] = reason

        response = await http_client.patch(
            f"/api/v1/reservations/{reservation_id}/status",
            json=payload,
        )

        if response is None:
            return f"❌ Error: Unable to update reservation '{reservation_id}'"

        result = f"✅ Reservation status updated to '{new_status}'!\n\n"
        result += format_reservation(response)

        return result

    except Exception as e:
        logger.error(
            "Failed to update reservation status",
            error=str(e),
            context="update_reservation_status",
        )
        return f"❌ Error updating reservation status: {str(e)}"
