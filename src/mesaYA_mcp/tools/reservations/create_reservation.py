"""Create reservation tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.application.require_access_decorator import require_access
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.shared.application.services.entity_resolver import (
    resolve_restaurant_id,
    resolve_user_id,
)
from mesaYA_mcp.tools.dtos.reservations import CreateReservationDto


@mcp.tool()
@require_access(AccessLevel.USER)
async def create_reservation(dto: CreateReservationDto) -> str:
    """Create a new reservation at a restaurant.

    You can identify the restaurant by name and the customer by email.
    No need to know internal UUIDs!

    Examples:
    - restaurant: "Pizza Palace"
    - customer_email: "john@example.com"
    - date: "2025-01-20"
    - time: "19:30"
    - party_size: 4

    Requires USER access level or higher.

    Args:
        dto: Reservation details including restaurant name, customer email, date, time, party_size.

    Returns:
        Confirmation with reservation details in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Creating reservation",
        context="create_reservation",
        restaurant=dto.restaurant,
        customer_email=dto.customer_email,
        date=dto.date,
        time=dto.time,
        party_size=dto.party_size,
    )

    try:
        # Resolve restaurant by name or ID
        restaurant_id = await resolve_restaurant_id(dto.restaurant)
        if restaurant_id is None:
            return adapter.map_not_found("restaurant", dto.restaurant)

        # Resolve customer by email
        customer_id = await resolve_user_id(dto.customer_email)
        if customer_id is None:
            return adapter.map_not_found("customer", dto.customer_email)

        payload = {
            "restaurantId": restaurant_id,
            "customerId": customer_id,
            "reservationDate": dto.date,
            "reservationTime": dto.time,
            "partySize": dto.party_size,
        }

        if dto.section_name:
            # TODO: Resolve section by name within restaurant
            payload["sectionName"] = dto.section_name
        if dto.table_name:
            payload["tableName"] = dto.table_name
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
