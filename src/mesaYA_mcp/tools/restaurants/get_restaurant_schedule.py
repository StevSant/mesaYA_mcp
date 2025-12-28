"""Get restaurant schedule tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.tools.dtos.restaurants import RestaurantIdDto


@mcp.tool()
async def get_restaurant_schedule(dto: RestaurantIdDto) -> str:
    """Get the operating hours schedule for a restaurant.

    Args:
        dto: Restaurant ID parameter.

    Returns:
        Weekly schedule with opening and closing times in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Getting restaurant schedule",
        context="get_restaurant_schedule",
        restaurant_id=dto.restaurant_id,
    )

    try:
        response = await http_client.get(
            f"/api/v1/restaurants/{dto.restaurant_id}/schedule"
        )

        if response is None:
            return adapter.map_not_found("schedule", dto.restaurant_id)

        schedules = response if isinstance(response, list) else response.get("data", [])

        if not schedules:
            return adapter.map_empty("schedule", "get")

        return adapter.map_success(
            data=schedules,
            entity_type="schedule",
            operation="get",
            count=len(schedules),
        )

    except Exception as e:
        logger.error(
            "Failed to get restaurant schedule",
            error=str(e),
            context="get_restaurant_schedule",
        )
        return adapter.map_error(
            message=str(e),
            entity_type="schedule",
            operation="get",
        )
