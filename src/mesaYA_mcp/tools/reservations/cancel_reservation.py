"""Cancel reservation tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.application.require_access_decorator import require_access
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.tools.dtos.reservations import CancelReservationDto


@mcp.tool()
@require_access(AccessLevel.USER)
async def cancel_reservation(dto: CancelReservationDto) -> str:
    """Cancel reservation. Requires USER+. Args: reservation_id, reason (opt). Returns: confirmation."""
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

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
            return adapter.map_error(
                message=f"Unable to cancel reservation '{dto.reservation_id}'",
                entity_type="reservation",
                operation="cancel",
            )

        return adapter.map_success(
            data=response,
            entity_type="reservation",
            operation="cancel",
        )

    except Exception as e:
        logger.error(
            "Failed to cancel reservation", error=str(e), context="cancel_reservation"
        )
        return adapter.map_error(
            message=str(e),
            entity_type="reservation",
            operation="cancel",
        )
