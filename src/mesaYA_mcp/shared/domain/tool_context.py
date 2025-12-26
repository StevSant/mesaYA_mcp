"""Tool execution context.

Provides a context object to pass access level and user info to tools.
Uses contextvars for thread-safe context propagation.
"""

from contextvars import ContextVar
from dataclasses import dataclass
from typing import Optional

from mesaYA_mcp.shared.domain.access_level import AccessLevel


@dataclass(frozen=True)
class ToolContext:
    """Context for tool execution.

    Contains user information needed for authorization and filtering.

    Attributes:
        access_level: User's access level for authorization.
        user_id: Optional user ID for user-specific queries.
        restaurant_id: Optional restaurant ID for owner-specific queries.
    """

    access_level: AccessLevel = AccessLevel.GUEST
    user_id: Optional[str] = None
    restaurant_id: Optional[str] = None


# Context variable for the current tool context
_current_context: ContextVar[ToolContext] = ContextVar(
    "tool_context",
    default=ToolContext(),
)


def get_current_context() -> ToolContext:
    """Get the current tool execution context.

    Returns:
        Current ToolContext, defaults to guest access if not set.
    """
    return _current_context.get()


def set_current_context(context: ToolContext) -> None:
    """Set the current tool execution context.

    Args:
        context: The ToolContext to set as current.
    """
    _current_context.set(context)


def reset_context() -> None:
    """Reset context to default (guest access)."""
    _current_context.set(ToolContext())
