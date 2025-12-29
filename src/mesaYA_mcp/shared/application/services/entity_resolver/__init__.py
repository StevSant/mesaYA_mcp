"""Entity resolver services for resolving user-friendly names to IDs.

This module provides functions to resolve user-friendly identifiers
(like restaurant names, user emails) to internal UUIDs.
"""

from mesaYA_mcp.shared.application.services.entity_resolver.restaurant import (
    resolve_restaurant,
    resolve_restaurant_id,
)
from mesaYA_mcp.shared.application.services.entity_resolver.user import (
    resolve_user,
    resolve_user_id,
)
from mesaYA_mcp.shared.application.services.entity_resolver.section import (
    resolve_section,
    resolve_section_id,
)

__all__ = [
    "resolve_restaurant",
    "resolve_restaurant_id",
    "resolve_user",
    "resolve_user_id",
    "resolve_section",
    "resolve_section_id",
]
