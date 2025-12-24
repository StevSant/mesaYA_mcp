"""Tool: get_nearby_restaurants - Find restaurants near a location."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.restaurants._format import format_restaurant


@mcp.tool()
async def get_nearby_restaurants(
    latitude: float,
    longitude: float,
    radius_km: float = 5.0,
    limit: int = 10,
) -> str:
    """Find restaurants near a specific geographic location.

    Args:
        latitude: User's latitude coordinate.
        longitude: User's longitude coordinate.
        radius_km: Search radius in kilometers (default 5km, max 100km).
        limit: Maximum number of results (default 10, max 50).

    Returns:
        List of nearby restaurants with distance information.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Finding nearby restaurants",
        context="get_nearby_restaurants",
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
    )

    try:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "radiusKm": radius_km,
            "limit": limit,
        }

        response = await http_client.get("/api/v1/restaurants/nearby", params=params)

        if response is None:
            return "❌ Error: Unable to find nearby restaurants"

        restaurants = (
            response if isinstance(response, list) else response.get("data", [])
        )

        if not restaurants:
            return f"🔍 No restaurants found within {radius_km}km of your location"

        result = f"✅ Found {len(restaurants)} restaurants nearby:\n\n"
        for r in restaurants:
            distance = r.get("distance", "N/A")
            result += format_restaurant(r)
            result += f"\n   📏 Distance: {distance}km\n\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to find nearby restaurants",
            error=str(e),
            context="get_nearby_restaurants",
        )
        return f"❌ Error finding nearby restaurants: {str(e)}"
