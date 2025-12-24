# MesaYA MCP

MCP (Model Context Protocol) server for the MesaYA restaurant reservation platform.

## Quick Start

```bash
# Run MCP server
uv run app

# Inspect with MCP inspector
npx @modelcontextprotocol/inspector uv --directory . run app --port 3333
```

## Project Structure

```text
mesaYA_mcp/
├── src/
│   └── mesaYA_mcp/
│       ├── __init__.py           # Package initialization
│       ├── __main__.py           # MCP server entry point
│       ├── features/             # Domain-specific tools
│       │   ├── restaurants/      # Restaurant-related tools
│       │   │   ├── __init__.py
│       │   │   └── tools.py
│       │   └── reservations/     # Reservation-related tools
│       │       ├── __init__.py
│       │       └── tools.py
│       └── shared/               # Shared modules
│           ├── application/      # Application layer (ports)
│           │   └── ports/
│           │       ├── __init__.py
│           │       └── logger_port.py
│           ├── core/             # Core configuration
│           │   ├── __init__.py
│           │   ├── config.py
│           │   └── container.py
│           └── infrastructure/   # Infrastructure layer (adapters)
│               └── adapters/
│                   ├── __init__.py
│                   └── logger_adapter.py
├── .env.template
├── pyproject.toml
└── README.md
```

## Architecture

This project follows a **Hexagonal Architecture** (Ports and Adapters):

- **Ports**: Abstract interfaces in `shared/application/ports/`
- **Adapters**: Concrete implementations in `shared/infrastructure/adapters/`
- **Features**: Domain-specific tools organized by feature

### Logger Port/Adapter Pattern

The logger follows the same pattern as other dependencies:

```python
# Port (abstract interface)
class LoggerPort(ABC):
    @abstractmethod
    def info(self, message: str, context: str | None = None, **meta: Any) -> None:
        pass
    # ... other methods

# Adapter (concrete implementation)
class LoggerAdapter(LoggerPort):
    def info(self, message: str, context: str | None = None, **meta: Any) -> None:
        self._log(logging.INFO, message, context, **meta)
```

## Installation

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

## Configuration

Copy the environment template and configure:

```bash
cp .env.template .env
```

Edit `.env` with your settings:

```env
APP_NAME=mesaYA_mcp
ENVIRONMENT=development
LOG_LEVEL=INFO
BACKEND_API_URL=http://localhost:3000
```

## Running the Server

```bash
# Using the script entry point
uv run app

# Or directly with Python
python -m mesaYA_mcp
```

## Available Tools

### Restaurant Tools

- `mcp_search_restaurants` - Search restaurants by name, cuisine, or location
- `mcp_get_restaurant_info` - Get detailed restaurant information

### Reservation Tools

- `mcp_create_reservation` - Create a new reservation
- `mcp_check_availability` - Check table availability
- `mcp_get_reservation_status` - Get reservation status

## Logging

All tools use structured JSON logging via the `LoggerAdapter`:

```python
from mesaYA_mcp.shared.core.container import Container

logger = Container.resolve("logger")
logger.info("Message", context="tool_name", key="value")
```

## Development

### Adding a New Feature

1. Create a new folder in `features/`:

   ```text
   features/your_feature/
   ├── __init__.py
   └── tools.py
   ```

2. Implement tools in `tools.py` using the logger:

   ```python
   from mesaYA_mcp.shared.core.container import Container

   async def your_tool(param: str) -> str:
       logger = Container.resolve("logger")
       logger.info("Executing tool", context="your_tool", param=param)
       # ... implementation
   ```

3. Register tools in `__main__.py`

### Adding a New Port/Adapter

1. Create the port in `shared/application/ports/your_port.py`
2. Create the adapter in `shared/infrastructure/adapters/your_adapter.py`
3. Register in container via `_configure_dependencies()`
