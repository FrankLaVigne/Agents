#!/usr/bin/env python3
"""Sample agent that connects to the local MCP server over stdio."""

from __future__ import annotations

import json
import subprocess
import sys
from typing import Any


class MCPClient:
    def __init__(self, server_cmd: list[str]) -> None:
        self.proc = subprocess.Popen(
            server_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._id = 1

    def close(self) -> None:
        if self.proc.stdin:
            self.proc.stdin.close()
        self.proc.terminate()
        self.proc.wait(timeout=2)

    def call(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        if self.proc.stdin is None or self.proc.stdout is None:
            raise RuntimeError("MCP process streams are not available")

        request = {
            "jsonrpc": "2.0",
            "id": self._id,
            "method": method,
            "params": params or {},
        }
        self._id += 1

        self.proc.stdin.write(json.dumps(request) + "\n")
        self.proc.stdin.flush()

        line = self.proc.stdout.readline()
        if not line:
            stderr = ""
            if self.proc.stderr:
                stderr = self.proc.stderr.read()
            raise RuntimeError(f"No response from MCP server. stderr: {stderr}")

        response = json.loads(line)
        if "error" in response:
            raise RuntimeError(f"MCP error: {response['error']}")
        return response["result"]


def render_content(result: dict[str, Any]) -> str:
    content = result.get("content", [])
    parts: list[str] = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            parts.append(str(item.get("text", "")))
    return "\n".join(parts) if parts else json.dumps(result, indent=2)


def run_chat_loop(client: MCPClient) -> None:
    print("\nInteractive mode")
    print("Commands:")
    print("  /echo <text>      - call the echo tool")
    print("  /search <regex>   - call the search_files tool")
    print("  /tools            - list tools")
    print("  /quit             - exit\n")

    while True:
        try:
            user_input = input("agent> ").strip()
        except EOFError:
            print()
            break

        if not user_input:
            continue
        if user_input == "/quit":
            break
        if user_input == "/tools":
            tools = client.call("tools/list")
            print(json.dumps(tools, indent=2))
            continue

        if user_input.startswith("/search "):
            pattern = user_input[len("/search ") :].strip()
            if not pattern:
                print("Missing pattern. Example: /search MCPClient")
                continue
            result = client.call(
                "tools/call",
                {"name": "search_files", "arguments": {"pattern": pattern}},
            )
            print(render_content(result))
            continue

        if user_input.startswith("/echo "):
            text = user_input[len("/echo ") :].strip()
            if not text:
                print("Missing text. Example: /echo hello")
                continue
            result = client.call("tools/call", {"name": "echo", "arguments": {"text": text}})
            print(render_content(result))
            continue

        # Default routing: treat free text as an echo request.
        result = client.call("tools/call", {"name": "echo", "arguments": {"text": user_input}})
        print(render_content(result))


def main() -> int:
    client = MCPClient([sys.executable, "mcp_server.py"])

    try:
        init = client.call(
            "initialize",
            {"clientInfo": {"name": "sample-agent", "version": "0.2.0"}},
        )
        print("Initialized:", json.dumps(init, indent=2))

        tools = client.call("tools/list")
        print("\nAvailable tools:", json.dumps(tools, indent=2))

        result = client.call(
            "tools/call",
            {"name": "echo", "arguments": {"text": "hello from agent"}},
        )
        print("\nOne-shot tool result:", render_content(result))

        run_chat_loop(client)

    finally:
        client.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
