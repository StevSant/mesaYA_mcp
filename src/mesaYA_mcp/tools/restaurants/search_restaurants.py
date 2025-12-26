"""Search restaurants tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.mappers.adapters.toon_response_adapter import get_response_adapter
from mesaYA_mcp.tools.dtos.restaurants import SearchRestaurantsDto


@mcp.tool()
async def search_restaurants(dto: SearchRestaurantsDto) -> str:
    """Search for restaurants by name, cuisine type, city, or location.

    You can filter by specific fields like name, city, or cuisine type.
    Use the name filter when you know the restaurant name.
    Use the city filter for location-based search.

    Args:
        dto: Search parameters including name, city, cuisine_type, query, and limit.

    Returns:
        List of matching restaurants with basic info in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Searching restaurants",
        context="search_restaurants",
        name=dto.name,
        city=dto.city,
        cuisine_type=dto.cuisine_type,
        query=dto.query,
    )

    try:
        params: dict = {"limit": dto.limit}
        if dto.name:
            params["name"] = dto.name
        if dto.city:
            params["city"] = dto.city
        if dto.cuisine_type:
            params["cuisineType"] = dto.cuisine_type
        if dto.query:
            params["q"] = dto.query
        if dto.is_active:
            params["isActive"] = True

        response = await http_client.get("/api/v1/restaurants", params=params)

        if response is None:
            return adapter.map_empty("restaurant", "search")

        if isinstance(response, dict):
            restaurants = response.get("data", response.get("results", []))
            total = response.get("pagination", {}).get("totalItems", len(restaurants))
            if not restaurants and "results" not in response and "data" not in response:
                restaurants = [response] if response.get("id") else []
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
