"""Section ID DTO."""

from pydantic import BaseModel, Field


class SectionIdDto(BaseModel):
    """Input requiring only a section ID."""

    section_id: str = Field(..., min_length=1, description="UUID of the section")
