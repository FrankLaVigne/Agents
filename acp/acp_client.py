#!/usr/bin/env python3
"""Minimal ACP client sample."""

from __future__ import annotations

import asyncio


async def main() -> None:
    try:
        from acp_sdk.client import Client
        from acp_sdk.models import Message, MessagePart
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing dependencies for ACP sample.\n"
            "Install with: pip install acp-sdk httpx\n"
            f"Details: {exc}"
        ) from exc

    async with Client(base_url="http://localhost:8001") as client:
        run = await client.run_sync(
            agent="echo",
            input=[
                Message(
                    role="user",
                    parts=[
                        MessagePart(
                            content="hello from ACP client",
                            content_type="text/plain",
                        )
                    ],
                )
            ],
        )
        print(run)


if __name__ == "__main__":
    asyncio.run(main())
