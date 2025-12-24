"""Tools package - MCP tool registrations organized by domain.

Each subpackage contains:
- __init__.py: Exports all tools from the module
- Individual tool files: One file per tool function

Structure:
    tools/
    ├── __init__.py          # This file
    ├── _formatters.py       # Shared formatting helpers
    ├── restaurants/         # Restaurant-related tools (7)
    │   ├── search_restaurants.py
    │   ├── get_nearby_restaurants.py
    │   ├── get_restaurant_info.py
    │   ├── get_restaurant_schedule.py
    │   ├── get_restaurant_menu.py
    │   ├── get_restaurant_sections.py
    │   └── get_section_tables.py
    ├── reservations/        # Reservation management tools (10)
    │   ├── create_reservation.py
    │   ├── get_reservation.py
    │   ├── list_reservations.py
    │   ├── get_restaurant_reservations.py
    │   ├── update_reservation_status.py
    │   ├── confirm_reservation.py
    │   ├── cancel_reservation.py
    │   ├── check_in_reservation.py
    │   ├── complete_reservation.py
    │   └── get_reservation_analytics.py
    ├── menus/               # Menu and dish tools (5)
    │   ├── get_menu.py
    │   ├── list_menus.py
    │   ├── search_dishes.py
    │   ├── get_dish.py
    │   └── get_menu_analytics.py
    └── users/               # User management tools (3)
        ├── get_user.py
        ├── list_users.py
        └── get_user_analytics.py

Total: 25 MCP tools (1 file = 1 tool)
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
