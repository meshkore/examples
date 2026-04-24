"""
Example: LangChain agent connected to MeshKore.

This agent receives task_requests from other agents on the mesh,
processes them using a LangChain LLM chain, and sends back results.

Requires: pip install langchain langchain-openai meshkore

This is a TEMPLATE — replace the LLM chain with your actual logic.
"""

import asyncio
import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sdk", "src"))
from meshkore import MeshKoreAgent

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("langchain-agent")

HUB_URL = os.environ.get("MESHKORE_HUB", "https://hub.meshkore.com")
AGENT_ID = os.environ.get("MESHKORE_AGENT_ID", "langchain-agent")
API_KEY = os.environ.get("MESHKORE_API_KEY", "your-api-key-here")


async def process_with_langchain(task: str) -> str:
    """
    Replace this with your actual LangChain logic.
    Example uses a simple echo — swap in your chain.
    """
    # from langchain_openai import ChatOpenAI
    # from langchain_core.prompts import ChatPromptTemplate
    #
    # llm = ChatOpenAI(model="gpt-4o-mini")
    # prompt = ChatPromptTemplate.from_messages([
    #     ("system", "You are a helpful assistant."),
    #     ("user", "{input}")
    # ])
    # chain = prompt | llm
    # result = await chain.ainvoke({"input": task})
    # return result.content

    # Placeholder — replace with real LangChain logic
    return f"[LangChain would process: {task}]"


async def main():
    agent = MeshKoreAgent(hub_url=HUB_URL, agent_id=AGENT_ID, api_key=API_KEY)
    await agent.connect()
    logger.info(f"LangChain agent online as {AGENT_ID}")

    async def handle_message(from_agent: str, payload: dict):
        msg_type = payload.get("type", "")
        logger.info(f"Received {msg_type} from {from_agent}")

        if msg_type == "task_request":
            task_text = payload.get("text", payload.get("description", ""))
            logger.info(f"Processing task: {task_text}")

            result = await process_with_langchain(task_text)

            await agent.send(from_agent, {
                "type": "task_result",
                "text": result,
                "original_task": task_text,
            })
            logger.info(f"Sent result to {from_agent}")

        elif msg_type == "ping":
            await agent.send(from_agent, {"type": "pong"})

        else:
            await agent.send(from_agent, {
                "type": "error",
                "text": f"Unknown message type: {msg_type}. Send a task_request.",
            })

    agent.on_message(handle_message)

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
