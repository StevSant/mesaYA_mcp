"""Restaurant menu DTO."""

from pydantic import BaseModel, Field


class RestaurantMenuDto(BaseModel):
    """Input for getting restaurant menu.

    The restaurant can be identified by either:
    - Its name (e.g., "Pizza Palace", "La Trattoria")
    - Its UUID (for backward compatibility)
    """

    restaurant: str = Field(
        ...,
        min_length=1,
        description="Restaurant name or UUID. Use the restaurant name for easier lookup (e.g., 'Pizza Palace').",
    )
    active_only: bool = Field(default=True, description="Only return active menu items")
