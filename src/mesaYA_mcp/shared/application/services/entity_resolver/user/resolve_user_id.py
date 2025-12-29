"""Resolve user identifier to UUID."""

from typing import Optional

from mesaYA_mcp.shared.application.services.entity_resolver.utils import is_uuid
from mesaYA_mcp.shared.application.services.entity_resolver.user.resolve_user import (
    resolve_user,
)


async def resolve_user_id(identifier: str) -> Optional[str]:
    """Resolve a user identifier to their UUID.

    Args:
        identifier: User email, name, or UUID.

    Returns:
        User UUID if found, None otherwise.
    """
    if not identifier or not identifier.strip():
        return None

    identifier = identifier.strip()

    # If already a UUID, return as-is (but validate it exists)
    if is_uuid(identifier):
        user = await resolve_user(identifier)
        return identifier if user else None

    # Otherwise resolve by email or name
    user = await resolve_user(identifier)
    if user and isinstance(user, dict):
        return user.get("id")

    return None
