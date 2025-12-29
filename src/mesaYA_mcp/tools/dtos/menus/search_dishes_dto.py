"""Search dishes DTO."""

from pydantic import BaseModel, Field


class SearchDishesDto(BaseModel):
    """Input for searching dishes.

    The restaurant can be identified by its name instead of UUID.
    """

    query: str = Field(
        ..., min_length=1, description="Search term for dish name or description"
    )
    restaurant: str = Field(
        default="",
        description="Optional restaurant name or UUID to filter dishes (e.g., 'Pizza Palace').",
    )
    category: str = Field(
        default="", description="Category: appetizer, main, dessert, etc"
    )
    max_price: float = Field(default=0, ge=0, description="Maximum price filter")
    vegetarian: bool = Field(default=False, description="Only show vegetarian dishes")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum results")
