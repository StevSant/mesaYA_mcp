"""Tool context module - Re-exports for backward compatibility.

This module re-exports ToolContext and context management functions
from their individual modules for backward compatibility.
"""

from mesaYA_mcp.shared.domain.get_current_context import get_current_context
from mesaYA_mcp.shared.domain.reset_context import reset_context
from mesaYA_mcp.shared.domain.set_current_context import set_current_context
from mesaYA_mcp.shared.domain.tool_context_model import ToolContext

__all__ = [
    "ToolContext",
    "get_current_context",
    "set_current_context",
    "reset_context",
]
