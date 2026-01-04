"""Get restaurant schedule tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.shared.application.services.entity_resolver import resolve_restaurant_id
from mesaYA_mcp.tools.dtos.restaurants import RestaurantIdDto


@mcp.tool()
async def get_restaurant_schedule(dto: RestaurantIdDto) -> str:
    """Get restaurant hours. Args: restaurant (name/UUID). Returns: weekly schedule."""
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Getting restaurant schedule",
        context="get_restaurant_schedule",
        restaurant=dto.restaurant,
    )

    try:
        # Resolve restaurant by name or ID
        restaurant_id = await resolve_restaurant_id(dto.restaurant)

        if restaurant_id is None:
            return adapter.map_not_found("restaurant", dto.restaurant)

        # Use the correct endpoint: /api/v1/restaurants/{id}/schedule-slots
        response = await http_client.get(
            f"/api/v1/restaurants/{restaurant_id}/schedule-slots"
        )

        if response is None:
            return adapter.map_not_found("schedule", dto.restaurant)

        # Response is a list of schedule slots
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
