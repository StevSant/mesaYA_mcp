"""List users tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.application.require_access_decorator import require_access
from mesaYA_mcp.mappers.adapters.toon_response_adapter import get_response_adapter
from mesaYA_mcp.tools.dtos.users import ListUsersDto


@mcp.tool()
@require_access(AccessLevel.ADMIN)
async def list_users(dto: ListUsersDto) -> str:
    """List users with optional filters.

    Requires ADMIN access level.

    You can filter by specific fields like email, name, or role.
    Use the email filter when you know the exact email address.
    Use the name filter for partial name matching.

    Args:
        dto: Filter parameters including email, name, role, active_only, search, and limit.

    Returns:
        List of users in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Listing users",
        context="list_users",
        email=dto.email,
        name=dto.name,
        role=dto.role,
        active_only=dto.active_only,
    )

    try:
        params: dict = {"limit": dto.limit}
        if dto.email:
            params["email"] = dto.email
        if dto.name:
            params["name"] = dto.name
        if dto.role:
            params["role"] = dto.role
        if dto.active_only:
            params["active"] = True
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
            users = response.get("data", response.get("results", []))
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
