"""List reservations tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools._formatters import format_reservation_summary
from mesaYA_mcp.tools.dtos.reservations import ListReservationsDto


@mcp.tool()
async def list_reservations(dto: ListReservationsDto) -> str:
    """List reservations with optional filters.

    Args:
        dto: Filter parameters including status, date_from, date_to, and limit.

    Returns:
        List of reservations matching the criteria.
    """
    logger = get_logger()
    http_client = get_http_client()

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
            return "❌ Error: Unable to retrieve reservations"

        if isinstance(response, dict):
            reservations = response.get("data", [])
            total = response.get("pagination", {}).get("totalItems", len(reservations))
        else:
            reservations = response
            total = len(reservations)

        if not reservations:
            return "🔍 No reservations found matching your criteria"

        result = f"📋 Found {total} reservations:\n\n"
        for r in reservations:
            result += format_reservation_summary(r) + "\n"

        return result.strip()

    except Exception as e:
        logger.error(
            "Failed to list reservations", error=str(e), context="list_reservations"
        )
        return f"❌ Error listing reservations: {str(e)}"
