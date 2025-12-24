"""Get restaurant reservations tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.mappers.adapters.toon_response_adapter import get_response_adapter
from mesaYA_mcp.tools.dtos.reservations import RestaurantReservationsDto


@mcp.tool()
async def get_restaurant_reservations(dto: RestaurantReservationsDto) -> str:
    """Get all reservations for a specific restaurant.

    Args:
        dto: Restaurant reservations parameters including restaurant_id, date, status, limit.

    Returns:
        List of reservations for the restaurant in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Getting restaurant reservations",
        context="get_restaurant_reservations",
        restaurant_id=dto.restaurant_id,
        date=dto.date,
    )

    try:
        params: dict = {"limit": dto.limit}
        if dto.date:
            params["date"] = dto.date
        if dto.status:
            params["status"] = dto.status

        response = await http_client.get(
            f"/api/v1/reservations/restaurant/{dto.restaurant_id}",
            params=params,
        )

        if response is None:
            return adapter.map_not_found("reservation", dto.restaurant_id)

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
