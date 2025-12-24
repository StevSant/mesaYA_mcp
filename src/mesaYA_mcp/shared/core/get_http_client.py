"""HTTP Client provider - Dependency injection function for HTTP client.

Provides a FastAPI-style dependency injection function for getting the HTTP client instance.
"""

from functools import lru_cache

from mesaYA_mcp.shared.core.container import Container


@lru_cache(maxsize=1)
def get_http_client():
    """Get the HTTP client for backend API calls (FastAPI Depends-style).

    Lazily initializes and registers the HTTP client on first call.

    Returns:
        HttpClient: Configured HTTP client instance.

    Example:
        >>> client = get_http_client()
        >>> response = await client.get("/api/v1/restaurants")
    """
    from mesaYA_mcp.shared.infrastructure.adapters.http_client import (
        HttpClient,
    )

    if not Container.has("http_client"):
        client = HttpClient()
        Container.register("http_client", client)

    return Container.resolve("http_client")
