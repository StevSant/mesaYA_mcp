"""ToolContext dataclass.

Context object for tool execution containing access information.
"""

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
