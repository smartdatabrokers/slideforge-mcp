"""SlideForge local stdio MCP server — a thin REST client over api.slideforge.dev.

This server holds ZERO engine IP. It bakes the 7 SlideForge tool schemas in locally
(from ``contract/tools_list.prod.json``, captured verbatim from the production served
surface) and forwards each call to the REST tool-dispatch endpoint
(``POST /v1/tools/{name}``) authenticated with a SlideForge API key.

Why a local server (vs. the hosted remote MCP endpoint): registries like Glama build a
Dockerfile, run it in a keyless sandbox, and score the tool schemas they see via
``tools/list``. Because the schemas are baked in here, that works with no network and no
key. Actual tool *calls* forward to the REST API and require ``SLIDEFORGE_API_KEY``.

Most agents should use the hosted remote server directly
(``https://api.slideforge.dev/mcp/``, OAuth 2.1 or API key) — no install. This wrapper is
for clients that boot MCP servers from a container/stdio and for offline schema discovery.
"""
from __future__ import annotations

import inspect
import json
import os
from importlib import resources
from typing import Any

import httpx
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.tools import Tool, ToolResult
from mcp.types import ToolAnnotations

API_BASE = os.environ.get("SLIDEFORGE_API_BASE", "https://api.slideforge.dev").rstrip("/")
API_KEY = os.environ.get("SLIDEFORGE_API_KEY", "")

_JSON_PY: dict[str, Any] = {
    "string": str,
    "integer": int,
    "number": float,
    "boolean": bool,
    "object": dict,
    "array": list,
}

mcp = FastMCP(
    "slideforge",
    instructions=(
        "SlideForge turns typed slide intents into deterministic, fully editable PowerPoint. "
        "Discover with browse_catalog / plan_slide (free), then create_slide / create_deck. "
        "Set SLIDEFORGE_API_KEY to run tool calls; get a key at https://slideforge.dev."
    ),
)

_client: httpx.AsyncClient | None = None


def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            base_url=API_BASE,
            timeout=httpx.Timeout(120.0, connect=10.0),
            headers={"X-API-Key": API_KEY} if API_KEY else {},
        )
    return _client


def _load_contract() -> list[dict]:
    raw = resources.files("slideforge_mcp.contract").joinpath("tools_list.prod.json").read_text("utf-8")
    return json.loads(raw)["tools"]


def _make_tool(defn: dict) -> Tool:
    """Build a forwarding Tool that advertises the prod schema verbatim.

    The function signature is synthesised from the schema's top-level properties so FastMCP
    accepts it (it rejects ``**kwargs`` tools), then ``parameters`` is overridden with the
    exact prod inputSchema so ``tools/list`` is byte-identical to production.
    """
    name = defn["name"]
    schema = defn["inputSchema"]
    props = schema.get("properties", {})

    params: list[inspect.Parameter] = []
    annotations: dict[str, Any] = {}
    for pname, pdef in props.items():
        pytype = _JSON_PY.get(pdef.get("type"), Any)
        opt = pytype | None
        annotations[pname] = opt
        params.append(
            inspect.Parameter(pname, inspect.Parameter.KEYWORD_ONLY, default=None, annotation=opt)
        )

    async def _forward(**kwargs: Any) -> ToolResult:
        payload = {k: v for k, v in kwargs.items() if v is not None}
        return await _dispatch(name, payload)

    _forward.__signature__ = inspect.Signature(params)  # type: ignore[attr-defined]
    _forward.__annotations__ = {**annotations, "return": ToolResult}
    _forward.__name__ = name
    _forward.__doc__ = defn.get("description", "")

    tool = Tool.from_function(_forward, name=name, description=defn.get("description"))
    update: dict[str, Any] = {"parameters": schema}
    if defn.get("title"):
        update["title"] = defn["title"]
    if defn.get("annotations"):
        update["annotations"] = ToolAnnotations.model_validate(defn["annotations"])
    return tool.model_copy(update=update)


async def _dispatch(name: str, payload: dict) -> ToolResult:
    if not API_KEY:
        raise ToolError(
            "SLIDEFORGE_API_KEY is not set. Get a key at https://slideforge.dev and set it in "
            "the server's environment."
        )
    try:
        resp = await _get_client().post(f"/v1/tools/{name}", json=payload)
    except httpx.TimeoutException as e:
        raise ToolError(f"SlideForge API timed out calling {name}: {e}") from e
    except httpx.HTTPError as e:
        raise ToolError(f"Network error calling SlideForge API {name}: {e}") from e

    if resp.status_code >= 400:
        try:
            body = resp.json()
        except ValueError:
            body = {"raw": resp.text[:2000]}
        raise ToolError(f"SlideForge API {resp.status_code} on {name}: {json.dumps(body)}")

    data = resp.json()
    content = data.get("content") or []
    structured = data.get("structuredContent")
    if structured is None:
        # Mirror the /mcp/ path's lift: surface a JSON text block as structured output.
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text = block.get("text", "")
                if text[:1] in "{[":
                    try:
                        structured = json.loads(text)
                    except (json.JSONDecodeError, ValueError):
                        pass
                break
    return ToolResult(content=content, structured_content=structured, is_error=bool(data.get("isError")))


for _defn in _load_contract():
    mcp.add_tool(_make_tool(_defn))


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
