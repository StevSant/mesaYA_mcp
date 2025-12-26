"""Access level definitions for MCP tool authorization.

Defines access levels that control which tools users can invoke.
"""

from enum import StrEnum


class AccessLevel(StrEnum):
    """User access levels for tool authorization.

    Levels are hierarchical:
    - GUEST: Unauthenticated users, read-only public data
    - USER: Authenticated customers, can manage own reservations
    - OWNER: Restaurant owners, can view their restaurant data
    - ADMIN: System administrators, full access
    """

    GUEST = "guest"
    USER = "user"
    OWNER = "owner"
    ADMIN = "admin"


# Hierarchy for permission inheritance
ACCESS_LEVEL_HIERARCHY: dict[AccessLevel, int] = {
    AccessLevel.GUEST: 0,
    AccessLevel.USER: 1,
    AccessLevel.OWNER: 2,
    AccessLevel.ADMIN: 3,
}


def has_access(user_level: AccessLevel, required_level: AccessLevel) -> bool:
    """Check if user has sufficient access level.

    Args:
        user_level: The user's current access level.
        required_level: The minimum required access level.

    Returns:
        True if user_level >= required_level in the hierarchy.
    """
    return ACCESS_LEVEL_HIERARCHY[user_level] >= ACCESS_LEVEL_HIERARCHY[required_level]
