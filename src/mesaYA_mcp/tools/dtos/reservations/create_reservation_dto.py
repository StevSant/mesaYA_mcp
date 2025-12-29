"""Create reservation DTO."""

from pydantic import BaseModel, Field


class CreateReservationDto(BaseModel):
    """Input for creating a reservation.

    Both restaurant and customer can be identified by user-friendly values:
    - restaurant: Use the restaurant name (e.g., "Pizza Palace")
    - customer: Use the customer's email (e.g., "john@example.com")
    """

    restaurant: str = Field(
        ...,
        min_length=1,
        description="Restaurant name or UUID. Use the restaurant name for easier lookup (e.g., 'Pizza Palace').",
    )
    customer_email: str = Field(
        ...,
        min_length=1,
        description="Customer email address (e.g., 'john@example.com'). The system will find the customer by email.",
    )
    date: str = Field(
        ..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Date (YYYY-MM-DD)"
    )
    time: str = Field(
        ..., pattern=r"^\d{2}:\d{2}$", description="Time (HH:MM, 24h format)"
    )
    party_size: int = Field(..., ge=1, le=20, description="Number of guests (1-20)")
    table_name: str = Field(
        default="",
        description="Optional table name or number (e.g., 'Mesa 5', 'VIP Table'). Leave empty for automatic assignment.",
    )
    section_name: str = Field(
        default="",
        description="Optional section/area name (e.g., 'Terraza', 'Salón Principal').",
    )
    notes: str = Field(
        default="", max_length=500, description="Special requests (max 500 chars)"
    )
