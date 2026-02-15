#!/usr/bin/env python3
"""Minimal A2A client sample."""

from __future__ import annotations

import asyncio
import uuid


async def run() -> None:
    try:
        import httpx
        from a2a.client import A2AClient
        from a2a.types import MessageSendParams, SendMessageRequest
        from a2a.utils import new_user_text_message
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing dependencies for A2A sample.\n"
            "Install with: pip install a2a-sdk httpx\n"
            f"Details: {exc}"
        ) from exc

    async with httpx.AsyncClient(timeout=30) as httpx_client:
        client = A2AClient(httpx_client=httpx_client, url="http://localhost:9999")
        send_request = SendMessageRequest(
            id=str(uuid.uuid4()),
            params=MessageSendParams(message=new_user_text_message(text="hello from A2A client")),
        )
        response = await client.send_message(send_request)
        print(response.model_dump_json(indent=2, exclude_none=True))


def main() -> int:
    asyncio.run(run())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
