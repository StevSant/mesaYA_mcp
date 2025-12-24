"""Search dishes tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools._formatters import format_dish
from mesaYA_mcp.tools.dtos.menus import SearchDishesDto


@mcp.tool()
async def search_dishes(dto: SearchDishesDto) -> str:
    """Search for dishes across menus.

    Args:
        dto: Search parameters including query, restaurant_id, category, max_price, vegetarian, limit.

    Returns:
        List of matching dishes with details.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Searching dishes",
        context="search_dishes",
        query=dto.query,
        restaurant_id=dto.restaurant_id,
    )

    try:
        params: dict = {"q": dto.query, "limit": dto.limit}
        if dto.restaurant_id:
            params["restaurantId"] = dto.restaurant_id
        if dto.category:
            params["category"] = dto.category
        if dto.max_price > 0:
            params["maxPrice"] = dto.max_price
        if dto.vegetarian:
            params["vegetarian"] = True

        response = await http_client.get("/api/v1/dishes/search", params=params)

        if response is None:
            return f"🔍 No dishes found matching '{dto.query}'"

        if isinstance(response, dict):
            dishes = response.get("data", [])
            total = response.get("pagination", {}).get("totalItems", len(dishes))
        else:
            dishes = response
            total = len(dishes)

        if not dishes:
            return f"🔍 No dishes found matching '{dto.query}'"

        result = f"🍽️ Found {total} dishes matching '{dto.query}':\n\n"

        for dish in dishes:
            result += format_dish(dish) + "\n"

        return result.strip()

    except Exception as e:
        logger.error("Failed to search dishes", error=str(e), context="search_dishes")
        return f"❌ Error searching dishes: {str(e)}"
