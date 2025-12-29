"""Get section tables tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.shared.application.services.entity_resolver import resolve_section_id
from mesaYA_mcp.tools.dtos.restaurants import SectionIdDto


@mcp.tool()
async def get_section_tables(dto: SectionIdDto) -> str:
    """Get all tables in a restaurant section.

    You can use either the section name or UUID to identify the section.
    When using a section name, also provide the restaurant name for context.
    Examples:
    - section: "Terraza", restaurant: "Pizza Palace"
    - section: "Salón Principal", restaurant: "La Trattoria"
    - section: "123e4567-e89b-12d3-a456-426614174000" (UUID also works without restaurant)

    Args:
        dto: Section identifier (name or UUID) and optional restaurant for context.

    Returns:
        List of tables with capacity and availability in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Getting section tables",
        context="get_section_tables",
        section=dto.section,
        restaurant=dto.restaurant,
    )

    try:
        # Resolve section by name or ID
        section_id = await resolve_section_id(dto.section, dto.restaurant)

        if section_id is None:
            if dto.restaurant:
                return adapter.map_not_found(
                    "section",
                    f"{dto.section} in restaurant {dto.restaurant}",
                )
            return adapter.map_not_found("section", dto.section)

        response = await http_client.get(f"/api/v1/sections/{section_id}/tables")

        if response is None:
            return adapter.map_not_found("table", dto.section)

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
