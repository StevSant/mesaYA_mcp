"""MCP Server instance - Single FastMCP server for the MesaYA platform.

This module creates the single FastMCP instance that all tool modules
will import and register their tools with using the @mcp.tool() decorator.
"""

from mcp.server.fastmcp import FastMCP

from mesaYA_mcp.shared.core import configure_dependencies, get_settings

# Initialize settings and dependencies
settings = get_settings()
configure_dependencies(settings)

# Create single MCP server instance - imported by all tool modules
mcp = FastMCP(settings.app_name)
