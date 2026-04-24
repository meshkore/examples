"""
Agent B (Barcelona) — Listens for messages and echoes back.

Usage:
    pip install -e ../meshkore-sdk-python
    python agent_b.py
"""

import asyncio
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sdk", "src"))
from meshkore import MeshKoreAgent

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("agent-b")

HUB_URL = os.environ.get("MESHKORE_HUB", "http://localhost:8080")
AGENT_ID = "agent-b"
API_KEY = "dev-key-b"


async def main():
    agent = MeshKoreAgent(hub_url=HUB_URL, agent_id=AGENT_ID, api_key=API_KEY)
    await agent.connect()
    logger.info("Connected. Waiting for messages... (Ctrl+C to stop)")

    async def handle_message(from_agent: str, payload: dict):
        logger.info(f"Received from {from_agent}: {payload}")

        # Echo back with modification
        await agent.send(from_agent, {
            "type": "reply",
            "text": f"Hola de vuelta desde Barcelona! Recibido: {payload.get('text', '')}",
        })
        logger.info(f"Reply sent to {from_agent}")

    agent.on_message(handle_message)

    # Keep running forever
    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        pass
    finally:
        await agent.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down.")
