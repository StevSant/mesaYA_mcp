"""Authorization service for MCP tool access control.

Provides functions to check and authorize tool access.
"""

from mesaYA_mcp.shared.domain.access_level import AccessLevel, has_access
from mesaYA_mcp.shared.domain.authorization_error import AuthorizationError
from mesaYA_mcp.shared.domain.tool_permissions import (
    TOOL_PERMISSIONS,
    get_required_access_level,
)


def authorize_tool_access(
    tool_name: str,
    user_level: AccessLevel,
) -> None:
    """Authorize access to a tool based on user's access level.

    Args:
        tool_name: The name of the MCP tool being accessed.
        user_level: The user's current access level.

    Raises:
        AuthorizationError: If user lacks required access level.
    """
    required_level = get_required_access_level(tool_name)

    if not has_access(user_level, required_level):
        raise AuthorizationError(tool_name, user_level, required_level)


def can_access_tool(tool_name: str, user_level: AccessLevel) -> bool:
    """Check if user can access a tool (non-throwing version).

    Args:
        tool_name: The name of the MCP tool.
        user_level: The user's current access level.

    Returns:
        True if user has permission, False otherwise.
    """
    required_level = get_required_access_level(tool_name)
    return has_access(user_level, required_level)


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
