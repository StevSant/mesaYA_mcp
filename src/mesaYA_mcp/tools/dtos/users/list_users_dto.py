"""List users DTO."""

from pydantic import BaseModel, Field


class ListUsersDto(BaseModel):
    """Input for listing users with human-friendly filters.

    All filters are optional. Use specific fields like email or name
    instead of generic search when you know the exact value.
    """

    email: str = Field(
        default="", description="Filter by exact email address (preferred for lookup)"
    )
    name: str = Field(default="", description="Filter by user name (partial match)")
    role: str = Field(default="", description="Filter: ADMIN, OWNER, USER")
    active_only: bool = Field(default=True, description="Only show active users")
    search: str = Field(default="", description="General search term for name or email")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum results")
