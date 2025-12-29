"""Get restaurant reservations tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.application.require_access_decorator import require_access
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.shared.application.services.entity_resolver import resolve_restaurant_id
from mesaYA_mcp.tools.dtos.reservations import RestaurantReservationsDto


@mcp.tool()
@require_access(AccessLevel.OWNER)
async def get_restaurant_reservations(dto: RestaurantReservationsDto) -> str:
    """Get all reservations for a specific restaurant.

    You can identify the restaurant by its name instead of UUID.
    Examples:
    - restaurant: "Pizza Palace"
    - restaurant: "La Trattoria"

    Requires OWNER access level or higher.

    Args:
        dto: Restaurant reservations parameters including restaurant name, date, status, limit.

    Returns:
        List of reservations for the restaurant in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Getting restaurant reservations",
        context="get_restaurant_reservations",
        restaurant=dto.restaurant,
        date=dto.date,
    )

    try:
        # Resolve restaurant by name or ID
        restaurant_id = await resolve_restaurant_id(dto.restaurant)
        if restaurant_id is None:
            return adapter.map_not_found("restaurant", dto.restaurant)

        params: dict = {"limit": dto.limit}
        if dto.date:
            params["date"] = dto.date
        if dto.status:
            params["status"] = dto.status

        response = await http_client.get(
            f"/api/v1/reservations/restaurant/{restaurant_id}",
            params=params,
        )

        if response is None:
            return adapter.map_not_found("reservation", dto.restaurant)

        if isinstance(response, dict):
            reservations = response.get("data", [])
        else:
            reservations = response

        if not reservations:
            return adapter.map_empty("reservation", "list")

        return adapter.map_success(
            data=reservations,
            entity_type="reservation",
            operation="list",
            count=len(reservations),
        )

    except Exception as e:
        logger.error(
            "Failed to get restaurant reservations",
            error=str(e),
            context="get_restaurant_reservations",
        )
        return adapter.map_error(
            message=str(e),
            entity_type="reservation",
            operation="list",
        )
