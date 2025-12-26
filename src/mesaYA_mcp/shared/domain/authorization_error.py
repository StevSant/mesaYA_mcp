"""Authorization error exception.

Custom exception for tool access denial.
"""

from mesaYA_mcp.shared.domain.access_level import AccessLevel


class AuthorizationError(Exception):
    """Raised when a user lacks permission to use a tool."""

    def __init__(
        self,
        tool_name: str,
        user_level: AccessLevel,
        required_level: AccessLevel,
    ) -> None:
        """Initialize authorization error.

        Args:
            tool_name: Name of the tool that was denied.
            user_level: User's current access level.
            required_level: Minimum required access level.
        """
        self.tool_name = tool_name
        self.user_level = user_level
        self.required_level = required_level
        super().__init__(
            f"Access denied: '{tool_name}' requires '{required_level}' level, "
            f"but user has '{user_level}' level."
        )
