import os
import sqlite3
from typing import Any


DB_PATH = os.path.join(os.path.dirname(__file__), "lab_database.db")


def get_db_connection() -> sqlite3.Connection:
    """Create a SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def get_schema() -> dict[str, list[dict[str, Any]]]:
    """Return the full database schema as table -> column metadata."""
    with get_db_connection() as conn:
        tables = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
            """
        ).fetchall()

        schema: dict[str, list[dict[str, Any]]] = {}
        for table in tables:
            table_name = table["name"]
            columns = conn.execute(f'PRAGMA table_info("{table_name}");').fetchall()
            schema[table_name] = [
                {
                    "name": column["name"],
                    "type": column["type"],
                    "notnull": bool(column["notnull"]),
                    "default": column["dflt_value"],
                    "primary_key": bool(column["pk"]),
                }
                for column in columns
            ]
        return schema


def get_table_schema(table_name: str) -> list[dict[str, Any]] | None:
    """Return schema metadata for a single table, or None when absent."""
    return get_schema().get(table_name)


def execute_query(sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    """Execute a read query safely with bound parameters."""
    with get_db_connection() as conn:
        rows = conn.execute(sql, params).fetchall()
        return [dict(row) for row in rows]


def execute_write(sql: str, params: tuple[Any, ...] = ()) -> int:
    """Execute a write query safely with bound parameters and return last row id."""
    with get_db_connection() as conn:
        cursor = conn.execute(sql, params)
        conn.commit()
        return int(cursor.lastrowid)
