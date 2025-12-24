"""Get restaurant sections tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.dtos.restaurants import RestaurantIdDto


@mcp.tool()
async def get_restaurant_sections(dto: RestaurantIdDto) -> str:
    """Get the floor plan sections of a restaurant.

    Args:
        dto: Restaurant ID parameter.

    Returns:
        List of sections (dining areas) with their table counts.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting restaurant sections",
        context="get_restaurant_sections",
        restaurant_id=dto.restaurant_id,
    )

    try:
        response = await http_client.get(
            f"/api/v1/restaurants/{dto.restaurant_id}/sections"
        )

        if response is None:
            return f"❌ Sections not found for restaurant '{dto.restaurant_id}'"

        sections = response if isinstance(response, list) else response.get("data", [])

        if not sections:
            return "🏠 No sections configured for this restaurant"

        result = "🏠 **Restaurant Sections:**\n\n"

        for section in sections:
            name = section.get("name", "Unnamed Section")
            section_id = section.get("id", "")[:8]
            description = section.get("description", "")
            tables = section.get("tables", [])
            table_count = len(tables) if isinstance(tables, list) else 0
            is_active = section.get("isActive", True)

            status = "✅" if is_active else "⏸️"
            result += f"{status} **{name}** (#{section_id})\n"
            if description:
                result += f"   {description}\n"
            result += f"   🪑 Tables: {table_count}\n\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to get restaurant sections",
            error=str(e),
            context="get_restaurant_sections",
        )
        return f"❌ Error getting restaurant sections: {str(e)}"
