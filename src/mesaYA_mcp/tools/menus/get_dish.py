"""Get dish tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.tools.dtos.menus import DishIdDto


@mcp.tool()
async def get_dish(dto: DishIdDto) -> str:
    """Get dish details. Args: dish_id. Returns: dish data."""
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info("Getting dish details", context="get_dish", dish_id=dto.dish_id)

    try:
        response = await http_client.get(f"/api/v1/dishes/{dto.dish_id}")

        if response is None:
            return adapter.map_not_found("dish", dto.dish_id)

        return adapter.map_success(
            data=response,
            entity_type="dish",
            operation="get",
        )

    except Exception as e:
        logger.error("Failed to get dish", error=str(e), context="get_dish")
        return adapter.map_error(
            message=str(e),
            entity_type="dish",
            operation="get",
        )
