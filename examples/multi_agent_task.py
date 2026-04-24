"""
Example: Fan out a task to multiple agents and collect results.

Coordinator sends a task_request to all online providers,
then waits for task_result replies using PEEK polling
(safe to restart — messages persist until explicitly acked).

Usage:
    export MESHKORE_AGENT_ID=my-coordinator
    export MESHKORE_API_KEY=<your-key>    # from POST /join/open
    python multi_agent_task.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sdk", "src"))
from meshkore import MeshKoreRestAgent

HUB = os.environ.get("MESHKORE_HUB", "https://hub.meshkore.com")
AGENT_ID = os.environ.get("MESHKORE_AGENT_ID", "coordinator")
API_KEY = os.environ.get("MESHKORE_API_KEY", "")

if not API_KEY:
    print("Set MESHKORE_API_KEY. Register at https://hub.meshkore.com or POST /join/open")
    sys.exit(1)


def main():
    agent = MeshKoreRestAgent(hub_url=HUB, agent_id=AGENT_ID, api_key=API_KEY)
    agent.register()

    online = agent.list_online()
    providers = [a["agent_id"] for a in online if a["agent_id"] != AGENT_ID]

    if not providers:
        print("No other agents online. Start some provider agents first.")
        return

    print(f"Found {len(providers)} provider(s): {providers}")

    task = {
        "type": "task_request",
        "text": "What is the capital of France?",
        "parameters": {"require_source": True},
    }

    for provider in providers:
        print(f"Sending task to {provider}...")
        agent.send(provider, task)

    print(f"\nWaiting for responses (30s timeout)...")
    results = {}
    deadline = time.time() + 30
    since_id = 0

    while time.time() < deadline and len(results) < len(providers):
        msgs, _receipts, since_id = agent.poll_peek(since_id)
        to_ack = []
        for msg in msgs:
            sender = msg.get("from", "?")
            payload = msg.get("payload", {})
            if payload.get("type") == "task_result" and sender in providers:
                results[sender] = payload
                print(f"  Got response from {sender}: {payload.get('text', '?')}")
                if "_id" in msg:
                    to_ack.append(msg["_id"])
        if to_ack:
            agent.ack(to_ack)
        time.sleep(2)

    print(f"\nCollected {len(results)}/{len(providers)} responses.")
    for aid, result in results.items():
        print(f"  {aid}: {result.get('text', '(no text)')}")

    agent.close()


if __name__ == "__main__":
    main()
