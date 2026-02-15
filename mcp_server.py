#!/usr/bin/env python3
"""Minimal MCP server over stdio.

Implements a tiny subset of MCP-style JSON-RPC methods:
- initialize
- tools/list
- tools/call
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

MAX_MATCHES = 20


def search_files(pattern: str, root: Path) -> list[str]:
    """Return up to MAX_MATCHES file:line matches for a regex pattern."""
    if not pattern:
        return []

    try:
        regex = re.compile(pattern)
    except re.error as exc:
        raise ValueError(f"Invalid regex: {exc}") from exc

    matches: list[str] = []
    for path in root.rglob("*"):
        if len(matches) >= MAX_MATCHES:
            break
        if not path.is_file():
            continue
        if path.name.startswith("."):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):
            if regex.search(line):
                rel = path.relative_to(root)
                snippet = line.strip()
                matches.append(f"{rel}:{line_no}: {snippet}")
                if len(matches) >= MAX_MATCHES:
                    break
    return matches


def send_json(message: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(message) + "\n")
    sys.stdout.flush()


def read_json_lines() -> dict[str, Any] | None:
    line = sys.stdin.readline()
    if not line:
        return None
    line = line.strip()
    if not line:
        return None
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def make_error(req_id: Any, code: int, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": code, "message": message},
    }


def handle_request(req: dict[str, Any]) -> dict[str, Any]:
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "sample-mcp-server", "version": "0.1.0"},
                "capabilities": {"tools": {}},
            },
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "echo",
                        "description": "Returns the same text you provide.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string", "description": "Text to echo."}
                            },
                            "required": ["text"],
                        },
                    },
                    {
                        "name": "search_files",
                        "description": "Searches text files in the current directory with a regex.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "pattern": {
                                    "type": "string",
                                    "description": "Regex pattern to search for.",
                                }
                            },
                            "required": ["pattern"],
                        },
                    },
                ]
            },
        }

    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name == "echo":
            text = arguments.get("text")
            if not isinstance(text, str):
                return make_error(req_id, -32602, "'text' must be a string")
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": f"Echo from MCP server: {text}"}],
                    "isError": False,
                },
            }

        if tool_name == "search_files":
            pattern = arguments.get("pattern")
            if not isinstance(pattern, str):
                return make_error(req_id, -32602, "'pattern' must be a string")
            try:
                matches = search_files(pattern, Path.cwd())
            except ValueError as exc:
                return make_error(req_id, -32602, str(exc))
            result_text = "No matches found." if not matches else "\n".join(matches)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": result_text}],
                    "isError": False,
                },
            }

        return make_error(req_id, -32602, f"Unknown tool: {tool_name}")

    return make_error(req_id, -32601, f"Method not found: {method}")


def main() -> None:
    while True:
        request = read_json_lines()
        if request is None:
            if sys.stdin.closed:
                break
            continue

        response = handle_request(request)
        send_json(response)


if __name__ == "__main__":
    main()
