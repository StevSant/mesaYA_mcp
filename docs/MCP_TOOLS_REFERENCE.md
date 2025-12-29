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

> **💡 Diseño User-Friendly**: Todas las herramientas del MCP están diseñadas para ser usadas por agentes de IA en conversaciones con usuarios.
> En lugar de requerir UUIDs internos, las herramientas aceptan **nombres de restaurantes**, **emails de usuarios** y otros identificadores amigables.
> El sistema resuelve automáticamente estos nombres a los IDs internos correspondientes.

### 🍽️ Restaurantes (8 herramientas)

#### `search_restaurants`

Busca restaurantes por diferentes criterios usando filtros específicos.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `name` | string | No | Nombre del restaurante (coincidencia parcial, preferido para búsquedas) |
| `city` | string | No | Ciudad o ubicación |
| `cuisine_type` | string | No | Tipo de cocina (italiana, mexicana, etc.) |
| `query` | string | No | Término de búsqueda general |
| `is_active` | bool | No | Solo restaurantes activos (default: true) |
| `limit` | int | No | Número máximo de resultados (default: 10) |

**Ejemplo de uso:**

```json
{
  "tool": "search_restaurants",
  "arguments": {
    "name": "Pizza Palace",
    "city": "Manta",
    "limit": 5
  }
}
```

#### `get_restaurant_by_name`

Obtiene información detallada de un restaurante por su nombre. **Preferido sobre `get_restaurant_info` cuando conoces el nombre.**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `name` | string | Sí | Nombre exacto del restaurante |

**Ejemplo de uso:**

```json
{
  "tool": "get_restaurant_by_name",
  "arguments": {
    "name": "Pizza Palace"
  }
}
```

#### `get_restaurant_info`

Obtiene información detallada de un restaurante. **Acepta nombre o UUID.**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant` | string | Sí | Nombre del restaurante o UUID (ej: "Pizza Palace") |

**Ejemplo de uso:**

```json
{
  "tool": "get_restaurant_info",
  "arguments": {
    "restaurant": "La Trattoria"
  }
}
```

#### `get_nearby_restaurants`

Busca restaurantes cercanos a una ubicación geográfica.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `latitude` | float | Sí | Latitud (-90 a 90) |
| `longitude` | float | Sí | Longitud (-180 a 180) |
| `radius_km` | float | No | Radio de búsqueda en km (default: 5.0) |
| `limit` | int | No | Máximo de resultados (default: 10) |

#### `get_restaurant_schedule`

Obtiene los horarios disponibles de un restaurante. **Acepta nombre o UUID.**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant` | string | Sí | Nombre del restaurante o UUID |

#### `get_restaurant_menu`

Obtiene el menú completo de un restaurante. **Acepta nombre o UUID.**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant` | string | Sí | Nombre del restaurante o UUID |
| `active_only` | bool | No | Solo mostrar items activos (default: true) |

#### `get_restaurant_sections`

Obtiene las secciones/áreas de un restaurante. **Acepta nombre o UUID.**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant` | string | Sí | Nombre del restaurante o UUID |

#### `get_section_tables`

Obtiene las mesas disponibles en una sección. **Acepta nombre de sección con contexto del restaurante.**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `section` | string | Sí | Nombre de la sección o UUID (ej: "Terraza") |
| `restaurant` | string | No* | Nombre del restaurante (requerido si usas nombre de sección) |

**Ejemplo de uso:**

```json
{
  "tool": "get_section_tables",
  "arguments": {
    "section": "Terraza",
    "restaurant": "Pizza Palace"
  }
}
```

---

### 📅 Reservaciones (10 herramientas)

#### `create_reservation`

