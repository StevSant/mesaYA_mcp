"""Get user tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.application.require_access_decorator import require_access
from mesaYA_mcp.src.mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import get_response_adapter
from mesaYA_mcp.tools.dtos.users import UserIdDto


@mcp.tool()
@require_access(AccessLevel.ADMIN)
async def get_user(dto: UserIdDto) -> str:
    """Get detailed information about a specific user.

    Requires ADMIN access level.

    Args:
        dto: User ID parameter.

    Returns:
        Complete user profile in TOON format.
    """
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info("Getting user details", context="get_user", user_id=dto.user_id)

    try:
        response = await http_client.get(f"/api/v1/users/{dto.user_id}")

        if response is None:
            return adapter.map_not_found("user", dto.user_id)

        return adapter.map_success(
            data=response,
            entity_type="user",
            operation="get",
        )

    except Exception as e:
        logger.error("Failed to get user", error=str(e), context="get_user")
        return adapter.map_error(
            message=str(e),
            entity_type="user",
            operation="get",
        )
