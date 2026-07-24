"""SlideForge from a LlamaIndex agent.

SlideForge is an MCP server, so LlamaIndex loads its tools directly via
`llama-index-tools-mcp` — no SlideForge SDK needed.

    pip install llama-index-tools-mcp
    export SLIDEFORGE_API_KEY=sf_live_...

Getting the key is free and takes ~30 seconds: sign up at https://slideforge.dev/sign-up
(60 free slides, no credit card, no subscription), then copy it from
https://slideforge.dev/console/keys. Discovery and dry_run are free; only real renders spend.

Run:  python llamaindex_slideforge.py

Verified 2026-07-24 against https://api.slideforge.dev/mcp/ with
llama-index-tools-mcp 0.4.8 / llama-index-core 0.14.23.
"""

import asyncio
import json
import os

from llama_index.tools.mcp import BasicMCPClient, aget_tools_from_mcp_url

SLIDEFORGE_MCP = "https://api.slideforge.dev/mcp/"
API_KEY = os.environ["SLIDEFORGE_API_KEY"]


async def slideforge_tools(allowed: list[str] | None = None):
    """All 7 SlideForge tools as LlamaIndex FunctionTools.

    Pass `allowed` to keep the agent's context small, e.g.
    ["browse_catalog", "plan_slide", "create_slide"].
    """
    client = BasicMCPClient(SLIDEFORGE_MCP, headers={"Authorization": f"Bearer {API_KEY}"})
    return await aget_tools_from_mcp_url(SLIDEFORGE_MCP, client=client, allowed_tools=allowed)


async def render_one_slide() -> None:
    """Call create_slide directly — no LLM required.

    Supplied values bind VERBATIM: the numbers below land on the slide exactly as
    written (no model in the render path). The response carries the honesty layer —
    status / fidelity / warnings — so an agent can trust the render or know why not.
    """
    tools = {t.metadata.name: t for t in await slideforge_tools()}

    result = await tools["create_slide"].acall(
        form="kpi_metrics",
        headline="Q3 at a glance",
        data={
            "metrics": [
                {"label": "Revenue", "value": "$12.4M", "delta": "+18% YoY"},
                {"label": "New clients", "value": "847"},
                {"label": "NPS", "value": "62"},
            ]
        },
    )

    # The MCP content blocks live on `.raw_output` (a JSON text block + an inline preview
    # image). `.content` is just a string repr — and printing the raw result dumps ~50KB
    # of base64 image, so pull the JSON block instead.
    blocks = result.raw_output.content
    text = next(b.text for b in blocks if getattr(b, "type", None) == "text")
    payload = json.loads(text)
    print(f"status={payload.get('status')}  fidelity={payload.get('fidelity')}")
    print(f"job_id={payload.get('job_id')}  form={payload.get('form')}/{payload.get('variant')}")
    print("Download the .pptx:")
    print("  curl -H 'Authorization: Bearer $SLIDEFORGE_API_KEY' \\")
    print(f"    -o slide.pptx https://api.slideforge.dev/v1/jobs/{payload.get('job_id')}/pptx")


async def agent_makes_a_slide() -> None:
    """The same tools inside a LlamaIndex agent (needs your own model key).

    `browse_catalog` and `plan_slide` are free, so the agent can discover the right
    layout before it renders.
    """
    from llama_index.core.agent.workflow import FunctionAgent
    from llama_index.llms.openai import OpenAI  # pip install llama-index-llms-openai

    agent = FunctionAgent(
        name="deck-builder",
        description="Builds consulting-grade slides with SlideForge.",
        system_prompt="You render slides with SlideForge. Supplied numbers must bind verbatim.",
        tools=await slideforge_tools(["browse_catalog", "plan_slide", "create_slide"]),
        llm=OpenAI(model="gpt-4.1"),
    )

    answer = await agent.run(
        "Make one slide: Q3 revenue $12.4M (+18% YoY), 847 new clients, NPS 62. "
        "Use a KPI layout and give me the download link."
    )
    print(answer)


if __name__ == "__main__":
    asyncio.run(render_one_slide())
    # asyncio.run(agent_makes_a_slide())   # needs OPENAI_API_KEY
