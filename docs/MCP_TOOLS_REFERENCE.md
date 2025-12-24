# MCP Tools Reference - MesaYA

Este documento describe todas las herramientas MCP implementadas en el servidor `mesaYA_mcp` que exponen la funcionalidad del sistema de reservas de restaurantes.

## Arquitectura Modular

```
mesaYA_mcp/src/mesaYA_mcp/
├── __main__.py          # Entry point - just imports and runs
├── server.py            # Single FastMCP instance
├── shared/              # Shared utilities (config, logging, http_client)
└── tools/               # All MCP tools organized by domain
    ├── __init__.py      # Imports all submodules
    ├── restaurants/
    │   ├── __init__.py
    │   ├── helpers.py   # Formatting functions
    │   ├── search.py    # search_restaurants, get_nearby_restaurants
    │   ├── info.py      # get_restaurant_info, schedule, menu
    │   └── sections.py  # get_restaurant_sections, get_section_tables
    ├── reservations/
    │   ├── __init__.py
    │   ├── helpers.py   # Formatting functions
    │   ├── crud.py      # create, get, list reservations
    │   ├── status.py    # confirm, cancel, check_in, complete
    │   └── analytics.py # get_reservation_analytics
    ├── menus/
    │   ├── __init__.py
    │   ├── helpers.py   # Formatting functions
    │   ├── menus.py     # get_menu, list_menus
    │   ├── dishes.py    # search_dishes, get_dish
    │   └── analytics.py # get_menu_analytics
    └── users/
        ├── __init__.py
        └── users.py     # get_user, list_users, get_user_analytics
```

## Cómo Funciona

1. **`server.py`** crea una única instancia de `FastMCP`
2. Cada módulo en **`tools/`** importa `mcp` desde `server.py`
3. Los decoradores `@mcp.tool()` registran las herramientas automáticamente
4. **`__main__.py`** solo importa `tools` para activar el registro

## Configuración

Variables de entorno requeridas:

```bash
# Host del backend NestJS
BACKEND_API_HOST=localhost

# Puerto del backend NestJS
BACKEND_API_PORT=3000

# Nivel de logging (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Timeout para peticiones HTTP (segundos)
BACKEND_API_TIMEOUT=30.0
```

## Herramientas Disponibles

### 🍽️ Restaurantes (7 herramientas)

#### `search_restaurants`

Busca restaurantes por diferentes criterios.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `query` | string | No | Término de búsqueda |
| `cuisine` | string | No | Tipo de cocina (italiana, mexicana, etc.) |
| `location` | string | No | Ciudad o ubicación |
| `limit` | int | No | Número máximo de resultados (default: 10) |

**Ejemplo de uso:**

```json
{
  "tool": "search_restaurants",
  "arguments": {
    "query": "pizza",
    "cuisine": "italiana",
    "location": "Manta",
    "limit": 5
  }
}
```

#### `get_restaurant_info`

Obtiene información detallada de un restaurante.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant_id` | string | Sí | UUID del restaurante |

#### `get_nearby_restaurants`

Busca restaurantes cercanos a una ubicación geográfica.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `latitude` | float | Sí | Latitud (-90 a 90) |
| `longitude` | float | Sí | Longitud (-180 a 180) |
| `radius_km` | float | No | Radio de búsqueda en km (default: 5.0) |
| `limit` | int | No | Máximo de resultados (default: 10) |

#### `get_restaurant_schedule`

Obtiene los horarios disponibles de un restaurante.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant_id` | string | Sí | UUID del restaurante |

#### `get_restaurant_menu`

Obtiene el menú completo de un restaurante.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant_id` | string | Sí | UUID del restaurante |

#### `get_restaurant_sections`

Obtiene las secciones/áreas de un restaurante.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant_id` | string | Sí | UUID del restaurante |

#### `get_section_tables`

Obtiene las mesas disponibles en una sección.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `section_id` | string | Sí | UUID de la sección |

---

### 📅 Reservaciones (10 herramientas)

#### `create_reservation`

Crea una nueva reservación.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `user_id` | string | Sí | UUID del usuario |
| `restaurant_id` | string | Sí | UUID del restaurante |
| `date` | string | Sí | Fecha (YYYY-MM-DD) |
| `time` | string | Sí | Hora (HH:MM) |
| `party_size` | int | Sí | Número de comensales |
| `table_id` | string | No | UUID de mesa específica |
| `notes` | string | No | Notas adicionales |

**Ejemplo de uso:**

```json
{
  "tool": "create_reservation",
  "arguments": {
    "user_id": "uuid-usuario",
    "restaurant_id": "uuid-restaurante",
    "date": "2025-01-20",
    "time": "19:30",
    "party_size": 4,
    "notes": "Mesa cerca de la ventana"
  }
}
```

#### `get_reservation`

Obtiene detalles de una reservación específica.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `reservation_id` | string | Sí | UUID de la reservación |

#### `list_reservations`

