"""Helper function for formatting restaurant data."""

from typing import Any


def format_restaurant(data: dict[str, Any]) -> str:
    """Format restaurant data into a readable string.

    Args:
        data: Restaurant data from API.

    Returns:
        Formatted restaurant string.
    """
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
