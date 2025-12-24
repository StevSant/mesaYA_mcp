"""List users tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools._formatters import format_user_summary
from mesaYA_mcp.tools.dtos.users import ListUsersDto


@mcp.tool()
async def list_users(dto: ListUsersDto) -> str:
    """List users with optional filters.

    Args:
        dto: Filter parameters including role, active_only, search, and limit.

    Returns:
        List of users matching the criteria.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Listing users",
        context="list_users",
        role=dto.role,
        active_only=dto.active_only,
    )

    try:
        params: dict = {"limit": dto.limit}
        if dto.role:
            params["role"] = dto.role
        if dto.active_only:
            params["isActive"] = True
        if dto.search:
            params["q"] = dto.search

        response = await http_client.get("/api/v1/users", params=params)

        if response is None:
            return "❌ Error: Unable to retrieve users"

        if isinstance(response, dict):
            users = response.get("data", [])
            total = response.get("pagination", {}).get("totalItems", len(users))
        else:
            users = response
            total = len(users)

        if not users:
            return "🔍 No users found"

        result = f"👥 Found {total} users:\n\n"

        for user in users:
            result += format_user_summary(user) + "\n"

        return result.strip()

    except Exception as e:
        logger.error("Failed to list users", error=str(e), context="list_users")
        return f"❌ Error listing users: {str(e)}"
