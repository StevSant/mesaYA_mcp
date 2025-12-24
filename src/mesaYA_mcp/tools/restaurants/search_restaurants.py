"""Tool: search_restaurants - Search restaurants by criteria."""

from typing import Any

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.restaurants._format import format_restaurant


@mcp.tool()
async def search_restaurants(
    query: str = "",
    cuisine: str = "",
    location: str = "",
    limit: int = 10,
) -> str:
    """Search for restaurants by name, cuisine type, or location.

    Args:
        query: Search term for restaurant name (optional).
        cuisine: Filter by cuisine type like 'Italian', 'Mexican', etc. (optional).
        location: Filter by city or address (optional).
        limit: Maximum number of results to return (default 10).

    Returns:
        Formatted list of matching restaurants with details.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Searching restaurants",
        context="search_restaurants",
        query=query,
        cuisine=cuisine,
        location=location,
    )

    try:
        params: dict[str, Any] = {"limit": limit}
        if query:
            params["q"] = query
        if cuisine:
            params["cuisineType"] = cuisine
        if location:
            params["city"] = location

        response = await http_client.get("/api/v1/restaurants", params=params)

        if response is None:
            return "❌ Error: Unable to connect to the restaurant service"

        if isinstance(response, dict):
            restaurants = response.get("data", [])
            total = response.get("pagination", {}).get("totalItems", len(restaurants))
        else:
            restaurants = response
            total = len(restaurants)

        if not restaurants:
            return "🔍 No restaurants found matching your criteria"

        result = f"✅ Found {total} restaurants:\n\n"
        for r in restaurants[:limit]:
            result += format_restaurant(r) + "\n\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to search restaurants", error=str(e), context="search_restaurants"
        )
        return f"❌ Error searching restaurants: {str(e)}"
