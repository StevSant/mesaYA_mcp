"""Tool: create_reservation - Create a new restaurant reservation."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.reservations._format import format_reservation


@mcp.tool()
async def create_reservation(
    restaurant_id: str,
    customer_id: str,
    date: str,
    time: str,
    party_size: int,
    table_id: str = "",
    notes: str = "",
) -> str:
    """Create a new reservation at a restaurant.

    Args:
        restaurant_id: UUID of the restaurant.
        customer_id: UUID of the customer making the reservation.
        date: Reservation date in YYYY-MM-DD format.
        time: Reservation time in HH:MM format (24h).
        party_size: Number of guests (1-20).
        table_id: Optional specific table UUID to reserve.
        notes: Special requests or notes for the reservation.

    Returns:
        Confirmation with reservation details or error message.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Creating reservation",
        context="create_reservation",
        restaurant_id=restaurant_id,
        date=date,
        time=time,
        party_size=party_size,
    )

    try:
        if not restaurant_id or not customer_id:
            return "❌ Error: restaurant_id and customer_id are required"

        if not date or not time:
            return "❌ Error: date and time are required"

        if party_size < 1 or party_size > 20:
            return "❌ Error: party_size must be between 1 and 20"

        payload = {
            "restaurantId": restaurant_id,
            "customerId": customer_id,
            "reservationDate": date,
            "reservationTime": time,
            "partySize": party_size,
        }

        if table_id:
            payload["tableId"] = table_id
        if notes:
            payload["specialRequests"] = notes

        response = await http_client.post("/api/v1/reservations", json=payload)

        if response is None:
            return "❌ Error: Unable to create reservation. The restaurant service is unavailable."

        result = "✅ Reservation created successfully!\n\n"
        result += format_reservation(response)

        return result

    except Exception as e:
        logger.error(
            "Failed to create reservation", error=str(e), context="create_reservation"
        )
        return f"❌ Error creating reservation: {str(e)}"
