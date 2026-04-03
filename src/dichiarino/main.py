"""Dichiarino MCP Server - entry point."""

from __future__ import annotations

from dichiarino.server import create_server


def main() -> None:
    """Run Dichiarino as a stdio MCP server."""
    mcp = create_server()
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
