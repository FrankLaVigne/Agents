#!/usr/bin/env python3
"""MCP server implemented with the official Python MCP SDK."""

from __future__ import annotations

import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sample-sdk-mcp-server")
MAX_MATCHES = 20


@mcp.tool()
def echo(text: str) -> str:
    """Returns the same text you provide."""
    return f"Echo from SDK MCP server: {text}"


@mcp.tool()
def search_files(pattern: str) -> str:
    """Search text files in the current directory with a regex."""
    try:
        regex = re.compile(pattern)
    except re.error as exc:
        return f"Invalid regex: {exc}"

    matches: list[str] = []
    root = Path.cwd()
    for path in root.rglob("*"):
        if len(matches) >= MAX_MATCHES:
            break
        if not path.is_file() or path.name.startswith("."):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):
            if regex.search(line):
                matches.append(f"{path.relative_to(root)}:{line_no}: {line.strip()}")
                if len(matches) >= MAX_MATCHES:
                    break

    return "No matches found." if not matches else "\n".join(matches)


if __name__ == "__main__":
    mcp.run(transport="stdio")
