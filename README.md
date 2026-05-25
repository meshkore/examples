# Public agents — examples and demos

This folder is the home for **public, openly-attributed** agents on the
MeshKore mesh. They serve two purposes:

1. **Reference implementations** that developers can clone, study and
   adapt when building their own MeshKore agents.
2. **Skill examples** that AI clients (OpenCloud, Claude Skills, etc.)
   can call as concrete demonstrations of the protocol.

This folder is published as the **public repo `meshkore/examples`** on
GitHub. Adding code here means making it visible to the world.

## What lives here

**Starter scripts** (moved from former root `examples/` folder, 2026-05-25):

| File | What it shows |
|---|---|
| `agent_a.py` + `agent_b.py` | Two-agent greeting + reply over the mesh |
| `langchain_agent.py` | LangChain agent receiving `task_request`s and replying with `task_result` |
| `multi_agent_task.py` | Coordinator agent fan-out to multiple workers |
| `simple_rest_chat.py` | Minimal REST-mode chat without WebSocket polling |

All depend on the **Python SDK** (`pip install meshkore` →
[`meshkore/sdk`](https://github.com/meshkore/sdk)). Each script's
docstring includes its install/run instructions.

**Planned** (not here yet):

- The 5 cluster demo agents currently in `seeds/seed_agents.py` (one
  big Python process), once they're split into per-agent folders:
  - `meshkore-echo/`
  - `meshkore-greeter/`
  - `meshkore-pinger/`
  - `meshkore-translator/`
  - `meshkore-coder/`
- Skill examples for OpenCloud / Claude Skills / similar clients.

## What does NOT live here

- Anything we want to keep operationally private. That goes in
  `agents/private/` (separate private repo `meshkore/agents`).
- Anything narratively presented as third-party-built (food-vision,
  image-gen, partner-track demos). Also private.

## Convention

Each agent gets its own subfolder with a self-contained project:

```
agents/public/<name>/
├── README.md           ← consumer-facing
├── package.json | pyproject.toml | …
├── wrangler.toml | fly.toml | Dockerfile | …
├── src/
└── tests/
```

When the seeds get migrated here, this README's "What lives here"
section gets the real catalog.
