"""Can access tool function.

Non-throwing check if user can access a tool.
"""

from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.domain.get_required_access_level import (
    get_required_access_level,
)
from mesaYA_mcp.shared.domain.has_access import has_access


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
