"""Restaurant identifier DTO."""

from pydantic import BaseModel, Field


class RestaurantIdDto(BaseModel):
    """Input requiring a restaurant identifier (name or UUID).

    The restaurant can be identified by either:
    - Its name (e.g., "Pizza Palace", "La Trattoria")
    - Its UUID (for backward compatibility)

    The system will automatically resolve names to IDs.
    """

    restaurant: str = Field(
        ...,
        min_length=1,
        description="Restaurant name or UUID. Use the restaurant name for easier lookup (e.g., 'Pizza Palace').",
    )
