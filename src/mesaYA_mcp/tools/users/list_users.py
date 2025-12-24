"""Tool: list_users - List users with filters."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.tools.users._format import format_user_summary


@mcp.tool()
async def list_users(
    role: str = "",
    active_only: bool = True,
    restaurant_id: str = "",
    limit: int = 20,
) -> str:
    """List users with optional filters.

    Args:
        role: Filter by role (admin, manager, staff, customer).
        active_only: If True, only show active users (default True).
        restaurant_id: Filter users by restaurant association.
        limit: Maximum number of results (default 20, max 100).

    Returns:
        List of users matching the criteria.
    """
    logger = get_logger()
    http_client = get_http_client()

    logger.info(
        "Listing users",
        context="list_users",
        role=role,
        active_only=active_only,
        restaurant_id=restaurant_id,
    )

    try:
        params: dict = {"limit": min(limit, 100)}

        if role:
            params["role"] = role
        if active_only:
            params["active"] = True
        if restaurant_id:
            params["restaurantId"] = restaurant_id

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
            return "🔍 No users found matching your criteria"

        result = f"👥 Found {total} users:\n\n"
        for user in users[:limit]:
            result += format_user_summary(user) + "\n"

        return result.strip()

    except Exception as e:
        logger.error("Failed to list users", error=str(e), context="list_users")
        return f"❌ Error listing users: {str(e)}"
