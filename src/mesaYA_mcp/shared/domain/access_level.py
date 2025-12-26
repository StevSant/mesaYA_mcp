"""AccessLevel enum - User access level definitions.

Defines access levels that control which tools users can invoke.
"""

from enum import StrEnum


class AccessLevel(StrEnum):
    """User access levels for tool authorization.

    Levels are hierarchical:
    - GUEST: Unauthenticated users, read-only public data
    - USER: Authenticated customers, can manage own reservations
    - OWNER: Restaurant owners, can view their restaurant data
    - ADMIN: System administrators, full access
    """

    GUEST = "guest"
    USER = "user"
    OWNER = "owner"
    ADMIN = "admin"
