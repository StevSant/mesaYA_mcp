"""Authorize tool access function.

Validates user access to a tool, throwing an error if unauthorized.
"""

from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.domain.authorization_error import AuthorizationError
from mesaYA_mcp.shared.domain.get_required_access_level import (
    get_required_access_level,
)
from mesaYA_mcp.shared.domain.has_access import has_access


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
