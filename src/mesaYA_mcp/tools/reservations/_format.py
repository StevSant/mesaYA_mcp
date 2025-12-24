"""Formatting helpers for reservation data."""

from typing import Any


STATUS_EMOJI = {
    "pending": "🟡",
    "confirmed": "🟢",
    "cancelled": "🔴",
    "completed": "✅",
    "no_show": "⚫",
    "checked_in": "🔵",
}


def format_reservation(reservation: dict[str, Any]) -> str:
    """Format a reservation dict into a readable string.

    Args:
        reservation: Reservation data from the API.

    Returns:
        Formatted reservation string with emoji indicators.
    """
    res_id = reservation.get("id", "N/A")
    status = reservation.get("status", "pending")
    date = reservation.get("date", reservation.get("reservationDate", "N/A"))
    time = reservation.get("time", reservation.get("reservationTime", "N/A"))
    party_size = reservation.get("partySize", reservation.get("guests", "N/A"))
    customer = reservation.get(
        "customerName", reservation.get("customer", {}).get("name", "N/A")
    )
    restaurant = reservation.get(
        "restaurantName", reservation.get("restaurant", {}).get("name", "")
    )
    table = reservation.get(
        "tableName", reservation.get("table", {}).get("name", "N/A")
    )
    notes = reservation.get("notes", reservation.get("specialRequests", ""))

    emoji = STATUS_EMOJI.get(status.lower(), "⚪")

    result = f"{emoji} **Reservation #{res_id[:8] if len(res_id) > 8 else res_id}**\n"
    result += f"   Status: {status.capitalize()}\n"
    result += f"   Date: {date} at {time}\n"
    result += f"   Party Size: {party_size} people\n"
    result += f"   Customer: {customer}\n"

    if restaurant:
        result += f"   Restaurant: {restaurant}\n"
    result += f"   Table: {table}\n"

    if notes:
        result += f"   Notes: {notes}\n"

    return result


def format_reservation_summary(reservation: dict[str, Any]) -> str:
    """Format a brief reservation summary.

    Args:
        reservation: Reservation data from the API.

    Returns:
        One-line summary of the reservation.
    """
    res_id = reservation.get("id", "N/A")[:8]
    status = reservation.get("status", "pending")
    date = reservation.get("date", reservation.get("reservationDate", "N/A"))
    party_size = reservation.get("partySize", reservation.get("guests", "N/A"))

    emoji = STATUS_EMOJI.get(status.lower(), "⚪")

    return f"{emoji} #{res_id} | {date} | {party_size} guests | {status.capitalize()}"
