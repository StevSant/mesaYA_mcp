"""Get required access level function.

Returns the required access level for a given tool.
"""

from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.domain.tool_permissions_map import TOOL_PERMISSIONS


def get_required_access_level(tool_name: str) -> AccessLevel:
    """Get the required access level for a tool.

    Args:
        tool_name: Name of the MCP tool.

    Returns:
        Required AccessLevel, defaults to ADMIN if tool not found.
    """
    return TOOL_PERMISSIONS.get(tool_name, AccessLevel.ADMIN)
