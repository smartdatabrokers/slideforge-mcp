"""Refresh the committed tool-surface snapshot from the PROD served MCP surface.

The wrapper must advertise exactly what production serves — that is what makes it scoreable in a
keyless registry sandbox. `tests/test_contract_parity.py` is the drift detector; this is the fix.

Run it when the live parity test fails, then bump the version + CHANGELOG and cut a release.

    python scripts/refresh_contract.py            # writes the snapshot, prints a diff summary
    python scripts/refresh_contract.py --check    # report drift, write nothing (exit 1 if drift)

**Encoding matters here.** The snapshot is written UTF-8 explicitly with `ensure_ascii=False`: tool
descriptions contain en/em dashes and arrows, and letting Windows pick cp1252 silently mojibakes
them into a snapshot that then fails parity for a reason that looks like a surface change.
"""
import argparse
import io
import json
import sys
from pathlib import Path

import httpx

PROD = "https://api.slideforge.dev/mcp/"
SNAPSHOT = Path(__file__).resolve().parents[1] / "src" / "slideforge_mcp" / "contract" / "tools_list.prod.json"


def fetch_prod_tools() -> list[dict]:
    r = httpx.post(
        PROD,
        headers={"Accept": "application/json, text/event-stream"},
        json={"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
        timeout=30,
    )
    r.raise_for_status()
    # Explicit UTF-8: httpx guesses from headers, and a wrong guess corrupts the dashes.
    payload = json.loads(r.content.decode("utf-8"))
    return payload["result"]["tools"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report drift without writing")
    ap.add_argument("--captured", default=None, help="date stamp for _captured (default: today UTC)")
    args = ap.parse_args()

    current = json.loads(io.open(SNAPSHOT, encoding="utf-8").read())
    prod_tools = fetch_prod_tools()

    old = {t["name"]: t for t in current["tools"]}
    new = {t["name"]: t for t in prod_tools}

    added, removed = sorted(set(new) - set(old)), sorted(set(old) - set(new))
    changed = [n for n in sorted(set(old) & set(new)) if old[n] != new[n]]

    if added:
        print(f"  + tools added:   {added}")
    if removed:
        print(f"  - tools REMOVED: {removed}   <-- breaking for anyone pinned to this wrapper")
    for name in changed:
        o, n = old[name], new[name]
        fields = [k for k in set(o) | set(n) if o.get(k) != n.get(k)]
        detail = []
        if "inputSchema" in fields:
            op = set(o.get("inputSchema", {}).get("properties", {}))
            np_ = set(n.get("inputSchema", {}).get("properties", {}))
            if np_ - op:
                detail.append(f"params added {sorted(np_ - op)}")
            if op - np_:
                detail.append(f"params REMOVED {sorted(op - np_)}")
            touched = [k for k in op & np_
                       if o["inputSchema"]["properties"][k] != n["inputSchema"]["properties"][k]]
            if touched:
                detail.append(f"param descriptions {sorted(touched)}")
        if "description" in fields:
            detail.append(f"description {len(o.get('description') or '')} -> {len(n.get('description') or '')} chars")
        print(f"  ~ {name}: {'; '.join(detail) or fields}")

    if not (added or removed or changed):
        print("  no drift — snapshot already matches prod")
        return 0
    if args.check:
        print("\ndrift found (--check: nothing written)")
        return 1

    if args.captured:
        stamp = args.captured
    else:
        from datetime import datetime, timezone
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    out = {**current, "_captured": stamp, "tools": prod_tools}
    io.open(SNAPSHOT, "w", encoding="utf-8", newline="\n").write(
        json.dumps(out, indent=2, ensure_ascii=False)
    )
    print(f"\nwrote {SNAPSHOT.name} (_captured={stamp}). Bump the version + CHANGELOG, then release.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
