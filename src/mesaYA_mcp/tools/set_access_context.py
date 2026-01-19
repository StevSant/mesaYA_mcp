"""Context setter tool.

MCP tool that sets the execution context for subsequent tool calls.
Must be called before any access-restricted tools.
"""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.domain.tool_context_model import ToolContext
from mesaYA_mcp.shared.domain.set_current_context import set_current_context


@mcp.tool()
async def set_access_context(
    access_level: str,
    user_id: str | None = None,
    user_email: str | None = None,
    restaurant_id: str | None = None,
) -> str:
    """Set access context. CALL FIRST. Args: access_level (guest/user/owner/admin), user_id, user_email, restaurant_id."""
    try:
        level = AccessLevel(access_level.lower())
    except ValueError:
        return f"Error: Invalid access level '{access_level}'. Valid: guest, user, owner, admin"

    context = ToolContext(
        access_level=level,
        user_id=user_id,
        user_email=user_email,
        restaurant_id=restaurant_id,
    )
    set_current_context(context)

    return (
        f"Access context set: level={level.value}, "
        f"user_id={user_id or 'none'}, "
        f"user_email={user_email or 'none'}, "
        f"restaurant_id={restaurant_id or 'none'}"
    )
