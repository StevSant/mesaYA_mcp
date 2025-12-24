"""DTOs package - Pydantic models for tool inputs.

Structure:
    dtos/
    ├── __init__.py
    ├── restaurants/         # 5 DTOs
    │   ├── search_restaurants_dto.py
    │   ├── nearby_restaurants_dto.py
    │   ├── restaurant_id_dto.py
    │   ├── restaurant_menu_dto.py
    │   └── section_id_dto.py
    ├── reservations/        # 7 DTOs
    │   ├── create_reservation_dto.py
    │   ├── reservation_id_dto.py
    │   ├── list_reservations_dto.py
    │   ├── restaurant_reservations_dto.py
    │   ├── update_reservation_status_dto.py
    │   ├── cancel_reservation_dto.py
    │   └── reservation_analytics_dto.py
    ├── menus/               # 5 DTOs
    │   ├── menu_id_dto.py
    │   ├── list_menus_dto.py
    │   ├── search_dishes_dto.py
    │   ├── dish_id_dto.py
    │   └── menu_analytics_dto.py
    └── users/               # 3 DTOs
        ├── user_id_dto.py
        ├── list_users_dto.py
        └── user_analytics_dto.py

Total: 20 DTOs (1 file = 1 DTO)
"""

from mesaYA_mcp.tools.dtos import restaurants
from mesaYA_mcp.tools.dtos import reservations
from mesaYA_mcp.tools.dtos import menus
from mesaYA_mcp.tools.dtos import users

__all__ = [
    "restaurants",
    "reservations",
    "menus",
    "users",
]
