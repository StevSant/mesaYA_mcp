"""Search restaurants DTO."""

from pydantic import BaseModel, Field


class SearchRestaurantsDto(BaseModel):
    """Input for searching restaurants."""

    query: str = Field(
        default="", description="Search term for restaurant name or description"
    )
    cuisine_type: str = Field(
        default="", description="Filter by cuisine (italian, mexican, etc)"
    )
    city: str = Field(default="", description="Filter by city name")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum results (max 50)")
