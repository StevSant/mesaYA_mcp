"""List reservations tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.application.require_access_decorator import require_access
from mesaYA_mcp.mappers.adapters.toon_response_adapter import get_response_adapter
from mesaYA_mcp.tools.dtos.reservations import ListReservationsDto


@mcp.tool()
@require_access(AccessLevel.USER)
async def list_reservations(dto: ListReservationsDto) -> str:
    """List reservations with optional filters.

    Requires USER access level or higher.

    Args:
        dto: Filter parameters including status, date_from, date_to, and limit.

    Returns:
        List of reservations in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Listing reservations",
        context="list_reservations",
        status=dto.status,
        date_from=dto.date_from,
        date_to=dto.date_to,
    )

    try:
        params: dict = {"limit": dto.limit}

        if dto.status:
            params["status"] = dto.status
        if dto.date_from:
            params["dateFrom"] = dto.date_from
        if dto.date_to:
            params["dateTo"] = dto.date_to

        response = await http_client.get("/api/v1/reservations", params=params)

        if response is None:
            return adapter.map_error(
                message="Unable to retrieve reservations",
                entity_type="reservation",
                operation="list",
            )

        if isinstance(response, dict):
            reservations = response.get("data", [])
        else:
            reservations = response

        if not reservations:
            return adapter.map_empty("reservation", "list")

        return adapter.map_success(
            data=reservations,
            entity_type="reservation",
            operation="list",
            count=len(reservations),
        )

    except Exception as e:
        logger.error(
            "Failed to list reservations", error=str(e), context="list_reservations"
        )
        return adapter.map_error(
            message=str(e),
            entity_type="reservation",
            operation="list",
        )
