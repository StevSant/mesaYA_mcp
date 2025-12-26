"""Get current context function.

Retrieves the current tool execution context.
"""

from mesaYA_mcp.shared.domain.current_context import _current_context
from mesaYA_mcp.shared.domain.tool_context_model import ToolContext


def get_current_context() -> ToolContext:
    """Get the current tool execution context.

    Returns:
        Current ToolContext, defaults to guest access if not set.
    """
    return _current_context.get()
