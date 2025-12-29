"""Section identifier DTO."""

from pydantic import BaseModel, Field


class SectionIdDto(BaseModel):
    """Input requiring a section identifier (name or UUID).

    The section can be identified by either:
    - Its name (e.g., "Terraza", "Salón Principal") - requires restaurant context
    - Its UUID (for backward compatibility)

    When using a section name, provide the restaurant name as well.
    """

    section: str = Field(
        ...,
        min_length=1,
        description="Section name or UUID. Use the section name with restaurant context (e.g., 'Terraza').",
    )
    restaurant: str = Field(
        default="",
        description="Restaurant name or UUID (required when using section name instead of UUID).",
    )
