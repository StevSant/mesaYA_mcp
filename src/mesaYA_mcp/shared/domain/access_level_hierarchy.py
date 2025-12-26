"""Access level hierarchy constant.

Defines the numeric hierarchy for permission inheritance.
"""

from mesaYA_mcp.shared.domain.access_level import AccessLevel


ACCESS_LEVEL_HIERARCHY: dict[AccessLevel, int] = {
    AccessLevel.GUEST: 0,
    AccessLevel.USER: 1,
    AccessLevel.OWNER: 2,
    AccessLevel.ADMIN: 3,
}
