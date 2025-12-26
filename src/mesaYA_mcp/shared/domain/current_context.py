"""Current context variable.

Thread-safe context variable for storing the current tool context.
"""

from contextvars import ContextVar

from mesaYA_mcp.shared.domain.tool_context_model import ToolContext


_current_context: ContextVar[ToolContext] = ContextVar(
    "tool_context",
    default=ToolContext(),
)