Lista reservaciones con filtros opcionales.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `user_id` | string | No | Filtrar por usuario |
| `status` | string | No | Estado (pending, confirmed, cancelled, completed, no_show) |
| `from_date` | string | No | Fecha inicial (YYYY-MM-DD) |
| `to_date` | string | No | Fecha final (YYYY-MM-DD) |
| `limit` | int | No | Máximo de resultados (default: 20) |

#### `get_restaurant_reservations`

Obtiene todas las reservaciones de un restaurante.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant_id` | string | Sí | UUID del restaurante |
| `date` | string | No | Filtrar por fecha |
| `status` | string | No | Filtrar por estado |

#### `update_reservation_status`

Actualiza el estado de una reservación.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `reservation_id` | string | Sí | UUID de la reservación |
| `status` | string | Sí | Nuevo estado |

**Estados válidos:**

- `pending` - Pendiente de confirmación
- `confirmed` - Confirmada
- `cancelled` - Cancelada
- `checked_in` - Cliente llegó
- `completed` - Completada
- `no_show` - Cliente no se presentó

#### `cancel_reservation`

Cancela una reservación (atajo para update_reservation_status con status=cancelled).

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `reservation_id` | string | Sí | UUID de la reservación |

#### `confirm_reservation`

Confirma una reservación pendiente.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `reservation_id` | string | Sí | UUID de la reservación |

#### `check_in_reservation`

Registra la llegada del cliente (check-in).

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `reservation_id` | string | Sí | UUID de la reservación |

#### `complete_reservation`

Marca una reservación como completada.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `reservation_id` | string | Sí | UUID de la reservación |

#### `get_reservation_analytics`

Obtiene estadísticas de reservaciones.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant_id` | string | No | Filtrar por restaurante |
| `from_date` | string | No | Fecha inicial |
| `to_date` | string | No | Fecha final |

---

### 🍕 Menús y Platillos (5 herramientas)

#### `get_menu`

Obtiene un menú específico por ID.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `menu_id` | string | Sí | UUID del menú |

#### `list_menus`

Lista todos los menús de un restaurante.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant_id` | string | Sí | UUID del restaurante |
| `limit` | int | No | Máximo de resultados (default: 20) |

#### `search_dishes`

Busca platillos con filtros.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `query` | string | No | Término de búsqueda |
| `restaurant_id` | string | No | Filtrar por restaurante |
| `min_price` | float | No | Precio mínimo |
| `max_price` | float | No | Precio máximo |
| `limit` | int | No | Máximo de resultados (default: 20) |

#### `get_dish`

Obtiene detalles de un platillo específico.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `dish_id` | string | Sí | UUID del platillo |

#### `get_menu_analytics`

Obtiene estadísticas de menús.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant_id` | string | No | Filtrar por restaurante |
| `from_date` | string | No | Fecha inicial |
| `to_date` | string | No | Fecha final |

---

### 👤 Usuarios (3 herramientas)

#### `get_user`

Obtiene información de un usuario.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `user_id` | string | Sí | UUID del usuario |

#### `list_users`

Lista usuarios con filtros.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `query` | string | No | Buscar por nombre o email |
| `role` | string | No | Filtrar por rol (admin, owner, staff, customer) |
| `limit` | int | No | Máximo de resultados (default: 20) |

#### `get_user_analytics`

Obtiene estadísticas de usuarios.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `role` | string | No | Filtrar por rol |
| `from_date` | string | No | Fecha inicial |
| `to_date` | string | No | Fecha final |

---

## Integración con Agentes

### Opción 1: Cliente MCP (Recomendado para nuevos desarrollos)

```python
from mcp import ClientSession
from mcp.client.stdio import stdio_client

async def call_mcp_tool(tool_name: str, arguments: dict):
    """Llama a una herramienta MCP."""
    async with stdio_client("uv", ["run", "mcp"]) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            return result.content
```

### Opción 2: Adaptador REST (Para compatibilidad existente)

El servicio de chatbot ya implementa `RestApiAdapter` que llama directamente al backend. Las herramientas MCP utilizan los mismos endpoints, por lo que ambos enfoques son equivalentes funcionalmente.

---

## Formato de Respuesta

Todas las herramientas devuelven respuestas en formato Markdown estructurado para fácil lectura:

```markdown
## 🍽️ Restaurante: La Trattoria

📍 **Dirección:** Av. Principal 123, Manta
🍕 **Cocina:** Italiana
⭐ **Calificación:** 4.5/5
💰 **Rango de precios:** $$
📞 **Teléfono:** +593 99 123 4567

---

**Descripción:**
Auténtica cocina italiana con ingredientes frescos importados...
```

---

## Ejecución del Servidor MCP

```bash
# Desarrollo
cd mesaYA_mcp
uv run mcp

# Producción (con Docker)
docker build -t mesaya-mcp .
docker run -e MESAYA_MCP_API_BASE_URL=http://backend:3000 mesaya-mcp
```

## Pruebas

```bash
# Ejecutar tests
cd mesaYA_mcp
uv run pytest

# Con cobertura
uv run pytest --cov=mesaYA_mcp
```
