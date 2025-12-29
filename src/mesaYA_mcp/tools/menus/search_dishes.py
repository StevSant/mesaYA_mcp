"""Search dishes tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.shared.application.services.entity_resolver import resolve_restaurant_id
from mesaYA_mcp.tools.dtos.menus import SearchDishesDto


@mcp.tool()
async def search_dishes(dto: SearchDishesDto) -> str:
    """Search for dishes across menus.

    You can filter by restaurant name instead of UUID.
    Examples:
    - query: "pizza"
    - restaurant: "Pizza Palace"
    - category: "main"

    Args:
        dto: Search parameters including query, restaurant name, category, max_price, vegetarian, limit.

    Returns:
        List of matching dishes in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Searching dishes",
        context="search_dishes",
        query=dto.query,
        restaurant=dto.restaurant,
    )

    try:
        params: dict = {"q": dto.query, "limit": dto.limit}

        # Resolve restaurant if provided
        if dto.restaurant:
            restaurant_id = await resolve_restaurant_id(dto.restaurant)
            if restaurant_id is None:
                return adapter.map_not_found("restaurant", dto.restaurant)
            params["restaurantId"] = restaurant_id

        if dto.category:
            params["category"] = dto.category
        if dto.max_price > 0:
            params["maxPrice"] = dto.max_price
        if dto.vegetarian:
            params["vegetarian"] = True

        response = await http_client.get("/api/v1/dishes/search", params=params)

        if response is None:
            return adapter.map_empty("dish", "search")

        if isinstance(response, dict):
            dishes = response.get("data", [])
        else:
            dishes = response

        if not dishes:
            return adapter.map_empty("dish", "search")

        return adapter.map_success(
            data=dishes,
            entity_type="dish",
            operation="search",
            count=len(dishes),
        )

    except Exception as e:
        logger.error("Failed to search dishes", error=str(e), context="search_dishes")
        return adapter.map_error(
            message=str(e),
            entity_type="dish",
            operation="search",
        )
