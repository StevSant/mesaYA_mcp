"""MesaYA MCP Server - Model Context Protocol server for MesaYA platform.

This module provides the entry point for the MCP server, offering tools
for interacting with the MesaYA restaurant reservation platform.

Supports two transport modes:
- **stdio**: Standard input/output (default, for local tools)
- **sse**: Server-Sent Events via HTTP (for MCP Gateway)

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

import sys
from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_settings

# Import all tool modules to register them with the MCP server
# The @mcp.tool() decorators execute on import, registering each tool
import mesaYA_mcp.tools  # noqa: F401


def main() -> None:
    """Main entry point for the MCP server.

    Supports two transport modes:
    - stdio: Standard input/output (default)
    - sse: HTTP Server-Sent Events (MCP Gateway mode)

    Transport mode can be set via:
    - Environment variable: MCP_TRANSPORT=sse
    - Command line argument: --sse or --gateway
    """
    logger = get_logger()
    settings = get_settings()

    # Check for command line transport override
    transport = settings.mcp_transport
    if "--sse" in sys.argv or "--gateway" in sys.argv:
        transport = "sse"
    elif "--stdio" in sys.argv:
        transport = "stdio"

    logger.info(
        f"Starting mesaYA_mcp MCP server (transport: {transport})",
        context="main",
    )
    logger.info(
        "Registered tool categories: restaurants, reservations, menus, users",
        context="main",
    )

    try:
        if transport == "sse":
            # MCP Gateway mode - HTTP/SSE transport
            logger.info(
                f"MCP Gateway listening on http://{settings.mcp_gateway_host}:{settings.mcp_gateway_port}",
                context="main",
            )
            mcp.run(
                transport="sse",
                sse_path="/sse",
                message_path="/messages",
                host=settings.mcp_gateway_host,
                port=settings.mcp_gateway_port,
            )
        else:
            # Standard stdio transport
            mcp.run(transport="stdio")
    except Exception as e:
        logger.error("Server error", error=str(e), context="main")
        raise


if __name__ == "__main__":
    main()
