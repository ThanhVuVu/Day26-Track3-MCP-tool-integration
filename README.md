# SQLite Database MCP Server Lab

This project implements a FastMCP server named `sqlite-lab` for a SQLite database.
It exposes database schema resources and safe tools for search, insert, and aggregate
operations over `students`, `courses`, and `enrollments`.

## Requirements

- Python 3.11+
- `fastmcp`

Install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install fastmcp
```

## Quick Start

Initialize the database first:

```powershell
.\.venv\Scripts\python.exe implementation\init_db.py
```

Run the verification script:

```powershell
.\.venv\Scripts\python.exe implementation\verify_server.py
```

Run the automated tests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s implementation\tests
```

Start the MCP server over stdio:

```powershell
.\.venv\Scripts\python.exe implementation\mcp_server.py
```

Open MCP Inspector:

```powershell
.\start_inspector.bat
```

## MCP Capabilities

Resources:

- `schema://database`: full database schema as JSON.
- `schema://table/{table_name}`: schema for one table.

Tools:

- `search(table_name, filters, sort_by, limit, offset)`: exact-match search with pagination.
- `insert(table_name, data)`: validated single-row insert.
- `aggregate(table_name, column, function)`: `count`, `avg`, `sum`, `min`, or `max`.

All dynamic table and column names are validated against the live SQLite schema before
SQL is executed. Values are passed with SQLite parameter binding.

## Gemini CLI Example

Use absolute paths. Example for this repo:

```powershell
gemini mcp add sqlite-lab D:\Day26-Track3-MCP-tool-integration\.venv\Scripts\python.exe D:\Day26-Track3-MCP-tool-integration\implementation\mcp_server.py --description "SQLite lab FastMCP server" --timeout 10000
```

Check the server:

```powershell
gemini mcp list
gemini --allowed-mcp-server-names sqlite-lab --yolo -p "Use sqlite-lab to show students in cohort A1"
```

## Claude Code Example

Add this to `.mcp.json`:

```json
{
  "mcpServers": {
    "sqlite-lab": {
      "type": "stdio",
      "command": "D:\\Day26-Track3-MCP-tool-integration\\.venv\\Scripts\\python.exe",
      "args": [
        "D:\\Day26-Track3-MCP-tool-integration\\implementation\\mcp_server.py"
      ]
    }
  }
}
```

## Project Structure

- `implementation/db.py`: SQLite data access helpers.
- `implementation/init_db.py`: schema creation and sample data seeding.
- `implementation/mcp_server.py`: FastMCP resources and tools.
- `implementation/verify_server.py`: local verification script.
- `implementation/tests/`: reserved for additional automated tests.
