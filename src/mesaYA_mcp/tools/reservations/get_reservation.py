"""Get reservation tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.application.require_access_decorator import require_access
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.tools.dtos.reservations import ReservationIdDto


@mcp.tool()
@require_access(AccessLevel.USER)
async def get_reservation(dto: ReservationIdDto) -> str:
    """Get reservation details. Requires USER+. Args: reservation_id. Returns: reservation data."""
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Getting reservation details",
        context="get_reservation",
        reservation_id=dto.reservation_id,
    )

    try:
        response = await http_client.get(f"/api/v1/reservations/{dto.reservation_id}")

        if response is None:
            return adapter.map_not_found("reservation", dto.reservation_id)

        return adapter.map_success(
            data=response,
            entity_type="reservation",
            operation="get",
        )

    except Exception as e:
        logger.error(
            "Failed to get reservation", error=str(e), context="get_reservation"
        )
        return adapter.map_error(
            message=str(e),
            entity_type="reservation",
            operation="get",
        )
