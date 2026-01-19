"""Get my profile tool.

Allows authenticated users to retrieve their own profile information
from the current context without requiring admin privileges.
"""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger
from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.application.require_access_decorator import require_access
from mesaYA_mcp.shared.domain.get_current_context import get_current_context
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)


@mcp.tool()
@require_access(AccessLevel.USER)
async def get_my_profile() -> str:
    """Get the current user's profile info. Requires USER access. No args needed.

    Returns user_id and user_email from the current context.
    Use this to identify the logged-in user for reservations.

    Returns:
        User profile information in TOON format.
    """
    logger = get_logger()
    adapter = get_response_adapter()

    logger.info("Getting current user profile", context="get_my_profile")

    try:
        context = get_current_context()

        if context.user_id is None:
            return adapter.map_error(
                message="No user context available. User must be authenticated.",
                entity_type="user",
                operation="get_profile",
            )

        profile_data = {
            "user_id": context.user_id,
            "email": context.user_email,
            "access_level": context.access_level.value,
        }

        return adapter.map_success(
            data=profile_data,
            entity_type="user",
            operation="get_profile",
        )

    except Exception as e:
        logger.error(
            "Failed to get user profile", error=str(e), context="get_my_profile"
        )
        return adapter.map_error(
            message=str(e),
            entity_type="user",
            operation="get_profile",
        )
