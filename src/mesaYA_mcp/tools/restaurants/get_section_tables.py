"""Tool: get_section_tables - Get tables in a restaurant section."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client


@mcp.tool()
async def get_section_tables(section_id: str) -> str:
    """Get all tables in a specific restaurant section.

    Args:
        section_id: The UUID of the section.

    Returns:
        List of tables with capacity and availability status.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting section tables",
        context="get_section_tables",
        section_id=section_id,
    )

    try:
        if not section_id:
            return "❌ Error: section_id is required"

        response = await http_client.get(f"/api/v1/tables/section/{section_id}")

        if response is None:
            return f"❌ Could not retrieve tables for section '{section_id}'"

        tables = response.get("data", []) if isinstance(response, dict) else response

        if not tables:
            return "🪑 No tables configured in this section"

        result = "🪑 **Section Tables:**\n\n"
        for table in tables:
            name = table.get("name", table.get("tableNumber", "Unknown"))
            capacity = table.get("capacity", "N/A")
            status = table.get("status", "available")
            is_active = table.get("active", True)

            status_emoji = (
                "🟢"
                if status == "available"
                else "🔴" if status == "occupied" else "🟡"
            )
            active_indicator = "" if is_active else " (Inactive)"

            result += f"{status_emoji} Table **{name}**{active_indicator}\n"
            result += f"   Capacity: {capacity} people\n"
            result += f"   Status: {status.capitalize()}\n\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to get section tables", error=str(e), context="get_section_tables"
        )
        return f"❌ Error getting section tables: {str(e)}"
