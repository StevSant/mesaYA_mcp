"""Confirm reservation tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.tools.dtos.reservations import ReservationIdDto


@mcp.tool()
async def confirm_reservation(dto: ReservationIdDto) -> str:
    """Confirm pending reservation. Args: reservation_id. Returns: updated reservation."""
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

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
            return adapter.map_error(
                message=f"Unable to confirm reservation '{dto.reservation_id}'",
                entity_type="reservation",
                operation="confirm",
            )

        return adapter.map_success(
            data=response,
            entity_type="reservation",
            operation="confirm",
        )

    except Exception as e:
        logger.error(
            "Failed to confirm reservation", error=str(e), context="confirm_reservation"
        )
        return adapter.map_error(
            message=str(e),
            entity_type="reservation",
            operation="confirm",
        )
