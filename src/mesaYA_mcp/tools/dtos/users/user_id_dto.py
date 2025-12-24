"""User ID DTO."""

from pydantic import BaseModel, Field


class UserIdDto(BaseModel):
    """Input requiring only a user ID."""

    user_id: str = Field(..., min_length=1, description="UUID of the user")
