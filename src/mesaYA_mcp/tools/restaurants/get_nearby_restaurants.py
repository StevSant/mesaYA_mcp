"""Get nearby restaurants tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools._formatters import format_restaurant
from mesaYA_mcp.tools.dtos.restaurants import NearbyRestaurantsDto


@mcp.tool()
async def get_nearby_restaurants(dto: NearbyRestaurantsDto) -> str:
    """Find restaurants near a geographic location.

    Args:
        dto: Location parameters including latitude, longitude, radius_km, and limit.

    Returns:
        List of nearby restaurants sorted by distance.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Finding nearby restaurants",
        context="get_nearby_restaurants",
        latitude=dto.latitude,
        longitude=dto.longitude,
        radius_km=dto.radius_km,
    )

    try:
        params = {
            "lat": dto.latitude,
            "lng": dto.longitude,
            "radius": dto.radius_km,
            "limit": dto.limit,
        }

        response = await http_client.get("/api/v1/restaurants/nearby", params=params)

        if response is None:
            return f"🔍 No restaurants found within {dto.radius_km}km of your location"

        if isinstance(response, dict):
            restaurants = response.get("data", [])
        else:
            restaurants = response

        if not restaurants:
            return f"🔍 No restaurants found within {dto.radius_km}km of your location"

        result = f"📍 Found {len(restaurants)} restaurants nearby:\n\n"
        for r in restaurants:
            distance = r.get("distance", 0)
            result += format_restaurant(r)
            if distance:
                result += f"   📏 Distance: {distance:.1f} km\n"
            result += "\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to find nearby restaurants",
            error=str(e),
            context="get_nearby_restaurants",
        )
        return f"❌ Error finding nearby restaurants: {str(e)}"
