"""UUID validation utility."""

import re

# UUID regex pattern
_UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
)


def is_uuid(value: str) -> bool:
    """Check if a string is a valid UUID.

    Args:
        value: The string to check.

    Returns:
        True if the string is a valid UUID, False otherwise.
    """
    return bool(_UUID_PATTERN.match(value))
