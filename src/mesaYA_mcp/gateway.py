"""MCP Gateway - HTTP/SSE endpoint for MesaYA MCP Server.

This module provides the MCP Gateway entry point, exposing the MCP server
via HTTP with Server-Sent Events (SSE) transport.

Usage:
    # Via command line
    uv run gateway

    # Or with environment variables
    MCP_GATEWAY_HOST=0.0.0.0 MCP_GATEWAY_PORT=8000 uv run gateway

Endpoints:
    GET  /sse       - SSE endpoint for MCP communication
    POST /messages  - Message endpoint for MCP commands
    GET  /health    - Health check endpoint

The gateway allows external clients to connect to the MCP server over HTTP,
enabling integration with web applications and services that cannot use
stdio transport.
"""

import sys

# Force SSE transport when running as gateway
sys.argv.append("--sse")

from mesaYA_mcp.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()
