"""Formatting helpers for user data."""

from typing import Any


ROLE_EMOJI = {
    "admin": "👑",
    "manager": "🏢",
    "staff": "👤",
    "customer": "🧑",
    "owner": "🔑",
}


def format_user(user: dict[str, Any]) -> str:
    """Format a user dict into a readable string.

    Args:
        user: User data from the API.

    Returns:
        Formatted user string with role indicators.
    """
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
    """Format a brief user summary.

    Args:
        user: User data from the API.

    Returns:
        One-line summary of the user.
    """
    name = user.get("name", user.get("fullName", "Unknown"))
    email = user.get("email", "N/A")
    role = user.get("role", "customer")
    is_active = user.get("active", user.get("isActive", True))

    emoji = ROLE_EMOJI.get(role.lower(), "👤")
    status = "🟢" if is_active else "🔴"

    return f"{emoji} {name} | {email} | {role.capitalize()} {status}"
