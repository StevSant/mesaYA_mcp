"""Complete reservation tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.src.mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import get_response_adapter
from mesaYA_mcp.tools.dtos.reservations import ReservationIdDto


@mcp.tool()
async def complete_reservation(dto: ReservationIdDto) -> str:
    """Mark a reservation as completed after guests leave.

    Args:
        dto: Reservation ID parameter.

    Returns:
        Confirmation of completion in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

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
            return adapter.map_error(
                message=f"Unable to complete reservation '{dto.reservation_id}'",
                entity_type="reservation",
                operation="complete",
            )

        return adapter.map_success(
            data=response,
            entity_type="reservation",
            operation="complete",
        )

    except Exception as e:
        logger.error(
            "Failed to complete reservation",
            error=str(e),
            context="complete_reservation",
        )
        return adapter.map_error(
            message=str(e),
            entity_type="reservation",
            operation="complete",
        )
