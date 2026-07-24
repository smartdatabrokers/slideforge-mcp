"""SlideForge from a LangChain / LangGraph agent.

SlideForge is an MCP server, so LangChain loads its tools directly via
`langchain-mcp-adapters` — no SlideForge SDK needed.

    pip install langchain-mcp-adapters
    export SLIDEFORGE_API_KEY=sf_live_...

Getting the key is free and takes ~30 seconds: sign up at https://slideforge.dev/sign-up
(60 free slides, no credit card, no subscription), then copy it from
https://slideforge.dev/console/keys. Discovery and dry_run are free; only real renders spend.

Run:  python langchain_slideforge.py

Verified 2026-07-24 against https://api.slideforge.dev/mcp/ with
langchain-mcp-adapters 0.3.0 / langchain-core 1.5.1 / langgraph 1.2.9.
"""

import asyncio
import json
import os

from langchain_mcp_adapters.client import MultiServerMCPClient

SLIDEFORGE_MCP = "https://api.slideforge.dev/mcp/"
API_KEY = os.environ["SLIDEFORGE_API_KEY"]


def slideforge_client() -> MultiServerMCPClient:
    """All 7 SlideForge tools, ready for any LangChain/LangGraph agent."""
    return MultiServerMCPClient(
        {
            "slideforge": {
                "transport": "streamable_http",
                "url": SLIDEFORGE_MCP,
                "headers": {"Authorization": f"Bearer {API_KEY}"},
            }
        }
    )


async def render_one_slide() -> None:
    """Call create_slide directly — no LLM required.

    Supplied values bind VERBATIM: the numbers below land on the slide exactly as
    written (no model in the render path). The response carries the honesty layer —
    status / fidelity / warnings — so an agent can trust the render or know why not.
    """
    tools = {t.name: t for t in await slideforge_client().get_tools()}

    result = await tools["create_slide"].ainvoke(
        {
            "form": "kpi_metrics",
            "headline": "Q3 at a glance",
            "data": {
                "metrics": [
                    {"label": "Revenue", "value": "$12.4M", "delta": "+18% YoY"},
                    {"label": "New clients", "value": "847"},
                    {"label": "NPS", "value": "62"},
                ]
            },
        }
    )

    payload = json.loads(result[0]["text"]) if isinstance(result, list) else result
    print(f"status={payload.get('status')}  fidelity={payload.get('fidelity')}")
    print(f"job_id={payload.get('job_id')}  form={payload.get('form')}/{payload.get('variant')}")
    print("Download the .pptx:")
    print(f"  curl -H 'Authorization: Bearer $SLIDEFORGE_API_KEY' \\")
    print(f"    -o slide.pptx https://api.slideforge.dev/v1/jobs/{payload.get('job_id')}/pptx")


async def agent_makes_a_slide() -> None:
    """The same tools inside a LangGraph agent (needs your own model key).

    Let the agent pick the layout: `browse_catalog` and `plan_slide` are free, so it can
    discover the right form before it renders.
    """
    from langchain_openai import ChatOpenAI  # or any LangChain chat model
    from langgraph.prebuilt import create_react_agent

    tools = await slideforge_client().get_tools()
    agent = create_react_agent(ChatOpenAI(model="gpt-4.1"), tools)

    answer = await agent.ainvoke(
        {
            "messages": [
                (
                    "user",
                    "Make one slide: Q3 revenue $12.4M (+18% YoY), 847 new clients, NPS 62. "
                    "Use a KPI layout and give me the download link.",
                )
            ]
        }
    )
    print(answer["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(render_one_slide())
    # asyncio.run(agent_makes_a_slide())   # needs OPENAI_API_KEY
