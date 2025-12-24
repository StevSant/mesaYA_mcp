"""Create reservation DTO."""

from pydantic import BaseModel, Field


class CreateReservationDto(BaseModel):
    """Input for creating a reservation."""

    restaurant_id: str = Field(..., min_length=1, description="UUID of the restaurant")
    customer_id: str = Field(..., min_length=1, description="UUID of the customer")
    date: str = Field(
        ..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Date (YYYY-MM-DD)"
    )
    time: str = Field(
        ..., pattern=r"^\d{2}:\d{2}$", description="Time (HH:MM, 24h format)"
    )
    party_size: int = Field(..., ge=1, le=20, description="Number of guests (1-20)")
    table_id: str = Field(default="", description="Optional specific table UUID")
    notes: str = Field(
        default="", max_length=500, description="Special requests (max 500 chars)"
    )
