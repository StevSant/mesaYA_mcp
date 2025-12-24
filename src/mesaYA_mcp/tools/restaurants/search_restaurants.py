"""Search restaurants tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.mappers.adapters.toon_response_adapter import get_response_adapter
from mesaYA_mcp.tools.dtos.restaurants import SearchRestaurantsDto


@mcp.tool()
async def search_restaurants(dto: SearchRestaurantsDto) -> str:
    """Search for restaurants by name, cuisine type, or location.

    Args:
        dto: Search parameters including query, cuisine_type, city, and limit.

    Returns:
        List of matching restaurants with basic info in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

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
            return adapter.map_empty("restaurant", "search")

        if isinstance(response, dict):
            restaurants = response.get("data", [])
            total = response.get("pagination", {}).get("totalItems", len(restaurants))
        else:
            restaurants = response
            total = len(restaurants)

        if not restaurants:
            return adapter.map_empty("restaurant", "search")

        return adapter.map_success(
            data=restaurants,
            entity_type="restaurant",
            operation="search",
            count=total,
        )

    except Exception as e:
        logger.error(
            "Failed to search restaurants", error=str(e), context="search_restaurants"
        )
        return adapter.map_error(
            message=str(e),
            entity_type="restaurant",
            operation="search",
        )
