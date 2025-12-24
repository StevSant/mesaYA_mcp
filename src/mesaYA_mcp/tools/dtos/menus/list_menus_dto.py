"""List menus DTO."""

from pydantic import BaseModel, Field


class ListMenusDto(BaseModel):
    """Input for listing menus."""

    restaurant_id: str = Field(
        default="", description="Optional restaurant UUID to filter by"
    )
    active_only: bool = Field(default=True, description="Only show active menus")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum results")
