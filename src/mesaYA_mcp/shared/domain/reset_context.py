"""Reset context function.

Resets the tool context to default guest access.
"""

from mesaYA_mcp.shared.domain.current_context import _current_context
from mesaYA_mcp.shared.domain.tool_context_model import ToolContext


def reset_context() -> None:
    """Reset context to default (guest access)."""
    _current_context.set(ToolContext())
