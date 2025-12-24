"""Reservation ID DTO."""

from pydantic import BaseModel, Field


class ReservationIdDto(BaseModel):
    """Input requiring only a reservation ID."""

    reservation_id: str = Field(
        ..., min_length=1, description="UUID of the reservation"
    )
