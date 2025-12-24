"""Reservation analytics DTO."""

from pydantic import BaseModel, Field


class ReservationAnalyticsDto(BaseModel):
    """Input for reservation analytics."""

    restaurant_id: str = Field(
        default="", description="Optional restaurant UUID to filter by"
    )
    date_from: str = Field(default="", description="Start date (YYYY-MM-DD)")
    date_to: str = Field(default="", description="End date (YYYY-MM-DD)")
