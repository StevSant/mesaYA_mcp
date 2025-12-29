"""Get reservation analytics tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.application.require_access_decorator import require_access
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.shared.application.services.entity_resolver import resolve_restaurant_id
from mesaYA_mcp.tools.dtos.reservations import ReservationAnalyticsDto


@mcp.tool()
@require_access(AccessLevel.OWNER)
async def get_reservation_analytics(dto: ReservationAnalyticsDto) -> str:
    """Get reservation analytics and statistics.

    You can filter by restaurant name instead of UUID.
    Examples:
    - restaurant: "Pizza Palace"
    - date_from: "2025-01-01"
    - date_to: "2025-01-31"

    Requires OWNER access level or higher.

    Args:
        dto: Analytics parameters including restaurant name, date_from, date_to.

    Returns:
        Reservation statistics in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Getting reservation analytics",
        context="get_reservation_analytics",
        restaurant=dto.restaurant,
        date_from=dto.date_from,
        date_to=dto.date_to,
    )

    try:
        params: dict = {}

        # Resolve restaurant if provided
        if dto.restaurant:
            restaurant_id = await resolve_restaurant_id(dto.restaurant)
            if restaurant_id is None:
                return adapter.map_not_found("restaurant", dto.restaurant)
            params["restaurantId"] = restaurant_id

        if dto.date_from:
            params["dateFrom"] = dto.date_from
        if dto.date_to:
            params["dateTo"] = dto.date_to

        response = await http_client.get(
            "/api/v1/reservations/analytics", params=params
        )

        if response is None:
            return adapter.map_error(
                message="Unable to retrieve reservation analytics",
                entity_type="analytics",
                operation="get",
            )

        return adapter.map_success(
            data=response,
            entity_type="analytics",
            operation="get",
        )

    except Exception as e:
        logger.error(
            "Failed to get reservation analytics",
            error=str(e),
            context="get_reservation_analytics",
        )
        return adapter.map_error(
            message=str(e),
            entity_type="analytics",
            operation="get",
        )
