"""Update reservation status tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.tools.dtos.reservations import UpdateReservationStatusDto


@mcp.tool()
async def update_reservation_status(dto: UpdateReservationStatusDto) -> str:
    """Update the status of a reservation.

    Args:
        dto: Status update parameters including reservation_id, new_status, and reason.

    Returns:
        Confirmation of the status update in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Updating reservation status",
        context="update_reservation_status",
        reservation_id=dto.reservation_id,
        new_status=dto.new_status,
    )

    try:
        payload = {"status": dto.new_status}
        if dto.reason:
            payload["reason"] = dto.reason

        response = await http_client.patch(
            f"/api/v1/reservations/{dto.reservation_id}/status",
            json=payload,
        )

        if response is None:
            return adapter.map_error(
                message=f"Unable to update reservation '{dto.reservation_id}'",
                entity_type="reservation",
                operation="update",
            )

        return adapter.map_success(
            data=response,
            entity_type="reservation",
            operation="update",
        )

    except Exception as e:
        logger.error(
            "Failed to update reservation status",
            error=str(e),
            context="update_reservation_status",
        )
        return adapter.map_error(
            message=str(e),
            entity_type="reservation",
            operation="update",
        )
