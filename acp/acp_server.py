#!/usr/bin/env python3
"""Minimal ACP server sample using the ACP Python SDK."""

from __future__ import annotations

from acp_sdk.models import Message
from acp_sdk.server import Server

server = Server()


@server.agent()
async def echo(input: list[Message]):
    """Echoes every message sent by the client."""
    for message in input:
        yield message


if __name__ == "__main__":
    try:
        server.run(port=8001)
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing dependencies for ACP sample.\n"
            "Install with: pip install acp-sdk uvicorn\n"
            f"Details: {exc}"
        ) from exc
