# Use SlideForge from your agent framework

**SlideForge is an MCP server, so LangChain and LlamaIndex load its tools directly — you don't need a
SlideForge SDK.** Point the framework's MCP adapter at `https://api.slideforge.dev/mcp/` with your API
key and all 7 tools become agent tools. Your agent's numbers bind **verbatim** (no model in the render
path), and every response carries `status` / `fidelity` / `warnings` so the agent can trust the render —
or know exactly why not.

Runnable files: [`langchain_slideforge.py`](langchain_slideforge.py) · [`llamaindex_slideforge.py`](llamaindex_slideforge.py)
Both verified end-to-end against production on 2026-07-24 (real `.pptx` out).

```bash
export SLIDEFORGE_API_KEY=sf_live_...   # https://slideforge.dev -> Console -> API keys
```

## LangChain / LangGraph

```bash
pip install langchain-mcp-adapters
```

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient({
    "slideforge": {
        "transport": "streamable_http",
        "url": "https://api.slideforge.dev/mcp/",
        "headers": {"Authorization": f"Bearer {API_KEY}"},
    }
})
tools = await client.get_tools()          # 7 SlideForge tools, ready for any agent

# ...or use them directly, no LLM required:
result = await {t.name: t for t in tools}["create_slide"].ainvoke({
    "form": "kpi_metrics",
    "headline": "Q3 at a glance",
    "data": {"metrics": [
        {"label": "Revenue", "value": "$12.4M", "delta": "+18% YoY"},
        {"label": "New clients", "value": "847"},
        {"label": "NPS", "value": "62"},
    ]},
})
```

Drop `tools` straight into a LangGraph agent:

```python
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(model, tools)
```

## LlamaIndex

```bash
pip install llama-index-tools-mcp
```

```python
from llama_index.tools.mcp import BasicMCPClient, aget_tools_from_mcp_url

URL = "https://api.slideforge.dev/mcp/"
client = BasicMCPClient(URL, headers={"Authorization": f"Bearer {API_KEY}"})

tools = await aget_tools_from_mcp_url(URL, client=client)
# keep the agent's context small — load only what you need:
tools = await aget_tools_from_mcp_url(
    URL, client=client, allowed_tools=["browse_catalog", "plan_slide", "create_slide"]
)
```

Then hand `tools` to a `FunctionAgent` (see the example file).

## What you get

| Tool | Use | Cost |
|---|---|---|
| `create_slide` | One slide from a typed intent (`form` + fields) or a brief | $0.05 |
| `create_deck` | Whole deck, rendered in parallel | N × $0.05 |
| `plan_slide` | Brief → best form/variant, creates nothing | **Free** |
| `browse_catalog` | 150+ layouts + their exact payload schemas | **Free** |
| `translate_deck` · `upload_asset` · `manage_account` | Localize · assets/PDF→deck · wallet & jobs | varies |

**Let the agent discover the layout:** `plan_slide` and `browse_catalog` are free, so an agent can find
the right form before it spends anything. `dry_run: true` validates a payload at $0.

## Reading the response

Every render returns the honesty layer — build your agent's control flow on it, not on a screenshot:

```json
{"job_id": "...", "status": "complete", "fidelity": "verbatim",
 "pptx_available": true, "editability": {"editable_percentage": 100}}
```

- `fidelity: verbatim` — your values were placed exactly as supplied.
- `status: rejected` with `errors[]` — nothing rendered and **nothing billed** (e.g. too few data
  points for the form). Fix the payload and retry.
- Download: `GET /v1/jobs/{job_id}/pptx` with the same `Authorization` header.

## Notes

- **No SlideForge SDK.** These adapters talk to the MCP server directly; there's nothing extra to keep
  in sync. `tools/list` is unauthenticated, tool *calls* need the key.
- Prefer a local stdio process? `pip install slideforge-mcp` (see the [repo README](../README.md)).
- Full tool reference: [slideforge.dev/docs/mcp](https://slideforge.dev/docs/mcp).
