"""Restaurant name DTO."""

from pydantic import BaseModel, Field


class RestaurantNameDto(BaseModel):
    """Input requiring only a restaurant name."""

    name: str = Field(
        ..., min_length=1, max_length=200, description="Name of the restaurant to find"
    )
