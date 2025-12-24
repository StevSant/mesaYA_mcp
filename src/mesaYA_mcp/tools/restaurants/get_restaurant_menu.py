"""Get restaurant menu tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.mappers.adapters.toon_response_adapter import get_response_adapter
from mesaYA_mcp.tools.dtos.restaurants import RestaurantMenuDto


@mcp.tool()
async def get_restaurant_menu(dto: RestaurantMenuDto) -> str:
    """Get the menu for a restaurant including all dishes.

    Args:
        dto: Restaurant menu parameters including restaurant_id and active_only.

    Returns:
        Complete menu with categories and dishes in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Getting restaurant menu",
        context="get_restaurant_menu",
        restaurant_id=dto.restaurant_id,
    )

    try:
        params = {"isActive": dto.active_only} if dto.active_only else {}
        response = await http_client.get(
            f"/api/v1/restaurants/{dto.restaurant_id}/menu", params=params
        )

        if response is None:
            return adapter.map_not_found("menu", dto.restaurant_id)

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
