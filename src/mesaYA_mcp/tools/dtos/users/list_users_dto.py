"""List users DTO."""

from pydantic import BaseModel, Field


class ListUsersDto(BaseModel):
    """Input for listing users."""

    role: str = Field(default="", description="Filter: admin, manager, staff, customer")
    active_only: bool = Field(default=True, description="Only show active users")
    search: str = Field(default="", description="Search term for name or email")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum results")
