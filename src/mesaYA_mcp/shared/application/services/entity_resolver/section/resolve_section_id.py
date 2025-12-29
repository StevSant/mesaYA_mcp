"""Resolve section identifier to UUID."""

from typing import Optional

from mesaYA_mcp.shared.application.services.entity_resolver.utils import is_uuid
from mesaYA_mcp.shared.application.services.entity_resolver.section.resolve_section import (
    resolve_section,
)


async def resolve_section_id(
    identifier: str, restaurant_identifier: Optional[str] = None
) -> Optional[str]:
    """Resolve a section identifier to its UUID.

    Args:
        identifier: Section name or UUID.
        restaurant_identifier: Optional restaurant name or ID for context.

    Returns:
        Section UUID if found, None otherwise.
    """
    if not identifier or not identifier.strip():
        return None

    identifier = identifier.strip()

    # If already a UUID, return as-is (but validate it exists)
    if is_uuid(identifier):
        section = await resolve_section(identifier)
        return identifier if section else None

    # Otherwise resolve by name
    section = await resolve_section(identifier, restaurant_identifier)
    if section and isinstance(section, dict):
        return section.get("id")

    return None
