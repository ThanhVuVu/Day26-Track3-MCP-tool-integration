import asyncio
import json
import logging

from init_db import init_db
from mcp_server import mcp


logging.getLogger("fastmcp.server.server").setLevel(logging.CRITICAL)


def print_result(title: str, result) -> None:
    print(f"\n--- {title} ---")
    print(json.dumps(result, indent=2, default=str))


def clean_tool_error(exc: Exception) -> str:
    message = str(exc)
    marker = ": "
    if message.startswith("Error calling tool ") and marker in message:
        return message.split(marker, 1)[1]
    return message


async def run_tests() -> None:
    init_db()

    database_schema = await mcp.read_resource("schema://database")
    print_result("Resource: schema://database", database_schema)

    table_schema = await mcp.read_resource("schema://table/students")
    print_result("Resource: schema://table/students", table_schema)

    paged_search = await mcp.call_tool(
        "search",
        {
            "table_name": "students",
            "filters": {"cohort": "A1"},
            "sort_by": "score",
            "limit": 2,
            "offset": 0,
        },
    )
    print_result("Search with filters and pagination", paged_search)

    avg_score = await mcp.call_tool(
        "aggregate",
        {"table_name": "students", "column": "score", "function": "avg"},
    )
    print_result("Aggregate average score", avg_score)

    inserted = await mcp.call_tool(
        "insert",
        {
            "table_name": "students",
            "data": {"name": "Test User", "cohort": "T1", "score": 100.0},
        },
    )
    print_result("Insert valid student", inserted)

    for title, tool_name, args in [
        (
            "Insert error: missing required field",
            "insert",
            {"table_name": "students", "data": {"name": "Missing Cohort"}},
        ),
        (
            "Search error: table does not exist",
            "search",
            {"table_name": "not_a_table"},
        ),
        (
            "Aggregate error: function not allowed",
            "aggregate",
            {"table_name": "students", "column": "score", "function": "median"},
        ),
    ]:
        try:
            await mcp.call_tool(tool_name, args)
        except Exception as exc:
            print_result(title, {"error": clean_tool_error(exc)})


if __name__ == "__main__":
    asyncio.run(run_tests())
