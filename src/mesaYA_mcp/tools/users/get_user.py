"""Get user tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools._formatters import format_user
from mesaYA_mcp.tools.dtos.users import UserIdDto


@mcp.tool()
async def get_user(dto: UserIdDto) -> str:
    """Get detailed information about a specific user.

    Args:
        dto: User ID parameter.

    Returns:
        Complete user profile including role and preferences.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info("Getting user details", context="get_user", user_id=dto.user_id)

    try:
        response = await http_client.get(f"/api/v1/users/{dto.user_id}")

        if response is None:
            return f"❌ User with ID '{dto.user_id}' not found"

        return format_user(response)

    except Exception as e:
        logger.error("Failed to get user", error=str(e), context="get_user")
        return f"❌ Error getting user: {str(e)}"
