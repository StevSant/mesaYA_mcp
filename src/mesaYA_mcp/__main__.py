
"""MesaYA MCP Server - Model Context Protocol server for MesaYA platform.

This module provides the entry point for the MCP server, offering tools
for interacting with the MesaYA restaurant reservation platform.
"""

from mcp.server.fastmcp import FastMCP

from mesaYA_mcp.shared.core import configure_dependencies, get_logger, get_settings

# Import feature tools
from mesaYA_mcp.features.restaurants.tools import (
    search_restaurants,
    get_restaurant_info,
)
from mesaYA_mcp.features.reservations.tools import (
    create_reservation,
    check_availability,
    get_reservation_status,
)


# Initialize settings and dependencies
settings = get_settings()
configure_dependencies(settings)

# Create MCP server instance
mcp = FastMCP(settings.app_name)


# ============================================================================
# Restaurant Tools
# ============================================================================


@mcp.tool()
async def mcp_search_restaurants(
    query: str = "",
    cuisine: str = "",
    location: str = "",
) -> str:
    """Search for restaurants by name, cuisine, or location."""
    return await search_restaurants(query, cuisine, location)


@mcp.tool()
async def mcp_get_restaurant_info(restaurant_id: str) -> str:
    """Get detailed information about a specific restaurant."""
    return await get_restaurant_info(restaurant_id)


# ============================================================================
# Reservation Tools
# ============================================================================


@mcp.tool()
async def mcp_create_reservation(
    restaurant_id: str,
    date: str,
    time: str,
    party_size: int = 2,
    customer_name: str = "",
    customer_email: str = "",
) -> str:
    """Create a new reservation at a restaurant."""
    return await create_reservation(
        restaurant_id, date, time, party_size, customer_name, customer_email
    )


@mcp.tool()
async def mcp_check_availability(
    restaurant_id: str,
    date: str,
    time: str = "",
    party_size: int = 2,
) -> str:
    """Check table availability at a restaurant for a specific date."""
    return await check_availability(restaurant_id, date, time, party_size)


@mcp.tool()
async def mcp_get_reservation_status(reservation_id: str) -> str:
    """Get the status of an existing reservation."""
    return await get_reservation_status(reservation_id)


def main() -> None:
    """Main entry point for the MCP server."""
    logger = get_logger()
    logger.info("Starting mesaYA_mcp MCP server...", context="main")

    try:
        mcp.run(transport="stdio")
    except Exception as e:
        logger.error("Server error", error=e, context="main")
        raise


if __name__ == "__main__":
    main()
