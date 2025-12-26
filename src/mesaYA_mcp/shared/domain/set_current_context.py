"""Set current context function.

Sets the current tool execution context.
"""

from mesaYA_mcp.shared.domain.current_context import _current_context
from mesaYA_mcp.shared.domain.tool_context_model import ToolContext


def set_current_context(context: ToolContext) -> None:
    """Set the current tool execution context.

    Args:
        context: The ToolContext to set as current.
    """
    _current_context.set(context)
