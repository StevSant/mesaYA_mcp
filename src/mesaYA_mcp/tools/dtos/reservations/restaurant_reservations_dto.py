"""Restaurant reservations DTO."""

from pydantic import BaseModel, Field


class RestaurantReservationsDto(BaseModel):
    """Input for getting restaurant reservations.

    The restaurant can be identified by its name instead of UUID.
    """

    restaurant: str = Field(
        ...,
        min_length=1,
        description="Restaurant name or UUID. Use the restaurant name for easier lookup (e.g., 'Pizza Palace').",
    )
    date: str = Field(default="", description="Optional date filter (YYYY-MM-DD)")
    status: str = Field(default="", description="Optional status filter")
    limit: int = Field(default=50, ge=1, le=100, description="Maximum results")
