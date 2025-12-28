"""Create reservation tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.application.require_access_decorator import require_access
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.tools.dtos.reservations import CreateReservationDto


@mcp.tool()
@require_access(AccessLevel.USER)
async def create_reservation(dto: CreateReservationDto) -> str:
    """Create a new reservation at a restaurant.

    Requires USER access level or higher.

    Args:
        dto: Reservation details including restaurant_id, customer_id, date, time, party_size.

    Returns:
        Confirmation with reservation details in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Creating reservation",
        context="create_reservation",
        restaurant_id=dto.restaurant_id,
        date=dto.date,
        time=dto.time,
        party_size=dto.party_size,
    )

    try:
        payload = {
            "restaurantId": dto.restaurant_id,
            "customerId": dto.customer_id,
            "reservationDate": dto.date,
            "reservationTime": dto.time,
            "partySize": dto.party_size,
        }

        if dto.table_id:
            payload["tableId"] = dto.table_id
        if dto.notes:
            payload["specialRequests"] = dto.notes

        response = await http_client.post("/api/v1/reservations", json=payload)

        if response is None:
            return adapter.map_error(
                message="Unable to create reservation. Service unavailable.",
                entity_type="reservation",
                operation="create",
            )

        return adapter.map_success(
            data=response,
            entity_type="reservation",
            operation="create",
        )

    except Exception as e:
        logger.error(
            "Failed to create reservation", error=str(e), context="create_reservation"
        )
        return adapter.map_error(
            message=str(e),
            entity_type="reservation",
            operation="create",
        )
