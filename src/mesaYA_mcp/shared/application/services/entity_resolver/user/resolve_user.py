"""Resolve user by email, name, or ID."""

from typing import Optional

from mesaYA_mcp.shared.core import get_logger, get_http_client
from mesaYA_mcp.shared.application.services.entity_resolver.utils import (
    is_uuid,
    is_email,
)


async def resolve_user(identifier: str) -> Optional[dict]:
    """Resolve a user by email, name, or ID.

    If the identifier is a UUID, fetches the user by ID.
    If the identifier is an email, searches for the user by email.
    Otherwise, searches by name.

    Args:
        identifier: User email, name, or UUID.

    Returns:
        User data dict if found, None otherwise.
    """
    logger = get_logger()
    http_client = get_http_client()

    if not identifier or not identifier.strip():
        return None

    identifier = identifier.strip()

    try:
        if is_uuid(identifier):
            # Direct ID lookup
            logger.debug(
                "Resolving user by ID",
                context="user_resolver",
                identifier=identifier,
            )
            response = await http_client.get(f"/api/v1/users/{identifier}")
            return response if response else None
        elif is_email(identifier):
            # Email lookup
            logger.debug(
                "Resolving user by email",
                context="user_resolver",
                email=identifier,
            )
            response = await http_client.get(
                "/api/v1/users", params={"email": identifier, "limit": 1}
            )

            if response:
                if isinstance(response, dict):
                    users = response.get("data", response.get("results", []))
                    if users:
                        return users[0]
                elif isinstance(response, list) and response:
                    return response[0]

            return None
        else:
            # Try name search as fallback
            logger.debug(
                "Resolving user by name",
                context="user_resolver",
                name=identifier,
            )
            response = await http_client.get(
                "/api/v1/users", params={"name": identifier, "limit": 1}
            )

            if response:
                if isinstance(response, dict):
                    users = response.get("data", response.get("results", []))
                    if users:
                        return users[0]
                elif isinstance(response, list) and response:
                    return response[0]

            return None

    except Exception as e:
        logger.error(
            "Failed to resolve user",
            error=str(e),
            context="user_resolver",
            identifier=identifier,
        )
        return None
