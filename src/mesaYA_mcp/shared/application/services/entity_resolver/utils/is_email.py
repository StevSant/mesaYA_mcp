"""Email validation utility."""

import re

# Email regex pattern
_EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def is_email(value: str) -> bool:
    """Check if a string is a valid email address.

    Args:
        value: The string to check.

    Returns:
        True if the string is a valid email, False otherwise.
    """
    return bool(_EMAIL_PATTERN.match(value))
