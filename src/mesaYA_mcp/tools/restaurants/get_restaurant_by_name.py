"""Get restaurant by name tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.src.mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import get_response_adapter
from mesaYA_mcp.tools.dtos.restaurants import RestaurantNameDto


@mcp.tool()
async def get_restaurant_by_name(dto: RestaurantNameDto) -> str:
    """Get detailed information about a restaurant by its name.

    This is the preferred way to find a restaurant when you know its name,
    instead of requiring a UUID.

    Args:
        dto: Restaurant name parameter.

    Returns:
        Complete restaurant details in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Getting restaurant info by name",
        context="get_restaurant_by_name",
        name=dto.name,
    )

    try:
        # URL encode the name for the path
        from urllib.parse import quote

        encoded_name = quote(dto.name, safe="")
        response = await http_client.get(f"/api/v1/restaurants/by-name/{encoded_name}")

        if response is None:
            return adapter.map_not_found("restaurant", dto.name)

        return adapter.map_success(
            data=response,
            entity_type="restaurant",
            operation="get",
        )

    except Exception as e:
        logger.error(
            "Failed to get restaurant by name",
            error=str(e),
            context="get_restaurant_by_name",
        )
        return adapter.map_error(
            message=str(e),
            entity_type="restaurant",
            operation="get",
        )
