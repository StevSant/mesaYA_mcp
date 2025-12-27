"""Get nearby restaurants tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.src.mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import get_response_adapter
from mesaYA_mcp.tools.dtos.restaurants import NearbyRestaurantsDto


@mcp.tool()
async def get_nearby_restaurants(dto: NearbyRestaurantsDto) -> str:
    """Find restaurants near a geographic location.

    Args:
        dto: Location parameters including latitude, longitude, radius_km, and limit.

    Returns:
        List of nearby restaurants sorted by distance in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

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
            return adapter.map_empty("restaurant", "nearby")

        if isinstance(response, dict):
            restaurants = response.get("data", [])
        else:
            restaurants = response

        if not restaurants:
            return adapter.map_empty("restaurant", "nearby")

        return adapter.map_success(
            data=restaurants,
            entity_type="restaurant",
            operation="nearby",
            count=len(restaurants),
        )

    except Exception as e:
        logger.error(
            "Failed to find nearby restaurants",
            error=str(e),
            context="get_nearby_restaurants",
        )
        return adapter.map_error(
            message=str(e),
            entity_type="restaurant",
            operation="nearby",
        )
