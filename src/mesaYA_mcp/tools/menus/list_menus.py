"""List menus tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.src.mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import get_response_adapter
from mesaYA_mcp.tools.dtos.menus import ListMenusDto


@mcp.tool()
async def list_menus(dto: ListMenusDto) -> str:
    """List available menus, optionally filtered by restaurant.

    Args:
        dto: Filter parameters including restaurant_id, active_only, and limit.

    Returns:
        List of menus in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Listing menus",
        context="list_menus",
        restaurant_id=dto.restaurant_id,
        active_only=dto.active_only,
    )

    try:
        params: dict = {"limit": dto.limit}
        if dto.restaurant_id:
            params["restaurantId"] = dto.restaurant_id
        if dto.active_only:
            params["isActive"] = True

        response = await http_client.get("/api/v1/menus", params=params)

        if response is None:
            return adapter.map_error(
                message="Unable to retrieve menus",
                entity_type="menu",
                operation="list",
            )

        if isinstance(response, dict):
            menus = response.get("data", [])
        else:
            menus = response

        if not menus:
            return adapter.map_empty("menu", "list")

        return adapter.map_success(
            data=menus,
            entity_type="menu",
            operation="list",
            count=len(menus),
        )

    except Exception as e:
        logger.error("Failed to list menus", error=str(e), context="list_menus")
        return adapter.map_error(
            message=str(e),
            entity_type="menu",
            operation="list",
        )
