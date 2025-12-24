"""Core module - configuration and dependency injection.

Provides centralized access to all core utilities:
- Settings: Application configuration class
- get_settings: Cached settings provider
- Container: Dependency injection container
- configure_dependencies: Application startup configuration
- get_logger: Logger provider function
- get_http_client: HTTP client provider function
"""

from mesaYA_mcp.shared.core.settings import Settings
from mesaYA_mcp.shared.core.get_settings import get_settings
from mesaYA_mcp.shared.core.container import Container
from mesaYA_mcp.shared.core.configure_dependencies import configure_dependencies
from mesaYA_mcp.shared.core.get_logger import get_logger
from mesaYA_mcp.shared.core.get_http_client import get_http_client

__all__ = [
    "Settings",
    "get_settings",
    "Container",
    "configure_dependencies",
    "get_logger",
    "get_http_client",
]
