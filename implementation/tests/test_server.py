import asyncio
import logging
import os
import sys
import unittest


IMPLEMENTATION_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, IMPLEMENTATION_DIR)

from init_db import init_db  # noqa: E402
from mcp_server import mcp  # noqa: E402


logging.getLogger("fastmcp.server.server").setLevel(logging.CRITICAL)


class SQLiteLabServerTests(unittest.TestCase):
    def setUp(self) -> None:
        init_db()

    def run_async(self, coro):
        return asyncio.run(coro)

    def test_search_with_pagination(self) -> None:
        result = self.run_async(
            mcp.call_tool(
                "search",
                {
                    "table_name": "students",
                    "filters": {"cohort": "A1"},
                    "limit": 1,
                    "offset": 0,
                },
            )
        )

        self.assertEqual(result.structured_content["count"], 1)
        self.assertEqual(result.structured_content["rows"][0]["cohort"], "A1")

    def test_insert_missing_required_column_fails(self) -> None:
        with self.assertRaises(Exception) as context:
            self.run_async(
                mcp.call_tool(
                    "insert",
                    {"table_name": "students", "data": {"name": "No Cohort"}},
                )
            )

        self.assertIn("Missing required column", str(context.exception))

    def test_search_unknown_table_fails(self) -> None:
        with self.assertRaises(Exception) as context:
            self.run_async(mcp.call_tool("search", {"table_name": "missing"}))

        self.assertIn("Unknown table", str(context.exception))


if __name__ == "__main__":
    unittest.main()
