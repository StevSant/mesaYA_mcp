"""Authorization service module - Re-exports for backward compatibility.

This module re-exports authorization functions from their individual modules.
"""

from mesaYA_mcp.shared.application.authorize_tool_access import authorize_tool_access
from mesaYA_mcp.shared.application.can_access_tool import can_access_tool
from mesaYA_mcp.shared.application.get_allowed_tools import get_allowed_tools

__all__ = [
    "authorize_tool_access",
    "can_access_tool",
    "get_allowed_tools",
]
