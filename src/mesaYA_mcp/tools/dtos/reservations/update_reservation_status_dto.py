"""Update reservation status DTO."""

from pydantic import BaseModel, Field


class UpdateReservationStatusDto(BaseModel):
    """Input for updating reservation status."""

    reservation_id: str = Field(
        ..., min_length=1, description="UUID of the reservation"
    )
    new_status: str = Field(
        ...,
        pattern=r"^(pending|confirmed|cancelled|completed|no_show|checked_in)$",
        description="New status: pending, confirmed, cancelled, completed, no_show, checked_in",
    )
    reason: str = Field(
        default="", max_length=200, description="Optional reason for change"
    )
