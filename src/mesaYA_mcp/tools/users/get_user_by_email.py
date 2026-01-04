"""Get user by email tool."""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.application.require_access_decorator import require_access
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from mesaYA_mcp.tools.dtos.users import UserEmailDto


@mcp.tool()
@require_access(AccessLevel.ADMIN)
async def get_user_by_email(dto: UserEmailDto) -> str:
    """Get user by email. Requires ADMIN. Args: email. Returns: user profile."""
    logger = get_logger()
    http_client = get_http_client()
    adapter = get_response_adapter()

    logger.info(
        "Getting user details by email",
        context="get_user_by_email",
        email=dto.email,
    )

    try:
        response = await http_client.get(f"/api/v1/users/by-email/{dto.email}")

        if response is None:
            return adapter.map_not_found("user", dto.email)

        return adapter.map_success(
            data=response,
            entity_type="user",
            operation="get",
        )

    except Exception as e:
        logger.error(
            "Failed to get user by email",
            error=str(e),
            context="get_user_by_email",
        )
        return adapter.map_error(
            message=str(e),
            entity_type="user",
            operation="get",
        )
