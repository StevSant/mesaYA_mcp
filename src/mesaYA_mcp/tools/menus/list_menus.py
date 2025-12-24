"""List menus tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.dtos.menus import ListMenusDto


@mcp.tool()
async def list_menus(dto: ListMenusDto) -> str:
    """List available menus, optionally filtered by restaurant.

    Args:
        dto: Filter parameters including restaurant_id, active_only, and limit.

    Returns:
        List of menus with basic information.
    """
    logger = get_logger()
    http_client = get_http_client()

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
            return "❌ Error: Unable to retrieve menus"

        if isinstance(response, dict):
            menus = response.get("data", [])
            total = response.get("pagination", {}).get("totalItems", len(menus))
        else:
            menus = response
            total = len(menus)

        if not menus:
            return "🔍 No menus found"

        result = f"📚 Found {total} menus:\n\n"

        for menu in menus:
            name = menu.get("name", "Unnamed Menu")
            menu_id = menu.get("id", "")[:8]
            is_active = menu.get("isActive", False)
            status = "✅ Active" if is_active else "⏸️ Inactive"
            description = menu.get("description", "")[:50]
            dishes_count = len(menu.get("dishes", []))

            result += f"📖 **{name}** (#{menu_id})\n"
            result += f"   Status: {status}\n"
            if description:
                result += f"   {description}...\n"
            if dishes_count > 0:
                result += f"   🍽️ {dishes_count} dishes\n"
            result += "\n"

        return result.strip()

    except Exception as e:
        logger.error("Failed to list menus", error=str(e), context="list_menus")
        return f"❌ Error listing menus: {str(e)}"
