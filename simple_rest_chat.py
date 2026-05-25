"""
Simple REST chat — Two agents talk without WebSocket.
Uses PEEK polling so messages survive crashes and restarts.

Usage (two terminals):
    Terminal 1: python simple_rest_chat.py --agent-id agent-a --api-key dev-key-a --peer agent-b
    Terminal 2: python simple_rest_chat.py --agent-id agent-b --api-key dev-key-b --peer agent-a

Or register first via the open endpoint:
    curl -X POST https://hub.meshkore.com/join/open \\
      -H "Content-Type: application/json" \\
      -d '{"agent_id":"agent-a","description":"test"}'
    # → returns api_key — use it with --api-key
"""

import argparse
import json
import os
import sys
import time
import threading

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sdk", "src"))
from meshkore import MeshKoreRestAgent

HUB = os.environ.get("MESHKORE_HUB", "https://hub.meshkore.com")


def poll_loop(agent: MeshKoreRestAgent):
    """Background thread — peek-polls and prints incoming messages."""
    since_id = 0
    while True:
        try:
            msgs, _receipts, since_id = agent.poll_peek(since_id)
            for msg in msgs:
                sender = msg.get("from", "?")
                payload = msg.get("payload", {})
                text = payload.get("text", json.dumps(payload))
                print(f"\n  [{sender}]: {text}")
                print("You: ", end="", flush=True)
            if msgs:
                agent.ack([m["_id"] for m in msgs if "_id" in m])
        except Exception:
            pass
        time.sleep(3)


def main():
    parser = argparse.ArgumentParser(description="MeshKore REST chat")
    parser.add_argument("--agent-id", default="agent-a")
    parser.add_argument("--api-key", default="dev-key-a")
    parser.add_argument("--peer", default="agent-b")
    args = parser.parse_args()

    agent = MeshKoreRestAgent(hub_url=HUB, agent_id=args.agent_id, api_key=args.api_key)
    agent.register()
    print(f"Connected as {args.agent_id}. Chatting with {args.peer}.")
    print("Type your messages (Ctrl+C to quit):\n")

    t = threading.Thread(target=poll_loop, args=(agent,), daemon=True)
    t.start()

    try:
        while True:
            text = input("You: ")
            if text.strip():
                agent.send(args.peer, {"type": "chat", "text": text})
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")
        agent.close()


if __name__ == "__main__":
    main()
