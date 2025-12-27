"""Get allowed tools function.

Returns list of tools a user is allowed to access.
"""

from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.domain.has_access import has_access
from mesaYA_mcp.shared.domain.tool_permissions_map import TOOL_PERMISSIONS


def get_allowed_tools(user_level: AccessLevel) -> list[str]:
    """Get list of tools the user is allowed to access.

    Args:
        user_level: The user's current access level.

    Returns:
        List of tool names the user can access.
    """
    return [
        tool_name
        for tool_name, required_level in TOOL_PERMISSIONS.items()
        if has_access(user_level, required_level)
    ]
