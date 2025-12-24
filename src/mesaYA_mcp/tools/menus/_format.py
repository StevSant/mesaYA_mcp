"""Formatting helpers for menu and dish data."""

from typing import Any


def format_menu(menu: dict[str, Any]) -> str:
    """Format a menu dict into a readable string.

    Args:
        menu: Menu data from the API.

    Returns:
        Formatted menu string.
    """
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
    """Format a dish dict into a readable string.

    Args:
        dish: Dish data from the API.

    Returns:
        Formatted dish string.
    """
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
