"""List users tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.mappers.adapters.toon_response_adapter import get_response_adapter
from mesaYA_mcp.tools.dtos.users import ListUsersDto


@mcp.tool()
async def list_users(dto: ListUsersDto) -> str:
    """List users with optional filters.

    Args:
        dto: Filter parameters including role, active_only, search, and limit.

    Returns:
        List of users in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

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
            return adapter.map_error(
                message="Unable to retrieve users",
                entity_type="user",
                operation="list",
            )

        if isinstance(response, dict):
            users = response.get("data", [])
        else:
            users = response

        if not users:
            return adapter.map_empty("user", "list")

        return adapter.map_success(
            data=users,
            entity_type="user",
            operation="list",
            count=len(users),
        )

    except Exception as e:
        logger.error("Failed to list users", error=str(e), context="list_users")
        return adapter.map_error(
            message=str(e),
            entity_type="user",
            operation="list",
        )
