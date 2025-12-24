"""Restaurants tools - MCP tool implementations for restaurant operations.

Each tool follows the single responsibility principle and uses the
shared logger from the container for consistent logging.
"""

from mesaYA_mcp.shared.core import get_logger


async def search_restaurants(
    query: str = "",
    cuisine: str = "",
    location: str = "",
) -> str:
    """Search for restaurants by name, cuisine, or location.

    Args:
        query: Search term for restaurant name.
        cuisine: Filter by cuisine type.
        location: Filter by location/city.

    Returns:
        JSON string with search results or error message.
    """
    logger = get_logger()
    logger.info(
        "Searching restaurants",
        context="search_restaurants",
        query=query,
        cuisine=cuisine,
        location=location,
    )

    try:
        # TODO: Implement actual API call to backend
        # This is a placeholder implementation
        result = {
            "restaurants": [],
            "total": 0,
            "query": query,
            "filters": {"cuisine": cuisine, "location": location},
        }

        logger.debug(
            "Search completed",
            context="search_restaurants",
            total=result["total"],
        )

        return f"✅ Found {result['total']} restaurants matching your criteria"

    except Exception as e:
        logger.error(
            "Failed to search restaurants",
            error=e,
            context="search_restaurants",
        )
        return f"❌ Error searching restaurants: {str(e)}"


async def get_restaurant_info(restaurant_id: str) -> str:
    """Get detailed information about a specific restaurant.

    Args:
        restaurant_id: The unique identifier of the restaurant.

    Returns:
        JSON string with restaurant details or error message.
    """
    logger = get_logger()
    logger.info(
        "Getting restaurant info",
        context="get_restaurant_info",
        restaurant_id=restaurant_id,
    )

    try:
        if not restaurant_id:
            logger.warn(
                "Empty restaurant_id provided",
                context="get_restaurant_info",
            )
            return "❌ Error: restaurant_id is required"

        # TODO: Implement actual API call to backend
        # This is a placeholder implementation
        result = {
            "id": restaurant_id,
            "name": "Example Restaurant",
            "cuisine": "International",
            "rating": 4.5,
        }

        logger.debug(
            "Restaurant info retrieved",
            context="get_restaurant_info",
            restaurant_name=result["name"],
        )

        return f"✅ Restaurant: {result['name']} ({result['cuisine']}) - Rating: {result['rating']}"

    except Exception as e:
        logger.error(
            "Failed to get restaurant info",
            error=e,
            context="get_restaurant_info",
            restaurant_id=restaurant_id,
        )
        return f"❌ Error getting restaurant info: {str(e)}"
