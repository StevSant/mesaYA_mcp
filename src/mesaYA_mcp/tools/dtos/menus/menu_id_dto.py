"""Menu ID DTO."""

from pydantic import BaseModel, Field


class MenuIdDto(BaseModel):
    """Input requiring only a menu ID."""

    menu_id: str = Field(..., min_length=1, description="UUID of the menu")
