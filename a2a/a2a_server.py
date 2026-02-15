#!/usr/bin/env python3
"""Minimal A2A server sample using the A2A Python SDK."""

from __future__ import annotations

import os


def main() -> None:
    try:
        import uvicorn
        from a2a.server.agent_execution import AgentExecutor, RequestContext
        from a2a.server.apps import A2AStarletteApplication
        from a2a.server.tasks import TaskUpdater
        from a2a.types import (
            AgentCapabilities,
            AgentCard,
            AgentSkill,
            Message,
            Part,
            TextPart,
        )
        from a2a.utils import new_agent_text_message
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing dependencies for A2A sample.\n"
            "Install with: pip install a2a-sdk uvicorn\n"
            f"Details: {exc}"
        ) from exc

    class EchoAgentExecutor(AgentExecutor):
        async def execute(self, context: RequestContext, event_queue) -> None:
            updater = TaskUpdater(event_queue, context.task_id, context.context_id)
            user_text = _extract_text(context.message)
            await updater.submit()
            await updater.add_artifact(
                [Part(root=TextPart(text=f"A2A echo: {user_text}"))],
                name="result",
            )
            await updater.complete()

        async def cancel(self, context: RequestContext, event_queue) -> None:
            raise RuntimeError("Cancel not supported in this sample")

    def _extract_text(message: Message) -> str:
        for part in message.parts:
            root = part.root
            if isinstance(root, TextPart):
                return root.text
        return "(no text)"

    card = AgentCard(
        name="A2A Echo Agent",
        description="A tiny A2A agent that echoes your message.",
        url="http://localhost:9999/",
        version="1.0.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=False),
        skills=[AgentSkill(id="echo", name="Echo", description="Echo back user text")],
    )

    server = A2AStarletteApplication(agent_card=card, http_handler=EchoAgentExecutor()).build()
    uvicorn.run(server, host="0.0.0.0", port=int(os.getenv("PORT", "9999")))


if __name__ == "__main__":
    main()
