"""Cancel reservation tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.dtos.reservations import CancelReservationDto


@mcp.tool()
async def cancel_reservation(dto: CancelReservationDto) -> str:
    """Cancel a reservation.

    Args:
        dto: Cancellation parameters including reservation_id and optional reason.

    Returns:
        Confirmation of the cancellation.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Cancelling reservation",
        context="cancel_reservation",
        reservation_id=dto.reservation_id,
        reason=dto.reason,
    )

    try:
        payload = {}
        if dto.reason:
            payload["reason"] = dto.reason

        response = await http_client.patch(
            f"/api/v1/reservations/{dto.reservation_id}/cancel",
            json=payload,
        )

        if response is None:
            return f"❌ Error: Unable to cancel reservation '{dto.reservation_id}'"

        res_id = response.get("id", dto.reservation_id)[:8]

        result = f"🔴 Reservation #{res_id} has been cancelled.\n"
        if dto.reason:
            result += f"   Reason: {dto.reason}\n"

        return result

    except Exception as e:
        logger.error(
            "Failed to cancel reservation", error=str(e), context="cancel_reservation"
        )
        return f"❌ Error cancelling reservation: {str(e)}"
