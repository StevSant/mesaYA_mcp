"""Authorization service module.

This module exports authorization functions for tool access control.
"""

from mesaYA_mcp.shared.application.services.authorization_service.authorize_tool_access import (
    authorize_tool_access,
)
from mesaYA_mcp.shared.application.services.authorization_service.can_access_tool import (
    can_access_tool,
)
from mesaYA_mcp.shared.application.services.authorization_service.get_allowed_tools import (
    get_allowed_tools,
)

__all__ = [
    "authorize_tool_access",
    "can_access_tool",
    "get_allowed_tools",
]
