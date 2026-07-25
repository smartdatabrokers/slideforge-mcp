# SlideForge in n8n

**You don't need a community node.** n8n ships a first-party **MCP Client Tool**, and SlideForge is
an MCP server — so an n8n workflow can render decks today, on **n8n Cloud and self-hosted**, with
nothing to install.

Two ways in, depending on whether an LLM is in your loop:

| You want | Use | Node |
|---|---|---|
| An agent that decides what slides to make | **MCP Client Tool** | AI Agent + MCP Client Tool |
| A pipeline: rows in → deck out, no LLM | **HTTP Request** | HTTP Request |

## Get a key first (free)

**[slideforge.dev/sign-up](https://slideforge.dev/sign-up) — 60 free slides, no credit card, no
subscription.** Then create a key at [slideforge.dev/console/keys](https://slideforge.dev/console/keys).
One key works for MCP *and* REST. Discovery calls are free and never touch the 60, and a render that
isn't usable is never billed.

---

## Option A — MCP Client Tool (agent workflows)

Add an **AI Agent** node, then attach an **MCP Client Tool** sub-node:

| Field | Value |
|---|---|
| **Endpoint** | `https://api.slideforge.dev/mcp/` |
| **Server Transport** | **HTTP Streamable** ← **not SSE** |
| **Authentication** | Bearer |
| **Bearer Token** | your `sf_live_…` key |

> ⚠️ **Transport must be HTTP Streamable.** SlideForge serves Streamable HTTP only — there is no SSE
> endpoint, so picking *SSE* fails with a connection error. n8n's docs page still calls the field
> "SSE Endpoint"; the node supports both transports and the dropdown is what matters.

The agent then sees all 7 tools: `browse_catalog`, `plan_slide`, `create_slide`, `create_deck`,
`translate_deck`, `upload_asset`, `manage_account`.

**Verified** against production with the exact transport n8n uses
(`StreamableHTTPClientTransport` + a Bearer-injecting fetch, per n8n's `shared/utils.ts`):

```
connect       : OK
tools/list    : 7 tools
tools/call    : create_slide -> status=complete
content       : text + image (inline preview)
```

Because the MCP Client Tool is an **AI Agent sub-node**, it needs an AI Agent in the workflow. If you
just want deterministic "data → deck" with no model in the loop, use Option B.

---

## Option B — HTTP Request (deterministic pipelines)

No agent, no LLM on either side. One **HTTP Request** node:

| Field | Value |
|---|---|
| **Method** | `POST` |
| **URL** | `https://api.slideforge.dev/v1/render/intent/deck` |
| **Authentication** | Generic → Header Auth |
| **Header** | `Authorization` : `Bearer sf_live_…` |
| **Body Content Type** | JSON |

Body — your data, bound **verbatim** (no model draws the slide, so the numbers on the slide are the
numbers you sent):

```json
{
  "name": "Weekly metrics",
  "slides": [
    { "form": "hero_statement", "headline": "Weekly metrics", "context": "Week 30" },
    { "form": "kpi_metrics", "headline": "Where we landed",
      "data": { "metrics": [
        { "label": "Signups",    "value": "1,284", "delta_value": "+12%", "delta_tone": "good" },
        { "label": "Activation", "value": "38%",   "delta_value": "+4pp", "delta_tone": "good" }
      ] } }
  ]
}
```

*Copy that verbatim — it is the payload that was run against production for this doc
(`status=complete`, `fidelity=verbatim`, 2/2 slides). Two easy mistakes it avoids: the cover form is
**`hero_statement`**, not `title_slide` (which does not exist), and the metric field is
**`delta_value`**, not `delta`. Repeat content fields live under `data`.*

Response fields worth branching on:

| Field | Use it for |
|---|---|
| `job_id` | fetch the file: `GET /v1/jobs/{job_id}/pptx` with the same header |
| `status` | `complete` · `partial` · `rejected` |
| `fidelity` | `verbatim` · `mixed` · `ai_completed` — **gate on this** |
| `cost` | `0` when nothing usable was produced |

An **IF** node on `{{ $json.fidelity === "verbatim" }}` gives you a pipeline that refuses to email a
deck unless every number came through untouched. That check is the reason to use SlideForge in
automation rather than a prompt-to-deck tool.

To get the `.pptx` bytes, add a second HTTP Request node: `GET
https://api.slideforge.dev/v1/jobs/{{ $json.job_id }}/pptx`, same `Authorization` header, response
format **File**. Attach it to Gmail/Slack/Drive as usual.

Discover the forms and their exact field shapes at
[slideforge.dev/templates](https://slideforge.dev/templates), or `GET /v1/catalog/forms` (free).

---

## Troubleshooting

| Symptom | Cause |
|---|---|
| Connection error on the MCP node | Transport set to **SSE**. Switch to **HTTP Streamable** — we serve no SSE endpoint. |
| `401 unauthorized` | Bad or missing key. The message links to `/console/keys`; it is never reported as a balance problem. |
| `402` | Genuinely out of balance — distinct from auth. |
| `status: would_fabricate`, `cost: 0` | Your content was too thin for the form and we refused to invent data rather than bill you. Send typed `data`, or set `allow_fabrication: true` if you *want* illustrative filler. |

## See also

- [`langchain_slideforge.py`](langchain_slideforge.py) · [`llamaindex_slideforge.py`](llamaindex_slideforge.py)
- [GitHub Action](https://github.com/smartdatabrokers/slideforge-deck-action) · [GitLab CI/CD component](https://gitlab.com/explore/catalog/smartdatabrokers/slideforge)
- MCP docs: [slideforge.dev/docs/mcp](https://slideforge.dev/docs/mcp)
