"""
Agent A (Madrid) — Sends a greeting to Agent B and waits for reply.

Usage:
    pip install -e ../meshkore-sdk-python
    python agent_a.py
"""

import asyncio
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sdk", "src"))
from meshkore import MeshKoreAgent

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("agent-a")

HUB_URL = os.environ.get("MESHKORE_HUB", "http://localhost:8080")
AGENT_ID = "agent-a"
API_KEY = "dev-key-a"
TARGET = "agent-b"


async def main():
    agent = MeshKoreAgent(hub_url=HUB_URL, agent_id=AGENT_ID, api_key=API_KEY)
    await agent.connect()
    logger.info("Connected. Waiting for agent-b to come online...")

    # Poll until target is online
    while True:
        online = await agent.list_online()
        if TARGET in online:
            break
        await asyncio.sleep(1)

    logger.info("agent-b is online! Sending greeting...")

    # Set up reply handler
    reply_received = asyncio.Event()

    async def on_reply(from_agent: str, payload: dict):
        logger.info(f"Reply from {from_agent}: {payload}")
        reply_received.set()

    agent.on_message(on_reply)

    # Send greeting
    await agent.send(TARGET, {
        "type": "greeting",
        "text": "Hola desde Madrid!",
    })
    logger.info("Greeting sent. Waiting for reply...")

    # Wait for reply
    await asyncio.wait_for(reply_received.wait(), timeout=30)

    logger.info("Done! Disconnecting.")
    await agent.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
