"""Has access function.

Checks if a user has sufficient access level.
"""

from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.domain.access_level_hierarchy import ACCESS_LEVEL_HIERARCHY


def has_access(user_level: AccessLevel, required_level: AccessLevel) -> bool:
    """Check if user has sufficient access level.

    Args:
        user_level: The user's current access level.
        required_level: The minimum required access level.

    Returns:
        True if user_level >= required_level in the hierarchy.
    """
    return ACCESS_LEVEL_HIERARCHY[user_level] >= ACCESS_LEVEL_HIERARCHY[required_level]
