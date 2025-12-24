"""Tool: get_restaurant_sections - Get restaurant floor plan sections."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client


@mcp.tool()
async def get_restaurant_sections(restaurant_id: str) -> str:
    """Get the sections/areas of a restaurant (floor plan).

    Args:
        restaurant_id: The UUID of the restaurant.

    Returns:
        List of restaurant sections with capacity information.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting restaurant sections",
        context="get_restaurant_sections",
        restaurant_id=restaurant_id,
    )

    try:
        if not restaurant_id:
            return "❌ Error: restaurant_id is required"

        response = await http_client.get(f"/api/v1/sections/restaurant/{restaurant_id}")

        if response is None:
            return f"❌ Could not retrieve sections for restaurant '{restaurant_id}'"

        sections = response.get("data", []) if isinstance(response, dict) else response

        if not sections:
            return "🏠 No sections configured for this restaurant"

        result = "🏠 **Restaurant Sections:**\n\n"
        for section in sections:
            name = section.get("name", "Unknown")
            description = section.get("description", "")
            capacity = section.get("capacity", "N/A")
            is_active = section.get("active", True)

            status = "🟢" if is_active else "🔴"
            result += f"{status} **{name}**\n"
            if description:
                result += f"   {description}\n"
            result += f"   Capacity: {capacity} people\n\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to get restaurant sections",
            error=str(e),
            context="get_restaurant_sections",
        )
        return f"❌ Error getting restaurant sections: {str(e)}"
