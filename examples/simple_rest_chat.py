"""
Simple REST chat — Two agents talk without WebSocket.
Demonstrates the synchronous MeshKoreRestAgent.

Usage (two terminals):
    Terminal 1: python simple_rest_chat.py --agent-id agent-a --api-key dev-key-a --peer agent-b
    Terminal 2: python simple_rest_chat.py --agent-id agent-b --api-key dev-key-b --peer agent-a
"""

import argparse
import json
import os
import sys
import time
import threading

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "meshkore-sdk-python", "src"))
from meshkore import MeshKoreRestAgent

HUB = os.environ.get("MESHKORE_HUB", "https://hub.meshkore.com")


def poll_loop(agent: MeshKoreRestAgent):
    """Background thread that polls and prints incoming messages."""
    while True:
        try:
            messages = agent.poll()
            for msg in messages:
                sender = msg.get("from", "?")
                payload = msg.get("payload", {})
                text = payload.get("text", json.dumps(payload))
                print(f"\n  [{sender}]: {text}")
                print("You: ", end="", flush=True)
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

    # Start polling in background
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
