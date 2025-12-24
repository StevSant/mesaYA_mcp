"""Create reservation tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools._formatters import format_reservation
from mesaYA_mcp.tools.dtos.reservations import CreateReservationDto


@mcp.tool()
async def create_reservation(dto: CreateReservationDto) -> str:
    """Create a new reservation at a restaurant.

    Args:
        dto: Reservation details including restaurant_id, customer_id, date, time, party_size.

    Returns:
        Confirmation with reservation details or error message.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Creating reservation",
        context="create_reservation",
        restaurant_id=dto.restaurant_id,
        date=dto.date,
        time=dto.time,
        party_size=dto.party_size,
    )

    try:
        payload = {
            "restaurantId": dto.restaurant_id,
            "customerId": dto.customer_id,
            "reservationDate": dto.date,
            "reservationTime": dto.time,
            "partySize": dto.party_size,
        }

        if dto.table_id:
            payload["tableId"] = dto.table_id
        if dto.notes:
            payload["specialRequests"] = dto.notes

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
