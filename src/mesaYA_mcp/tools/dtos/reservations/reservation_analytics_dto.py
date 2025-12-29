"""Reservation analytics DTO."""

from pydantic import BaseModel, Field


class ReservationAnalyticsDto(BaseModel):
    """Input for reservation analytics.

    The restaurant can be identified by its name instead of UUID.
    """

    restaurant: str = Field(
        default="",
        description="Optional restaurant name or UUID to filter analytics.",
    )
    date_from: str = Field(default="", description="Start date (YYYY-MM-DD)")
    date_to: str = Field(default="", description="End date (YYYY-MM-DD)")
