"""Tool permissions constant.

Maps each MCP tool to its required minimum access level.
"""

from mesaYA_mcp.shared.domain.access_level import AccessLevel


TOOL_PERMISSIONS: dict[str, AccessLevel] = {
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
    "get_menu_dishes": AccessLevel.GUEST,
    "get_dish_details": AccessLevel.GUEST,
    "search_dishes": AccessLevel.GUEST,
    "get_menu_categories": AccessLevel.GUEST,
    "get_dishes_by_category": AccessLevel.GUEST,
    # ============================================
    # RESERVATION TOOLS - User level and above
    # ============================================
    "create_reservation": AccessLevel.USER,
    "get_reservation": AccessLevel.USER,
    "cancel_reservation": AccessLevel.USER,
    "get_user_reservations": AccessLevel.USER,
    "check_table_availability": AccessLevel.GUEST,
    "get_available_time_slots": AccessLevel.GUEST,
    # ============================================
    # RESTAURANT OWNER TOOLS - Owner level
    # ============================================
    "get_restaurant_reservations": AccessLevel.OWNER,
    "update_reservation_status": AccessLevel.OWNER,
    "get_restaurant_analytics": AccessLevel.OWNER,
    "get_reservation_statistics": AccessLevel.OWNER,
    # ============================================
    # USER MANAGEMENT TOOLS - Admin only
    # ============================================
    "list_users": AccessLevel.ADMIN,
    "get_user_by_email": AccessLevel.ADMIN,
    "get_user_info": AccessLevel.ADMIN,
}
