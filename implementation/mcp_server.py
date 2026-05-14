import json
from typing import Any

from fastmcp import FastMCP

from db import execute_query, execute_write, get_schema, get_table_schema


mcp = FastMCP("sqlite-lab")

ALLOWED_AGGREGATES = {"count", "avg", "sum", "min", "max"}


def _table_columns(table_name: str) -> set[str]:
    table_schema = get_table_schema(table_name)
    if table_schema is None:
        raise ValueError(f"Unknown table: {table_name}")
    return {column["name"] for column in table_schema}


def validate_input(table_name: str, columns: list[str] | set[str] | None = None) -> None:
    """Validate table and column names against the live SQLite schema."""
    allowed_columns = _table_columns(table_name)
    if not columns:
        return

    invalid_columns = sorted(set(columns) - allowed_columns)
    if invalid_columns:
        raise ValueError(
            f"Invalid column(s) for table {table_name}: {', '.join(invalid_columns)}"
        )


def _required_insert_columns(table_name: str) -> set[str]:
    table_schema = get_table_schema(table_name)
    if table_schema is None:
        raise ValueError(f"Unknown table: {table_name}")

    return {
        column["name"]
        for column in table_schema
        if column["notnull"] and not column["primary_key"] and column["default"] is None
    }


@mcp.resource("schema://database")
def database_schema() -> str:
    """Return JSON metadata for all tables and columns."""
    return json.dumps(get_schema(), indent=2)


@mcp.resource("schema://table/{table_name}")
def table_schema(table_name: str) -> str:
    """Return JSON metadata for one table."""
    schema = get_table_schema(table_name)
    if schema is None:
        raise ValueError(f"Unknown table: {table_name}")
    return json.dumps({table_name: schema}, indent=2)


@mcp.tool
def search(
    table_name: str,
    filters: dict[str, Any] | None = None,
    sort_by: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """Search rows with optional exact-match filters, sorting, and pagination."""
    filters = filters or {}
    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100")
    if offset < 0:
        raise ValueError("offset must be greater than or equal to 0")

    filter_columns = set(filters.keys())
    columns_to_validate = set(filter_columns)
    if sort_by:
        columns_to_validate.add(sort_by)
    validate_input(table_name, columns_to_validate)

    where_clause = ""
    params: list[Any] = []
    if filters:
        where_parts = [f'"{column}" = ?' for column in filters]
        where_clause = " WHERE " + " AND ".join(where_parts)
        params.extend(filters.values())

    order_clause = f' ORDER BY "{sort_by}"' if sort_by else ""
    sql = f'SELECT * FROM "{table_name}"{where_clause}{order_clause} LIMIT ? OFFSET ?;'
    params.extend([limit, offset])

    rows = execute_query(sql, tuple(params))
    return {
        "table": table_name,
        "filters": filters,
        "limit": limit,
        "offset": offset,
        "count": len(rows),
        "rows": rows,
    }


@mcp.tool
def insert(table_name: str, data: dict[str, Any]) -> dict[str, Any]:
    """Insert one row after validating the target table and columns."""
    if not data:
        raise ValueError("data must contain at least one column")

    validate_input(table_name, set(data.keys()))
    missing_columns = sorted(_required_insert_columns(table_name) - set(data.keys()))
    if missing_columns:
        raise ValueError(f"Missing required column(s): {', '.join(missing_columns)}")

    columns = list(data.keys())
    column_sql = ", ".join(f'"{column}"' for column in columns)
    placeholder_sql = ", ".join("?" for _ in columns)
    sql = f'INSERT INTO "{table_name}" ({column_sql}) VALUES ({placeholder_sql});'
    new_id = execute_write(sql, tuple(data[column] for column in columns))

    return {
        "table": table_name,
        "inserted_id": new_id,
        "data": data,
    }


@mcp.tool
def aggregate(
    table_name: str,
    column: str,
    function: str,
) -> dict[str, Any]:
    """Calculate a single aggregate value for a table column."""
    function_name = function.lower()
    if function_name not in ALLOWED_AGGREGATES:
        raise ValueError(f"Unsupported aggregate function: {function}")

    validate_input(table_name, {column})
    sql = f'SELECT {function_name.upper()}("{column}") AS value FROM "{table_name}";'
    rows = execute_query(sql)
    return {
        "table": table_name,
        "column": column,
        "function": function_name,
        "value": rows[0]["value"],
    }


if __name__ == "__main__":
    mcp.run()
