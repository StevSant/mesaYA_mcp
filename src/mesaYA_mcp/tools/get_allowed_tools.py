"""Get allowed tools for an access level.

MCP tool that returns the list of tools available for a given access level.
"""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.application.authorization_service import get_allowed_tools


@mcp.tool()
async def get_tools_for_access_level(access_level: str) -> str:
    """Get the list of MCP tools available for a given access level.

    Use this tool to understand what capabilities are available for the user's
    access level before attempting to call other tools.

    Args:
        access_level: User's access level ('guest', 'user', 'owner', 'admin').

    Returns:
        JSON list of allowed tool names for the access level.
    """
    try:
        level = AccessLevel(access_level.lower())
    except ValueError:
        return f"Invalid access level: {access_level}. Valid levels: guest, user, owner, admin"

    allowed = get_allowed_tools(level)
    return f"Allowed tools for '{access_level}': {', '.join(sorted(allowed))}"
