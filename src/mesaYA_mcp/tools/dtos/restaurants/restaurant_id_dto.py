"""Restaurant ID DTO."""

from pydantic import BaseModel, Field


class RestaurantIdDto(BaseModel):
    """Input requiring only a restaurant ID."""

    restaurant_id: str = Field(..., min_length=1, description="UUID of the restaurant")
