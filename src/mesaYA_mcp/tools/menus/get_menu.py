"""Get menu tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools._formatters import format_menu
from mesaYA_mcp.tools.dtos.menus import MenuIdDto


@mcp.tool()
async def get_menu(dto: MenuIdDto) -> str:
    """Get detailed information about a specific menu.

    Args:
        dto: Menu ID parameter.

    Returns:
        Complete menu details including all dishes.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info("Getting menu details", context="get_menu", menu_id=dto.menu_id)

    try:
        response = await http_client.get(f"/api/v1/menus/{dto.menu_id}")

        if response is None:
            return f"❌ Menu with ID '{dto.menu_id}' not found"

        return format_menu(response)

    except Exception as e:
        logger.error("Failed to get menu", error=str(e), context="get_menu")
        return f"❌ Error getting menu: {str(e)}"
