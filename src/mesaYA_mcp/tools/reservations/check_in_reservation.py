"""Check-in reservation tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.mappers.adapters.toon_response_adapter import get_response_adapter
from mesaYA_mcp.tools.dtos.reservations import ReservationIdDto


@mcp.tool()
async def check_in_reservation(dto: ReservationIdDto) -> str:
    """Mark a reservation as checked in when guests arrive.

    Args:
        dto: Reservation ID parameter.

    Returns:
        Confirmation of check-in with reservation details in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

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
            return adapter.map_error(
                message=f"Unable to check in reservation '{dto.reservation_id}'",
                entity_type="reservation",
                operation="check-in",
            )

        return adapter.map_success(
            data=response,
            entity_type="reservation",
            operation="check-in",
        )

    except Exception as e:
        logger.error(
            "Failed to check in reservation",
            error=str(e),
            context="check_in_reservation",
        )
        return adapter.map_error(
            message=str(e),
            entity_type="reservation",
            operation="check-in",
        )
