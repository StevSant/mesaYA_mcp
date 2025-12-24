"""Get section tables tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.mappers.adapters.toon_response_adapter import get_response_adapter
from mesaYA_mcp.tools.dtos.restaurants import SectionIdDto


@mcp.tool()
async def get_section_tables(dto: SectionIdDto) -> str:
    """Get all tables in a restaurant section.

    Args:
        dto: Section ID parameter.

    Returns:
        List of tables with capacity and availability in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Getting section tables",
        context="get_section_tables",
        section_id=dto.section_id,
    )

    try:
        response = await http_client.get(f"/api/v1/sections/{dto.section_id}/tables")

        if response is None:
            return adapter.map_not_found("table", dto.section_id)

        tables = response if isinstance(response, list) else response.get("data", [])

        if not tables:
            return adapter.map_empty("table", "list")

        return adapter.map_success(
            data=tables,
            entity_type="table",
            operation="list",
            count=len(tables),
        )

    except Exception as e:
        logger.error(
            "Failed to get section tables",
            error=str(e),
            context="get_section_tables",
        )
        return adapter.map_error(
            message=str(e),
            entity_type="table",
            operation="list",
        )
