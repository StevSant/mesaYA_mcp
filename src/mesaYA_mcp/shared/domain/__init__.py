"""Shared domain layer - Access control and authorization."""

from mesaYA_mcp.shared.domain.access_level import AccessLevel, has_access
from mesaYA_mcp.shared.domain.authorization_error import AuthorizationError
from mesaYA_mcp.shared.domain.tool_context import (
    ToolContext,
    get_current_context,
    set_current_context,
    reset_context,
)
from mesaYA_mcp.shared.domain.tool_permissions import (
    TOOL_PERMISSIONS,
    get_required_access_level,
)

__all__ = [
    # Access level
    "AccessLevel",
    "has_access",
    # Authorization error
    "AuthorizationError",
    # Tool context
    "ToolContext",
    "get_current_context",
    "set_current_context",
    "reset_context",
    # Tool permissions
    "TOOL_PERMISSIONS",
    "get_required_access_level",
]
