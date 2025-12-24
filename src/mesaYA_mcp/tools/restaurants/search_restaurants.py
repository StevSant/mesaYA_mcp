"""Search restaurants tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools._formatters import format_restaurant
from mesaYA_mcp.tools.dtos.restaurants import SearchRestaurantsDto


@mcp.tool()
async def search_restaurants(dto: SearchRestaurantsDto) -> str:
    """Search for restaurants by name, cuisine type, or location.

    Args:
        dto: Search parameters including query, cuisine_type, city, and limit.

    Returns:
        List of matching restaurants with basic info.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Searching restaurants",
        context="search_restaurants",
        query=dto.query,
        cuisine_type=dto.cuisine_type,
        city=dto.city,
    )

    try:
        params: dict = {"limit": dto.limit}
        if dto.query:
            params["q"] = dto.query
        if dto.cuisine_type:
            params["cuisineType"] = dto.cuisine_type
        if dto.city:
            params["city"] = dto.city

        response = await http_client.get("/api/v1/restaurants", params=params)

        if response is None:
            return "🔍 No restaurants found matching your criteria"

        if isinstance(response, dict):
            restaurants = response.get("data", [])
            total = response.get("pagination", {}).get("totalItems", len(restaurants))
        else:
            restaurants = response
            total = len(restaurants)

        if not restaurants:
            return "🔍 No restaurants found matching your criteria"

        result = f"🍽️ Found {total} restaurants:\n\n"
        for r in restaurants:
            result += format_restaurant(r) + "\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to search restaurants", error=str(e), context="search_restaurants"
        )
        return f"❌ Error searching restaurants: {str(e)}"
