"""Nearby restaurants DTO."""

from pydantic import BaseModel, Field


class NearbyRestaurantsDto(BaseModel):
    """Input for finding nearby restaurants."""

    latitude: float = Field(..., ge=-90, le=90, description="Latitude (-90 to 90)")
    longitude: float = Field(
        ..., ge=-180, le=180, description="Longitude (-180 to 180)"
    )
    radius_km: float = Field(
        default=5.0, ge=0.1, le=50, description="Search radius in km (max 50)"
    )
    limit: int = Field(default=10, ge=1, le=50, description="Maximum results")
