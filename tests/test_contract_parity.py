"""Contract parity — the wrapper must advertise EXACTLY the production tool surface.

`test_local_tools_match_contract` runs offline (no key, no network): it proves the baked-in
schemas the wrapper serves via tools/list are byte-identical to the committed contract
snapshot. This is what makes the server scoreable in a keyless registry sandbox.

`test_contract_matches_prod` is the drift detector: it fetches the live production
tools/list and diffs it against the committed snapshot. It only runs when
SLIDEFORGE_LIVE_PARITY=1 (needs network). When it fails, regenerate the snapshot from prod
and cut a new release.
"""
import asyncio
import json
import os
from importlib import resources

import httpx
import pytest


def _contract() -> list[dict]:
    raw = resources.files("slideforge_mcp.contract").joinpath("tools_list.prod.json").read_text("utf-8")
    return json.loads(raw)["tools"]


def _served() -> list[dict]:
    from slideforge_mcp.server import mcp

    tools = asyncio.run(mcp.list_tools())
    out = []
    for t in tools:
        w = t.to_mcp_tool()
        out.append(
            {
                "name": w.name,
                "title": w.title,
                "description": w.description,
                "inputSchema": w.inputSchema,
                "annotations": w.annotations.model_dump(exclude_none=True) if w.annotations else None,
            }
        )
    return out


def test_local_tools_match_contract():
    contract = {t["name"]: t for t in _contract()}
    served = {t["name"]: t for t in _served()}

    assert set(served) == set(contract), "tool NAME set drifted from contract"

    for name, c in contract.items():
        s = served[name]
        assert s["inputSchema"] == c["inputSchema"], f"{name}: inputSchema drifted"
        assert s["description"] == c.get("description"), f"{name}: description drifted"
        assert s["title"] == c.get("title"), f"{name}: title drifted"
        assert s["annotations"] == c.get("annotations"), f"{name}: annotations drifted"


@pytest.mark.skipif(os.environ.get("SLIDEFORGE_LIVE_PARITY") != "1", reason="network drift check; set SLIDEFORGE_LIVE_PARITY=1")
def test_contract_matches_prod():
    base = os.environ.get("SLIDEFORGE_API_BASE", "https://api.slideforge.dev").rstrip("/")
    r = httpx.post(
        f"{base}/mcp/",
        headers={"Accept": "application/json, text/event-stream"},
        json={"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
        timeout=30,
    )
    r.raise_for_status()
    prod = {t["name"]: t for t in r.json()["result"]["tools"]}
    contract = {t["name"]: t for t in _contract()}
    assert set(prod) == set(contract), "prod tool set differs from committed contract — regenerate + release"
    for name, c in contract.items():
        assert prod[name]["inputSchema"] == c["inputSchema"], f"{name}: prod inputSchema differs — regenerate + release"
