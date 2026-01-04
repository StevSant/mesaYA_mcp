"""Tool permissions constant.

Maps each MCP tool to its required minimum access level.
"""

from mesaYA_mcp.shared.domain.access_level import AccessLevel


TOOL_PERMISSIONS: dict[str, AccessLevel] = {
    # ============================================
    # SYSTEM TOOLS - Always accessible
    # ============================================
    "get_tools_for_access_level": AccessLevel.GUEST,
    "set_access_context": AccessLevel.GUEST,
    # ============================================
    # RESTAURANT TOOLS - Mostly public access
    # ============================================
    "search_restaurants": AccessLevel.GUEST,
    "get_restaurant_info": AccessLevel.GUEST,
    "get_restaurant_menu": AccessLevel.GUEST,
    "get_restaurant_schedule": AccessLevel.GUEST,
    "get_restaurant_sections": AccessLevel.GUEST,
    "get_section_tables": AccessLevel.GUEST,
    "get_nearby_restaurants": AccessLevel.GUEST,
    "get_restaurant_by_name": AccessLevel.GUEST,
    # ============================================
    # MENU TOOLS - Public read access
    # ============================================
    "get_menu": AccessLevel.GUEST,
    "list_menus": AccessLevel.GUEST,
    "get_dish": AccessLevel.GUEST,
    "search_dishes": AccessLevel.GUEST,
    # ============================================
    # RESERVATION TOOLS - User level and above
    # ============================================
    "create_reservation": AccessLevel.USER,
    "get_reservation": AccessLevel.USER,
    "cancel_reservation": AccessLevel.USER,
    "list_reservations": AccessLevel.USER,
    # ============================================
    # RESTAURANT OWNER TOOLS - Owner level
    # ============================================
    "get_restaurant_reservations": AccessLevel.OWNER,
    "update_reservation_status": AccessLevel.OWNER,
    "confirm_reservation": AccessLevel.OWNER,
    "check_in_reservation": AccessLevel.OWNER,
    "complete_reservation": AccessLevel.OWNER,
    "get_reservation_analytics": AccessLevel.OWNER,
    "get_menu_analytics": AccessLevel.OWNER,
    # ============================================
    # USER MANAGEMENT TOOLS - Admin only
    # ============================================
    "list_users": AccessLevel.ADMIN,
    "get_user_by_email": AccessLevel.ADMIN,
    "get_user": AccessLevel.ADMIN,
    "get_user_analytics": AccessLevel.ADMIN,
}
