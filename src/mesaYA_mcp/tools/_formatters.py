"""Formatting helpers for MCP tool responses.

Contains all formatting functions used by tools to present data in a
user-friendly format with emojis and structured text.
"""

from typing import Any


# =============================================================================
# Restaurant Formatters
# =============================================================================


def format_restaurant(data: dict[str, Any]) -> str:
    """Format restaurant data into a readable string."""
    name = data.get("name", "Unknown")
    cuisine = data.get("cuisineType", data.get("cuisine_type", "N/A"))
    description = data.get("description", "")
    address = data.get("address", "N/A")
    city = data.get("city", "")
    phone = data.get("phone", "N/A")
    rating = data.get("rating", "N/A")
    is_active = data.get("active", True)

    location = f"{address}, {city}" if city else address
    status = "🟢 Open" if is_active else "🔴 Closed"

    base = (
        f"🍽️ **{name}** ({cuisine})\n"
        f"   📍 {location}\n"
        f"   📞 {phone}\n"
        f"   ⭐ Rating: {rating}\n"
        f"   {status}"
    )

    if description:
        desc_text = f"{description[:100]}..." if len(description) > 100 else description
        base += f"\n   📝 {desc_text}"

    return base


# =============================================================================
# Reservation Formatters
# =============================================================================


STATUS_EMOJI = {
    "pending": "🟡",
    "confirmed": "🟢",
    "cancelled": "🔴",
    "completed": "✅",
    "no_show": "⚫",
    "checked_in": "🔵",
}


def format_reservation(reservation: dict[str, Any]) -> str:
    """Format a reservation dict into a readable string."""
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
    """Format a brief reservation summary."""
    res_id = reservation.get("id", "N/A")[:8]
    status = reservation.get("status", "pending")
    date = reservation.get("date", reservation.get("reservationDate", "N/A"))
    party_size = reservation.get("partySize", reservation.get("guests", "N/A"))

    emoji = STATUS_EMOJI.get(status.lower(), "⚪")

    return f"{emoji} #{res_id} | {date} | {party_size} guests | {status.capitalize()}"


# =============================================================================
# Menu Formatters
# =============================================================================


def format_menu(menu: dict[str, Any]) -> str:
    """Format a menu dict into a readable string."""
    menu_id = menu.get("id", "N/A")
    name = menu.get("name", "Unnamed Menu")
    description = menu.get("description", "")
    price = menu.get("price", 0)
    is_active = menu.get("active", True)
    dishes = menu.get("dishes", [])

    status = "🟢" if is_active else "🔴"

    result = f"{status} **{name}**\n"
    result += f"   ID: {menu_id[:8]}...\n"
    result += f"   Price: ${price:.2f}\n"

    if description:
        result += f"   Description: {description}\n"

    if dishes:
        result += f"   Dishes: {len(dishes)} items\n"

    return result


def format_dish(dish: dict[str, Any]) -> str:
    """Format a dish dict into a readable string."""
    dish_id = dish.get("id", "N/A")
    name = dish.get("name", "Unknown Dish")
    description = dish.get("description", "")
    price = dish.get("price", 0)
    category = dish.get("category", "")
    is_available = dish.get("available", True)
    dietary = dish.get("dietaryInfo", [])
    allergens = dish.get("allergens", [])

    status = "🟢" if is_available else "🔴"

    result = f"{status} **{name}** - ${price:.2f}\n"
    result += f"   ID: {dish_id[:8]}...\n"

    if category:
        result += f"   Category: {category}\n"

    if description:
        desc_text = f"{description[:100]}..." if len(description) > 100 else description
        result += f"   Description: {desc_text}\n"

    if dietary:
        result += f"   Dietary: {', '.join(dietary)}\n"

    if allergens:
        result += f"   ⚠️ Allergens: {', '.join(allergens)}\n"

    return result


# =============================================================================
# User Formatters
# =============================================================================


ROLE_EMOJI = {
    "admin": "👑",
    "manager": "🏢",
    "staff": "👤",
    "customer": "🧑",
    "owner": "🔑",
}


def format_user(user: dict[str, Any]) -> str:
    """Format a user dict into a readable string."""
    user_id = user.get("id", "N/A")
    name = user.get("name", user.get("fullName", "Unknown"))
    email = user.get("email", "N/A")
    role = user.get("role", "customer")
    is_active = user.get("active", user.get("isActive", True))
    phone = user.get("phone", user.get("phoneNumber", ""))
    created_at = user.get("createdAt", "")

    emoji = ROLE_EMOJI.get(role.lower(), "👤")
    status = "🟢" if is_active else "🔴"

    result = f"{emoji} **{name}** {status}\n"
    result += f"   ID: {user_id[:8]}...\n"
    result += f"   Email: {email}\n"
    result += f"   Role: {role.capitalize()}\n"

    if phone:
        result += f"   Phone: {phone}\n"

    if created_at:
        result += f"   Joined: {created_at[:10]}\n"

    return result


def format_user_summary(user: dict[str, Any]) -> str:
    """Format a brief user summary."""
    name = user.get("name", user.get("fullName", "Unknown"))
    email = user.get("email", "N/A")
    role = user.get("role", "customer")
    is_active = user.get("active", user.get("isActive", True))

    emoji = ROLE_EMOJI.get(role.lower(), "👤")
    status = "🟢" if is_active else "🔴"

    return f"{emoji} {name} | {email} | {role.capitalize()} {status}"
