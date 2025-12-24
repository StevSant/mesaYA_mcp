"""Cancel reservation DTO."""

from pydantic import BaseModel, Field


class CancelReservationDto(BaseModel):
    """Input for cancelling a reservation."""

    reservation_id: str = Field(
        ..., min_length=1, description="UUID of the reservation"
    )
    reason: str = Field(
        default="", max_length=200, description="Optional cancellation reason"
    )
