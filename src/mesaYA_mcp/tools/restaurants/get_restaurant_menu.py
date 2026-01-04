"""Get restaurant menu tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.shared.application.services.entity_resolver import resolve_restaurant_id
from mesaYA_mcp.tools.dtos.restaurants import RestaurantMenuDto


@mcp.tool()
async def get_restaurant_menu(dto: RestaurantMenuDto) -> str:
    """Get restaurant menu. Args: restaurant (name/UUID), active_only. Returns: menu with dishes."""
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Getting restaurant menu",
        context="get_restaurant_menu",
        restaurant=dto.restaurant,
    )

    try:
        # Resolve restaurant by name or ID
        restaurant_id = await resolve_restaurant_id(dto.restaurant)

        if restaurant_id is None:
            return adapter.map_not_found("restaurant", dto.restaurant)

        params = {}
        if dto.active_only:
            params["isActive"] = "true"

        # Use the correct endpoint: /api/v1/menus/restaurant/{restaurantId}
        response = await http_client.get(
            f"/api/v1/menus/restaurant/{restaurant_id}", params=params
        )

        if response is None:
            return adapter.map_not_found("menu", dto.restaurant)

        # Response is paginated: { results: [...], total, page, ... }
        if isinstance(response, dict):
            menus = response.get("results", response.get("data", []))
        else:
            menus = response if isinstance(response, list) else [response]

        if not menus:
            return adapter.map_empty("menu", "get")

        return adapter.map_success(
            data=menus,
            entity_type="menu",
            operation="get",
            count=len(menus),
        )

    except Exception as e:
        logger.error(
            "Failed to get restaurant menu",
            error=str(e),
            context="get_restaurant_menu",
        )
        return adapter.map_error(
            message=str(e),
            entity_type="menu",
            operation="get",
        )
