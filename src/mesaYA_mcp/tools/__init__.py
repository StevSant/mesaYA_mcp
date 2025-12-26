"""Tools package - MCP tool registrations organized by domain.

Each subpackage contains:
- __init__.py: Exports all tools from the module
- Individual tool files: One file per tool function

All tools return data in TOON format via the mappers/adapters layer.

Structure:
    tools/
    ├── __init__.py           # This file
    ├── dtos/                 # Pydantic DTOs for input validation
    ├── set_access_context.py # Context setter (call first!)
    ├── get_allowed_tools.py  # Authorization info tool
    ├── restaurants/          # Restaurant-related tools (8)
    ├── reservations/         # Reservation management tools (10)
    ├── menus/                # Menu and dish tools (5)
    └── users/                # User management tools (3)

Total: 28 MCP tools (1 file = 1 tool)
"""

# Import authorization tools first
from mesaYA_mcp.tools import set_access_context  # noqa: F401
from mesaYA_mcp.tools import get_allowed_tools  # noqa: F401

# Import all tool modules to register them with the MCP server
# Each import triggers the @mcp.tool() decorators
from mesaYA_mcp.tools import restaurants  # noqa: F401
from mesaYA_mcp.tools import reservations  # noqa: F401
from mesaYA_mcp.tools import menus  # noqa: F401
from mesaYA_mcp.tools import users  # noqa: F401

__all__ = [
    "set_access_context",
    "get_allowed_tools",
    "restaurants",
    "reservations",
    "menus",
    "users",
]
