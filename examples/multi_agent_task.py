"""
Example: Send a task to multiple agents and collect results.

Demonstrates how a coordinator agent can fan out tasks to
multiple providers and aggregate results.

Usage:
    python multi_agent_task.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "meshkore-sdk-python", "src"))
from meshkore import MeshKoreRestAgent

HUB = os.environ.get("MESHKORE_HUB", "https://hub.meshkore.com")
AGENT_ID = os.environ.get("MESHKORE_AGENT_ID", "coordinator")
API_KEY = os.environ.get("MESHKORE_API_KEY", "your-api-key-here")


def main():
    agent = MeshKoreRestAgent(hub_url=HUB, agent_id=AGENT_ID, api_key=API_KEY)
    agent.register()

    # Find all online agents
    online = agent.list_online()
    providers = [a["agent_id"] for a in online if a["agent_id"] != AGENT_ID]

    if not providers:
        print("No other agents online. Start some provider agents first.")
        return

    print(f"Found {len(providers)} provider(s): {providers}")

    # Send task to all providers
    task = {
        "type": "task_request",
        "text": "What is the capital of France?",
        "parameters": {"require_source": True},
    }

    for provider in providers:
        print(f"Sending task to {provider}...")
        agent.send(provider, task)

    # Collect responses
    print(f"\nWaiting for responses (30s timeout)...")
    results = {}
    deadline = time.time() + 30

    while time.time() < deadline and len(results) < len(providers):
        messages = agent.poll()
        for msg in messages:
            sender = msg.get("from", "?")
            payload = msg.get("payload", {})
            results[sender] = payload
            print(f"  Got response from {sender}: {payload.get('text', '?')}")
        time.sleep(2)

    print(f"\nCollected {len(results)}/{len(providers)} responses.")
    for agent_id, result in results.items():
        print(f"  {agent_id}: {result.get('text', '(no text)')}")

    agent.close()


if __name__ == "__main__":
    main()
