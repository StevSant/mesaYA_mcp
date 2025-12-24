"""MesaYA MCP Server - Model Context Protocol server for MesaYA platform.

This module provides the entry point for the MCP server, offering tools
for interacting with the MesaYA restaurant reservation platform.

## Available Tools

### Restaurant Tools (7)
- search_restaurants: Search restaurants by name, cuisine, or location
- get_nearby_restaurants: Find restaurants near a location
- get_restaurant_info: Get detailed restaurant information
- get_restaurant_schedule: Get restaurant operating hours
- get_restaurant_menu: Get restaurant menu with dishes
- get_restaurant_sections: Get restaurant floor plan sections
- get_section_tables: Get tables in a section

### Reservation Tools (10)
- create_reservation: Create a new reservation
- get_reservation: Get reservation details
- list_reservations: List reservations with filters
- get_restaurant_reservations: Get all reservations for a restaurant
- update_reservation_status: Update reservation status
- confirm_reservation: Confirm a pending reservation
- cancel_reservation: Cancel a reservation
- check_in_reservation: Mark guest as checked in
- complete_reservation: Mark reservation as completed
- get_reservation_analytics: Get reservation statistics

### Menu Tools (5)
- get_menu: Get menu details
- list_menus: List restaurant menus
- search_dishes: Search dishes across restaurants
- get_dish: Get dish details
- get_menu_analytics: Get menu statistics

### User Tools (3)
- get_user: Get user profile
- list_users: List users with filters
- get_user_analytics: Get user statistics
"""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger

# Import all tool modules to register them with the MCP server
# The @mcp.tool() decorators execute on import, registering each tool
import mesaYA_mcp.tools  # noqa: F401


def main() -> None:
    """Main entry point for the MCP server."""
    logger = get_logger()
    logger.info("Starting mesaYA_mcp MCP server...", context="main")
    logger.info(
        "Registered tool categories: restaurants, reservations, menus, users",
        context="main",
    )

    try:
        mcp.run(transport="stdio")
    except Exception as e:
        logger.error("Server error", error=str(e), context="main")
        raise


if __name__ == "__main__":
    main()
