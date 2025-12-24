"""Tool: list_reservations - List reservations with filters."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.reservations._format import format_reservation_summary


@mcp.tool()
async def list_reservations(
    status: str = "",
    date_from: str = "",
    date_to: str = "",
    limit: int = 20,
) -> str:
    """List reservations with optional filters.

    Args:
        status: Filter by status: pending, confirmed, cancelled, completed, no_show.
        date_from: Start date filter in YYYY-MM-DD format.
        date_to: End date filter in YYYY-MM-DD format.
        limit: Maximum number of results (default 20, max 100).

    Returns:
        List of reservations matching the criteria.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Listing reservations",
        context="list_reservations",
        status=status,
        date_from=date_from,
        date_to=date_to,
    )

    try:
        params: dict = {"limit": min(limit, 100)}

        if status:
            params["status"] = status
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to

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
