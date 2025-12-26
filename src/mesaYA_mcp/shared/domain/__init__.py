"""Shared domain layer - Access control and authorization."""

from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.domain.access_level_hierarchy import ACCESS_LEVEL_HIERARCHY
from mesaYA_mcp.shared.domain.authorization_error import AuthorizationError
from mesaYA_mcp.shared.domain.get_current_context import get_current_context
from mesaYA_mcp.shared.domain.get_required_access_level import (
    get_required_access_level,
)
from mesaYA_mcp.shared.domain.has_access import has_access
from mesaYA_mcp.shared.domain.reset_context import reset_context
from mesaYA_mcp.shared.domain.set_current_context import set_current_context
from mesaYA_mcp.shared.domain.tool_context_model import ToolContext
from mesaYA_mcp.shared.domain.tool_permissions_map import TOOL_PERMISSIONS

__all__ = [
    # Access level
    "AccessLevel",
    "ACCESS_LEVEL_HIERARCHY",
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
