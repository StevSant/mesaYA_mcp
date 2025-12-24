# MesaYA MCP

MCP (Model Context Protocol) server for the MesaYA restaurant reservation platform.

## Quick Start

```bash
# Run MCP server (stdio transport - for local tools)
uv run app

# Run MCP Gateway (HTTP/SSE transport - for web clients)
uv run gateway

# Or with explicit flags
uv run app --sse      # SSE mode
uv run app --stdio    # stdio mode (default)

# Inspect with MCP inspector
npx @modelcontextprotocol/inspector uv --directory . run app --port 3333
```

## Transport Modes

### stdio (default)

Standard input/output transport for local tool integration.

```bash
uv run app
```

### SSE (MCP Gateway)

HTTP/SSE transport for web applications and remote access.

```bash
uv run gateway

# Or with environment variables
MCP_GATEWAY_HOST=0.0.0.0 MCP_GATEWAY_PORT=8000 uv run gateway
```

**Gateway Endpoints:**

- `GET /sse` - SSE endpoint for MCP communication
- `POST /messages` - Message endpoint for MCP commands
- `GET /health` - Health check

## Project Structure

```text
mesaYA_mcp/
├── src/
│   └── mesaYA_mcp/
│       ├── __init__.py           # Package initialization
│       ├── __main__.py           # MCP server entry point
│       ├── server.py             # FastMCP instance
│       ├── gateway.py            # MCP Gateway entry point
│       ├── tools/                # Tool modules (LangChain pattern)
│       │   ├── __init__.py       # Tool registration
│       │   ├── _formatters.py    # Shared formatting helpers
│       │   ├── restaurants.py    # 7 restaurant tools
│       │   ├── reservations.py   # 10 reservation tools
│       │   ├── menus.py          # 5 menu tools
│       │   └── users.py          # 3 user tools
│       └── shared/               # Shared modules
│           ├── application/      # Application layer (ports)
│           ├── core/             # Core configuration
│           └── infrastructure/   # Infrastructure layer (adapters)
├── .env.template
├── pyproject.toml
└── README.md
```

## Architecture

This project follows a **Hexagonal Architecture** (Ports and Adapters):

- **Ports**: Abstract interfaces in `shared/application/ports/`
- **Adapters**: Concrete implementations in `shared/infrastructure/adapters/`
- **Tools**: Flat structure following LangChain's recommended pattern

### LangChain MCP Pattern

Tools are organized in flat modules following LangChain's recommendation:

```python
# server.py - Single MCP instance
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("mesaYA_mcp")

# tools/restaurants.py - Import and decorate
from mesaYA_mcp.server import mcp

@mcp.tool()
async def search_restaurants(...):
    ...

# __main__.py - Import tools, run server
import mesaYA_mcp.tools  # Registers all tools
mcp.run()
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
