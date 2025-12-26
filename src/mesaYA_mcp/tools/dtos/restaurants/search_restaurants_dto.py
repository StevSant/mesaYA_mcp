"""Search restaurants DTO."""

from pydantic import BaseModel, Field


class SearchRestaurantsDto(BaseModel):
    """Input for searching restaurants with human-friendly filters.

    All filters are optional. Use specific fields like name or city
    when you know the exact or partial value.
    """

    name: str = Field(
        default="",
        description="Filter by restaurant name (partial match, preferred for lookup)",
    )
    city: str = Field(default="", description="Filter by city/location name")
    cuisine_type: str = Field(
        default="", description="Filter by cuisine (italian, mexican, etc)"
    )
    query: str = Field(
        default="", description="General search term for name or description"
    )
    is_active: bool = Field(default=True, description="Only show active restaurants")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum results (max 50)")
