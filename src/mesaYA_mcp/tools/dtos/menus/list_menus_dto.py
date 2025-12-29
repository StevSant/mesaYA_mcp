"""List menus DTO."""

from pydantic import BaseModel, Field


class ListMenusDto(BaseModel):
    """Input for listing menus.

    The restaurant can be identified by its name instead of UUID.
    """

    restaurant: str = Field(
        default="",
        description="Optional restaurant name or UUID to filter menus (e.g., 'Pizza Palace').",
    )
    active_only: bool = Field(default=True, description="Only show active menus")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum results")
