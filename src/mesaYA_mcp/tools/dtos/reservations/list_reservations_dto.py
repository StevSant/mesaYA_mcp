"""List reservations DTO."""

from pydantic import BaseModel, Field


class ListReservationsDto(BaseModel):
    """Input for listing reservations."""

    status: str = Field(
        default="",
        description="Filter: pending, confirmed, cancelled, completed, no_show",
    )
    date_from: str = Field(default="", description="Start date (YYYY-MM-DD)")
    date_to: str = Field(default="", description="End date (YYYY-MM-DD)")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum results")
