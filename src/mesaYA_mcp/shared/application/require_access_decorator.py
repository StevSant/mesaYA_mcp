"""Require access level decorator.

Decorator to enforce access level requirements on MCP tools.
"""

from functools import wraps
from typing import Callable, TypeVar, ParamSpec

from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.domain.has_access import has_access
from mesaYA_mcp.shared.domain.authorization_error import AuthorizationError
from mesaYA_mcp.shared.domain.get_current_context import get_current_context

P = ParamSpec("P")
R = TypeVar("R")


def require_access(level: AccessLevel) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator to require a minimum access level for a tool.

    Args:
        level: Minimum required access level.

    Returns:
        Decorator function that enforces access level check.

    Example:
        @mcp.tool()
        @require_access(AccessLevel.USER)
        async def create_reservation(dto: CreateReservationDto) -> str:
            ...
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            context = get_current_context()

            if not has_access(context.access_level, level):
                raise AuthorizationError(
                    tool_name=func.__name__,
                    user_level=context.access_level,
                    required_level=level,
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
