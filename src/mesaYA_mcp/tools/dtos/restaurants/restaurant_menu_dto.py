"""Restaurant menu DTO."""

from pydantic import BaseModel, Field


class RestaurantMenuDto(BaseModel):
    """Input for getting restaurant menu."""

    restaurant_id: str = Field(..., min_length=1, description="UUID of the restaurant")
    active_only: bool = Field(default=True, description="Only return active menu items")
