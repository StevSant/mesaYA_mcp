"""Dish ID DTO."""

from pydantic import BaseModel, Field


class DishIdDto(BaseModel):
    """Input requiring only a dish ID."""

    dish_id: str = Field(..., min_length=1, description="UUID of the dish")
