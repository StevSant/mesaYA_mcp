"""Tool: get_user - Get user profile information."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.users._format import format_user


@mcp.tool()
async def get_user(user_id: str) -> str:
    """Get detailed information about a user.

    Args:
        user_id: The UUID of the user.

    Returns:
        User profile information including name, email, and role.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Getting user details",
        context="get_user",
        user_id=user_id,
    )

    try:
        if not user_id:
            return "❌ Error: user_id is required"

        response = await http_client.get(f"/api/v1/users/{user_id}")

        if response is None:
            return f"❌ User with ID '{user_id}' not found"

        return format_user(response)

    except Exception as e:
        logger.error("Failed to get user", error=str(e), context="get_user")
        return f"❌ Error getting user: {str(e)}"
