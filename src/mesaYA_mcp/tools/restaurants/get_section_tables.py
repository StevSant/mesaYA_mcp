"""Get section tables tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.dtos.restaurants import SectionIdDto


@mcp.tool()
async def get_section_tables(dto: SectionIdDto) -> str:
    """Get all tables in a restaurant section.

    Args:
        dto: Section ID parameter.

    Returns:
        List of tables with capacity and availability status.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting section tables",
        context="get_section_tables",
        section_id=dto.section_id,
    )

    try:
        response = await http_client.get(f"/api/v1/sections/{dto.section_id}/tables")

        if response is None:
            return f"❌ Tables not found for section '{dto.section_id}'"

        tables = response if isinstance(response, list) else response.get("data", [])

        if not tables:
            return "🪑 No tables configured in this section"

        result = "🪑 **Section Tables:**\n\n"

        for table in tables:
            table_num = table.get("tableNumber", "?")
            table_id = table.get("id", "")[:8]
            capacity = table.get("capacity", 0)
            min_cap = table.get("minCapacity", 1)
            is_available = table.get("isAvailable", True)
            is_active = table.get("isActive", True)

            if not is_active:
                status = "⏸️ Inactive"
            elif is_available:
                status = "✅ Available"
            else:
                status = "🔴 Occupied"

            result += f"   Table #{table_num} ({table_id})\n"
            result += f"   👥 Capacity: {min_cap}-{capacity} guests\n"
            result += f"   Status: {status}\n\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to get section tables",
            error=str(e),
            context="get_section_tables",
        )
        return f"❌ Error getting section tables: {str(e)}"
