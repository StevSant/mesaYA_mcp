"""Tool permissions module - Re-exports for backward compatibility.

This module re-exports TOOL_PERMISSIONS and get_required_access_level
from their individual modules for backward compatibility.
"""

from mesaYA_mcp.shared.domain.get_required_access_level import (
    get_required_access_level,
)
from mesaYA_mcp.shared.domain.tool_permissions_map import TOOL_PERMISSIONS

__all__ = [
    "TOOL_PERMISSIONS",
    "get_required_access_level",
]
