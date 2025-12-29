"""Get restaurant sections tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.shared.application.services.entity_resolver import resolve_restaurant_id
from mesaYA_mcp.tools.dtos.restaurants import RestaurantIdDto


@mcp.tool()
async def get_restaurant_sections(dto: RestaurantIdDto) -> str:
    """Get the floor plan sections of a restaurant.

    You can use either the restaurant name or UUID to identify the restaurant.
    Examples:
    - restaurant: "Pizza Palace"
    - restaurant: "La Trattoria"

    Args:
        dto: Restaurant identifier (name or UUID).

    Returns:
        List of sections (dining areas) in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Getting restaurant sections",
        context="get_restaurant_sections",
        restaurant=dto.restaurant,
    )

    try:
        # Resolve restaurant by name or ID
        restaurant_id = await resolve_restaurant_id(dto.restaurant)

        if restaurant_id is None:
            return adapter.map_not_found("restaurant", dto.restaurant)

        response = await http_client.get(
            f"/api/v1/restaurants/{restaurant_id}/sections"
        )

        if response is None:
            return adapter.map_not_found("section", dto.restaurant)

        sections = response if isinstance(response, list) else response.get("data", [])

        if not sections:
            return adapter.map_empty("section", "list")

        return adapter.map_success(
            data=sections,
            entity_type="section",
            operation="list",
            count=len(sections),
        )

    except Exception as e:
        logger.error(
            "Failed to get restaurant sections",
            error=str(e),
            context="get_restaurant_sections",
        )
        return adapter.map_error(
            message=str(e),
            entity_type="section",
            operation="list",
        )
