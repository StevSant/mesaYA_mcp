"""Get menu analytics tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.tools.dtos.menus import MenuAnalyticsDto


@mcp.tool()
async def get_menu_analytics(dto: MenuAnalyticsDto) -> str:
    """Get menu and dish analytics.

    Args:
        dto: Analytics parameters including restaurant_id, date_from, date_to.

    Returns:
        Menu statistics in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Getting menu analytics",
        context="get_menu_analytics",
        restaurant_id=dto.restaurant_id,
    )

    try:
        params: dict = {}
        if dto.restaurant_id:
            params["restaurantId"] = dto.restaurant_id
        if dto.date_from:
            params["dateFrom"] = dto.date_from
        if dto.date_to:
            params["dateTo"] = dto.date_to

        response = await http_client.get("/api/v1/menus/analytics", params=params)

        if response is None:
            return adapter.map_error(
                message="Unable to retrieve menu analytics",
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
            "Failed to get menu analytics", error=str(e), context="get_menu_analytics"
        )
        return adapter.map_error(
            message=str(e),
            entity_type="analytics",
            operation="get",
        )
