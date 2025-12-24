"""Tool: search_dishes - Search for dishes across menus."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.menus._format import format_dish


@mcp.tool()
async def search_dishes(
    query: str = "",
    category: str = "",
    dietary: str = "",
    price_max: float = 0,
    restaurant_id: str = "",
    limit: int = 20,
) -> str:
    """Search for dishes across all menus.

    Args:
        query: Search term for dish name or description.
        category: Filter by category (appetizer, main, dessert, etc.).
        dietary: Filter by dietary info (vegan, vegetarian, gluten-free, etc.).
        price_max: Maximum price filter.
        restaurant_id: Optional restaurant UUID to limit search.
        limit: Maximum number of results (default 20).

    Returns:
        List of matching dishes with details.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Searching dishes",
        context="search_dishes",
        query=query,
        category=category,
        dietary=dietary,
    )

    try:
        params: dict = {"limit": limit}

        if query:
            params["q"] = query
        if category:
            params["category"] = category
        if dietary:
            params["dietary"] = dietary
        if price_max > 0:
            params["priceMax"] = price_max
        if restaurant_id:
            params["restaurantId"] = restaurant_id

        response = await http_client.get("/api/v1/dishes", params=params)

        if response is None:
            return "❌ Error: Unable to search dishes"

        if isinstance(response, dict):
            dishes = response.get("data", [])
            total = response.get("pagination", {}).get("totalItems", len(dishes))
        else:
            dishes = response
            total = len(dishes)

        if not dishes:
            return "🔍 No dishes found matching your criteria"

        result = f"🍽️ Found {total} dishes:\n\n"
        for dish in dishes[:limit]:
            result += format_dish(dish) + "\n"

        return result.strip()

    except Exception as e:
        logger.error("Failed to search dishes", error=str(e), context="search_dishes")
        return f"❌ Error searching dishes: {str(e)}"
