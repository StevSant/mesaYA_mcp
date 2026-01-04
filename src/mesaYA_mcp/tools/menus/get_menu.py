"""Get menu tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.tools.dtos.menus import MenuIdDto


@mcp.tool()
async def get_menu(dto: MenuIdDto) -> str:
    """Get menu details. Args: menu_id. Returns: menu data."""
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info("Getting menu details", context="get_menu", menu_id=dto.menu_id)

    try:
        response = await http_client.get(f"/api/v1/menus/{dto.menu_id}")

        if response is None:
            return adapter.map_not_found("menu", dto.menu_id)

        return adapter.map_success(
            data=response,
            entity_type="menu",
            operation="get",
        )

    except Exception as e:
        logger.error("Failed to get menu", error=str(e), context="get_menu")
        return adapter.map_error(
            message=str(e),
            entity_type="menu",
            operation="get",
        )
