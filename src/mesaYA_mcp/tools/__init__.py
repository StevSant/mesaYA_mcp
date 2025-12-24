"""Tools package - MCP tool registrations organized by domain.

Each subpackage contains:
- __init__.py: Exports all tools from the module
- _format.py: Formatting helpers for data presentation
- Individual tool files: One file per tool function

Structure:
    tools/
    ├── __init__.py          # This file
    ├── restaurants/         # Restaurant-related tools (7)
    ├── reservations/        # Reservation management tools (10)
    ├── menus/               # Menu and dish tools (5)
    └── users/               # User management tools (3)

Total: 25 MCP tools
"""

# Import all tool modules to register them with the MCP server
# Each import triggers the @mcp.tool() decorators
from mesaYA_mcp.tools import restaurants  # noqa: F401
from mesaYA_mcp.tools import reservations  # noqa: F401
from mesaYA_mcp.tools import menus  # noqa: F401
from mesaYA_mcp.tools import users  # noqa: F401

__all__ = [
    "restaurants",
    "reservations",
    "menus",
    "users",
]
