"""HTTP Client Adapter - REST API client for MesaYA backend.

This adapter provides HTTP communication with the NestJS REST API backend,
handling all network operations for the MCP tools.
"""

import json
from typing import Any

import httpx

from mesaYA_mcp.shared.core import get_logger, get_settings


class HttpClient:
    """HTTP client for backend API communication.

    Provides async HTTP methods with built-in error handling,
    logging, and configuration from settings.

    Attributes:
        _base_url: Base URL of the REST API.
        _timeout: Request timeout in seconds.
        _headers: Default headers for all requests.
    """

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float | None = None,
        api_key: str | None = None,
    ) -> None:
        """Initialize the HTTP client.

        Args:
            base_url: Base URL of the REST API. Defaults to settings.
            timeout: Request timeout in seconds. Defaults to settings.
            api_key: Optional API key for authentication.
        """
        settings = get_settings()
        self._base_url = (base_url or settings.backend_api_url).rstrip("/")
        self._timeout = timeout or settings.backend_api_timeout
        self._headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if api_key or settings.backend_api_key:
            self._headers["X-API-Key"] = api_key or settings.backend_api_key

    def _get_client(self) -> httpx.AsyncClient:
        """Create a new async HTTP client instance.

        Returns:
            Configured AsyncClient instance.
        """
        return httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._timeout,
            headers=self._headers,
        )

    async def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[Any] | None:
        """Perform GET request.

        Args:
            path: API endpoint path.
            params: Optional query parameters.

        Returns:
            JSON response data or None on error.
        """
        logger = get_logger()
        logger.debug(
            "HTTP GET request",
            context="HttpClient.get",
            path=path,
            params=params,
        )

        async with self._get_client() as client:
            try:
                response = await client.get(path, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(
                    "HTTP status error",
                    error=str(e),
                    context="HttpClient.get",
                    path=path,
                    status_code=e.response.status_code,
                )
                return None
            except httpx.RequestError as e:
                logger.error(
                    "HTTP request failed",
                    error=str(e),
                    context="HttpClient.get",
                    path=path,
                )
                return None
            except json.JSONDecodeError as e:
                logger.error(
                    "JSON decode error",
                    error=str(e),
                    context="HttpClient.get",
                    path=path,
                )
                return None

    async def post(
        self,
        path: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Perform POST request.

        Args:
            path: API endpoint path.
            data: Request body data.
            params: Optional query parameters.

        Returns:
            JSON response data or None on error.
        """
        logger = get_logger()
        logger.debug(
            "HTTP POST request",
            context="HttpClient.post",
            path=path,
        )

        async with self._get_client() as client:
            try:
                response = await client.post(path, json=data, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(
                    "HTTP status error",
                    error=str(e),
                    context="HttpClient.post",
                    path=path,
                    status_code=e.response.status_code,
                )
                return None
            except httpx.RequestError as e:
                logger.error(
                    "HTTP request failed",
                    error=str(e),
                    context="HttpClient.post",
                    path=path,
                )
                return None

    async def patch(
        self,
        path: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Perform PATCH request.

        Args:
            path: API endpoint path.
            data: Request body data.

        Returns:
            JSON response data or None on error.
        """
        logger = get_logger()
        logger.debug(
            "HTTP PATCH request",
            context="HttpClient.patch",
            path=path,
        )

        async with self._get_client() as client:
            try:
                response = await client.patch(path, json=data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(
                    "HTTP status error",
                    error=str(e),
                    context="HttpClient.patch",
                    path=path,
                    status_code=e.response.status_code,
                )
                return None
            except httpx.RequestError as e:
                logger.error(
                    "HTTP request failed",
                    error=str(e),
                    context="HttpClient.patch",
                    path=path,
                )
                return None

    async def delete(self, path: str) -> bool:
        """Perform DELETE request.

        Args:
            path: API endpoint path.

        Returns:
            True if successful, False otherwise.
        """
        logger = get_logger()
        logger.debug(
            "HTTP DELETE request",
            context="HttpClient.delete",
            path=path,
        )

        async with self._get_client() as client:
            try:
                response = await client.delete(path)
                response.raise_for_status()
                return True
            except httpx.HTTPStatusError as e:
                logger.error(
                    "HTTP status error",
                    error=str(e),
                    context="HttpClient.delete",
                    path=path,
                    status_code=e.response.status_code,
                )
                return False
            except httpx.RequestError as e:
                logger.error(
                    "HTTP request failed",
                    error=str(e),
                    context="HttpClient.delete",
                    path=path,
                )
                return False