Crea una nueva reservación. **Usa nombre de restaurante y email del cliente.**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant` | string | Sí | Nombre del restaurante (ej: "Pizza Palace") |
| `customer_email` | string | Sí | Email del cliente (ej: "<juan@email.com>") |
| `date` | string | Sí | Fecha (YYYY-MM-DD) |
| `time` | string | Sí | Hora (HH:MM) |
| `party_size` | int | Sí | Número de comensales |
| `section_name` | string | No | Nombre de la sección (ej: "Terraza") |
| `table_name` | string | No | Nombre/número de mesa (ej: "Mesa 5") |
| `notes` | string | No | Notas adicionales |

**Ejemplo de uso:**

```json
{
  "tool": "create_reservation",
  "arguments": {
    "restaurant": "Pizza Palace",
    "customer_email": "juan.perez@email.com",
    "date": "2025-01-20",
    "time": "19:30",
    "party_size": 4,
    "section_name": "Terraza",
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
| `status` | string | No | Estado (pending, confirmed, cancelled, completed, no_show) |
| `date_from` | string | No | Fecha inicial (YYYY-MM-DD) |
| `date_to` | string | No | Fecha final (YYYY-MM-DD) |
| `limit` | int | No | Máximo de resultados (default: 20) |

#### `get_restaurant_reservations`

Obtiene todas las reservaciones de un restaurante. **Acepta nombre o UUID.**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant` | string | Sí | Nombre del restaurante o UUID |
| `date` | string | No | Filtrar por fecha |
| `status` | string | No | Filtrar por estado |

**Ejemplo de uso:**

```json
{
  "tool": "get_restaurant_reservations",
  "arguments": {
    "restaurant": "Pizza Palace",
    "date": "2025-01-20",
    "status": "confirmed"
  }
}
```

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

Obtiene estadísticas de reservaciones. **Acepta nombre de restaurante o UUID.**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant` | string | No | Nombre del restaurante o UUID |
| `date_from` | string | No | Fecha inicial |
| `date_to` | string | No | Fecha final |

**Ejemplo de uso:**

```json
{
  "tool": "get_reservation_analytics",
  "arguments": {
    "restaurant": "Pizza Palace",
    "date_from": "2025-01-01",
    "date_to": "2025-01-31"
  }
}
```

---

### 🍕 Menús y Platillos (5 herramientas)

#### `get_menu`

Obtiene un menú específico por ID.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `menu_id` | string | Sí | UUID del menú |

#### `list_menus`

Lista todos los menús de un restaurante. **Acepta nombre o UUID.**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant` | string | No | Nombre del restaurante o UUID |
| `active_only` | bool | No | Solo mostrar menús activos (default: true) |
| `limit` | int | No | Máximo de resultados (default: 20) |

**Ejemplo de uso:**

```json
{
  "tool": "list_menus",
  "arguments": {
    "restaurant": "Pizza Palace"
  }
}
```

#### `search_dishes`

Busca platillos con filtros. **Acepta nombre de restaurante o UUID.**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `query` | string | Sí | Término de búsqueda |
| `restaurant` | string | No | Nombre del restaurante o UUID |
| `category` | string | No | Categoría: appetizer, main, dessert, etc |
| `max_price` | float | No | Precio máximo |
| `vegetarian` | bool | No | Solo platillos vegetarianos |
| `limit` | int | No | Máximo de resultados (default: 20) |

**Ejemplo de uso:**

```json
{
  "tool": "search_dishes",
  "arguments": {
    "query": "pizza",
    "restaurant": "Pizza Palace",
    "max_price": 15.00
  }
}
```

#### `get_dish`

Obtiene detalles de un platillo específico.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `dish_id` | string | Sí | UUID del platillo |

#### `get_menu_analytics`

Obtiene estadísticas de menús. **Acepta nombre de restaurante o UUID.**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `restaurant` | string | No | Nombre del restaurante o UUID |
| `date_from` | string | No | Fecha inicial |
| `date_to` | string | No | Fecha final |

---

### 👤 Usuarios (4 herramientas)

#### `get_user_by_email`

Obtiene información de un usuario por su email. **Preferido sobre `get_user` cuando conoces el email.**

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `email` | string | Sí | Email del usuario |

**Ejemplo de uso:**

```json
{
  "tool": "get_user_by_email",
  "arguments": {
    "email": "usuario@ejemplo.com"
  }
}
```

#### `get_user`

Obtiene información de un usuario por UUID (use `get_user_by_email` si conoce el email).

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `user_id` | string | Sí | UUID del usuario |

#### `list_users`

Lista usuarios con filtros específicos.

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `email` | string | No | Filtrar por email exacto (preferido para búsquedas) |
| `name` | string | No | Filtrar por nombre (coincidencia parcial) |
| `role` | string | No | Filtrar por rol (ADMIN, OWNER, USER) |
| `active_only` | bool | No | Solo usuarios activos (default: true) |
| `search` | string | No | Búsqueda general por nombre o email |
| `limit` | int | No | Máximo de resultados (default: 20) |

**Ejemplo de uso:**

```json
{
  "tool": "list_users",
  "arguments": {
    "email": "usuario@ejemplo.com"
  }
}
```

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
