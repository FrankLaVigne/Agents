#!/usr/bin/env python3
"""Sample MCP agent/client built with the official MCP Python SDK."""

from __future__ import annotations

import asyncio
import sys


async def run() -> None:
    try:
        from mcp import ClientSession, StdioServerParameters, types
        from mcp.client.stdio import stdio_client
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing dependency: mcp\n"
            "Install with: pip install \"mcp[cli]\"\n"
            f"Details: {exc}"
        ) from exc

    params = StdioServerParameters(command=sys.executable, args=["sdk_mcp_server.py"])

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools:", [tool.name for tool in tools.tools])

            result = await session.call_tool("echo", arguments={"text": "hello from sdk agent"})
            for block in result.content:
                if isinstance(block, types.TextContent):
                    print("Echo result:", block.text)

            search_result = await session.call_tool(
                "search_files", arguments={"pattern": "MCPClient|FastMCP"}
            )
            for block in search_result.content:
                if isinstance(block, types.TextContent):
                    print("\nSearch result:")
                    print(block.text)


def main() -> int:
    asyncio.run(run())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
