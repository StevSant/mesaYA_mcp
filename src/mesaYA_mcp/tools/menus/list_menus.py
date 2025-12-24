"""Tool: list_menus - List all menus for a restaurant."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.menus._format import format_menu


@mcp.tool()
async def list_menus(
    restaurant_id: str,
    active_only: bool = True,
    limit: int = 20,
) -> str:
    """List all menus for a restaurant.

    Args:
        restaurant_id: UUID of the restaurant.
        active_only: If True, only show active menus (default True).
        limit: Maximum number of results (default 20).

    Returns:
        List of menus with their details.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Listing menus",
        context="list_menus",
        restaurant_id=restaurant_id,
        active_only=active_only,
    )

    try:
        if not restaurant_id:
            return "❌ Error: restaurant_id is required"

        params: dict = {"limit": limit}
        if active_only:
            params["active"] = True

        response = await http_client.get(
            f"/api/v1/menus/restaurant/{restaurant_id}",
            params=params,
        )

        if response is None:
            return f"❌ Could not retrieve menus for restaurant '{restaurant_id}'"

        if isinstance(response, dict):
            menus = response.get("data", [])
            total = response.get("pagination", {}).get("totalItems", len(menus))
        else:
            menus = response
            total = len(menus)

        if not menus:
            return "🍽️ No menus found for this restaurant"

        result = f"🍽️ Found {total} menus:\n\n"
        for menu in menus:
            result += format_menu(menu) + "\n"

        return result.strip()

    except Exception as e:
        logger.error("Failed to list menus", error=str(e), context="list_menus")
        return f"❌ Error listing menus: {str(e)}"
