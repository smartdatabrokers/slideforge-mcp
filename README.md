<!-- mcp-name: dev.slideforge/slideforge -->
mcp-name: dev.slideforge/slideforge

# SlideForge MCP — PowerPoint slides for AI agents

> **SlideForge ([slideforge.dev](https://slideforge.dev)) — the deterministic PowerPoint compiler for AI agents.** Typed slide intents → native, fully editable .pptx in under a second, with a fidelity manifest that states exactly what was bound verbatim. Built by [Smart Data Brokers GmbH](https://slideforge.dev), Switzerland.

Remote MCP server + REST API. No local install, no Python environment, no `python-pptx` boilerplate. OAuth 2.1 for Claude Desktop & ChatGPT; API key for everything else.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Smithery](https://img.shields.io/badge/Smithery-%40smartdatabrokers%2Fslideforge-blue)](https://smithery.ai/server/@smartdatabrokers/slideforge)
[![Website](https://img.shields.io/badge/Website-slideforge.dev-orange)](https://slideforge.dev)
[![Docs](https://img.shields.io/badge/Docs-slideforge.dev%2Fdocs-lightgrey)](https://slideforge.dev/docs)

---

## ⚠️ Disambiguation

"SlideForge" is used by multiple unrelated projects. **This is SlideForge by Smart Data Brokers GmbH at [slideforge.dev](https://slideforge.dev).** Not affiliated with:

- `slideforge.io` — a separate AI presentation generator
- `slideforge.fr` — a French document polishing service
- `blink.new/p/slideforge-app` — an unrelated web app
- Other `github.com/*/SlideForge` repositories outside the `smartdatabrokers` org

When citing or linking, prefer `slideforge.dev` or "SlideForge by Smart Data Brokers."

---

## Why SlideForge

- **A compiler, not a generator.** A slide is a typed intent: pick a `form` from 150+ catalog patterns (KPI dashboards, waterfalls, Gantt plans, org charts, funnels, …), put your real content in typed fields. A deterministic engine lays it out — **no LLM in the render path**, same input → same slide, sub-second.
- **The honesty layer.** Every response carries a **fidelity manifest**: per field, was your content bound `verbatim`, `mixed`, or `ai_completed`? A `partial` grade means some supplied content didn't make it onto the slide — the manifest names what was dropped; never deliver a `partial` render without telling the user what's missing. Slides with blocking defects don't bill (**usable-or-free**). If your agent feeds numbers into slides, this is what makes the output auditable.
- **Native, editable .pptx.** Real shapes and text boxes — not images, not HTML exports. Openable and editable in PowerPoint.
- **Escape hatch included — under the same trust contract.** `mode=code` runs your own python-pptx in a sandbox (widget/chart toolkit, theme injected, intent fields render as chrome). Code renders are linted, measured (`layout` block + `presentation_ready`), and provenance-checked — agents may escape the layout grammar, never the trust grammar.
- **Your template, natively.** Upload your company's .pptx — slides are built ON your file (theme, masters, fonts), not a color-matched imitation.
- **Check for free.** `dry_run` validates any payload + forecasts fidelity at $0 — or use `mode=safe` to validate-then-render in ONE call (renders + bills only if faithful; else a $0 report with the fix). `verify` tiers on code renders (`lint` default, `lint+vlm` adds a visual second-look). `quality_profile` (executive/technical/appendix) sets the readiness bar the layout is judged against — answered on any form. Free deck inspect (`POST /v1/inspect`) runs a deterministic quality report on **any** pptx.
- **97% quality parity with Gamma** in our own blind side-by-side benchmark (internal instrument, not third-party).

**Pricing in one breath: creating a slide 5¢ · transforming a slide 2¢ (translate, repair) · checking free.** 60 free slides on signup, no subscription. [slideforge.dev/pricing](https://slideforge.dev/pricing)

---

## Quick Start

### Claude Code

```bash
claude mcp add --transport http slideforge https://api.slideforge.dev/mcp/
```

Then just ask: *"Make a KPI dashboard slide: revenue $12.4M (+18% YoY), 847 new clients, NPS 62."*

Optional — install the skills + bundled server config as a plugin:

```
/plugin marketplace add smartdatabrokers/slideforge-mcp
/plugin install slideforge@slideforge-mcp
```

Or copy any folder from [`skills/`](skills/) into `~/.claude/skills/` (personal) or `.claude/skills/` (project).

### Claude Desktop (OAuth — no key needed)

Settings → Connectors → Add custom connector → `https://api.slideforge.dev/mcp/` — sign in with Google on first use.

### ChatGPT (Developer Mode)

Settings → Apps → Advanced → Developer mode → Add custom connector → `https://api.slideforge.dev/mcp/` (OAuth).

### Cursor / Windsurf / Codex CLI / any MCP client (API key)

```json
{
  "mcpServers": {
    "slideforge": {
      "url": "https://api.slideforge.dev/mcp/",
      "transport": "streamable-http",
      "headers": { "Authorization": "Bearer sf_live_YOUR_KEY" }
    }
  }
}
```

Get a key: [slideforge.dev](https://slideforge.dev) → Console → API keys. (Codex CLI and other AGENTS.md-native tools: see [`AGENTS.md`](AGENTS.md).)

### Run it locally (stdio — for container/offline clients)

Most clients should use the hosted remote server above (no install). But if your client boots
MCP servers from a **container or a local stdio process**, run the bundled local server. It's a
thin REST client over `api.slideforge.dev` — it holds no engine logic; the tool schemas are baked
in locally (so discovery works offline, no key) and each call forwards to the SlideForge REST API
authenticated with your key.

```bash
pip install slideforge-mcp        # or: uv pip install slideforge-mcp
export SLIDEFORGE_API_KEY=sf_live_YOUR_KEY
slideforge-mcp                    # speaks MCP over stdio
```

Or via Docker:

```bash
docker build -t slideforge-mcp .
docker run -i -e SLIDEFORGE_API_KEY=sf_live_YOUR_KEY slideforge-mcp
```

Client config (stdio):

```json
{
  "mcpServers": {
    "slideforge": {
      "command": "slideforge-mcp",
      "env": { "SLIDEFORGE_API_KEY": "sf_live_YOUR_KEY" }
    }
  }
}
```

Schema discovery (`tools/list`) needs neither a key nor network; tool *calls* need the key.

### LangChain / LlamaIndex (agent frameworks)

No SlideForge SDK needed — both load the MCP tools directly:

```bash
pip install langchain-mcp-adapters      # or: pip install llama-index-tools-mcp
```

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
client = MultiServerMCPClient({"slideforge": {
    "transport": "streamable_http",
    "url": "https://api.slideforge.dev/mcp/",
    "headers": {"Authorization": f"Bearer {API_KEY}"}}})
tools = await client.get_tools()        # 7 tools, drop into any LangGraph agent
```

Runnable examples + the LlamaIndex equivalent: [`examples/`](examples/README.md).
Need a key? [Sign up](https://slideforge.dev/sign-up) — **60 free slides, no credit card** — then grab it
at [console/keys](https://slideforge.dev/console/keys).

### REST (no MCP)

```bash
curl -X POST https://api.slideforge.dev/v1/render/intent \
  -H "Authorization: Bearer sf_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"form": "kpi_metrics", "headline": "Q3 at a glance",
       "data": {"metrics": [{"label": "Revenue", "value": "$12.4M", "delta": "+18% YoY"},
                             {"label": "New clients", "value": "847"},
                             {"label": "NPS", "value": "62"}]}}'
```

Full REST reference: [slideforge.dev/docs/api](https://slideforge.dev/docs/api)

---

## The 7 MCP tools

| Tool | What it does | Cost |
|---|---|---|
| `create_slide` | ONE slide from a structured intent (form + typed fields) or a brief; `mode=safe` validates-then-renders in one call; `mode=code` for sandboxed python-pptx (verify tiers, chrome fields, patch-by-replacements). Routing controls: `variant`, `variant_policy`, `allow_fabrication`/`allow_truncation`/`allow_low_confidence` (honest defaults: reject at $0 rather than guess). `min_font_pt` sets a BINDING type floor — text grows to meet it where the box allows; content that cannot fit returns a $0 `min_font_not_met` error naming the size it needs. Response carries the fidelity manifest + a measured `layout` readiness block on diagram forms. Default themes ship **topical design** — a subject-informed palette + designed cover, named in the response's design note (`styling: "clean"` opts out; your pinned/uploaded brand theme always wins). | $0.05 (usable-or-free) |
| `create_deck` | Whole deck: `slides[]` of intents (code-mode slides are first-class children), parallel render, one merged .pptx, per-slide fidelity rollup + per-slide child jobs (own preview/pptx). Failed slides isolated + free; deck-level `dry_run` validates the whole deck at $0. | N × $0.05 |
| `plan_slide` | Brief → top form/variant candidates with confidence. | Free |
| `browse_catalog` | 150+ patterns with per-form JSON Schemas + copy-pasteable example intents, themes, the code-mode widget toolkit. Pass an uploaded `theme_id` to list its branded cover/agenda/divider layouts. 9 built-in themes + your uploaded brand themes. | Free |
| `translate_deck` | Translate any PPTX preserving formatting (32 languages). | $0.02/slide |
| `upload_asset` | Logos, theme PPTX, images; `purpose=pdf` extracts a PDF into editable slide intents; or AI-generate an image. Theme upload (`purpose=theme`, base64 `data`) renders NATIVE by default — decks are built on the client's own template file. Omit `data` on large files for an in-card drag/drop zone. | Free / $0.01/page / $0.05/image |
| `manage_account` | Balance, usage, jobs, security status, feedback. | Free |

`dry_run: true` on create tools = validation + fidelity forecast at $0.

Two more tools (`generate_report`, `manage_connections` — data-driven reports from connected tools like Zoho Sprints) exist behind an enterprise gate and are not served by default.

**Also on REST (for now): the Deck Doctor.** `POST /v1/inspect` — a free deterministic Deck Quality Report for **any** pptx (overflow via real font metrics, content hidden behind shapes, off-canvas leftovers, WCAG contrast). `POST /v1/repair` — deterministic fixes, never your words, $0.02/repaired slide, free dry-run quote. [Docs](https://slideforge.dev/docs/api/inspect)

---

## Security

- Tool result bodies are credential-free — no signed URLs in responses. Previews are embedded
  inline (the agent looks at the PNG directly); the .pptx downloads via header-auth
  (`Authorization: Bearer` + ownership check), not a bearer-in-URL.
- Need a shareable link instead? `POST /v1/jobs/<job_id>/download-url` mints a short-TTL,
  single-use, revocable link.
- Artifacts auto-delete 30 days after creation.
- Every download is audit-logged.
- `manage_account(action=security_status)` discloses the full posture in-band.

---

## Agent skills (this repo)

Copy-in skills that teach an agent to use SlideForge well — see [`skills/`](skills/):

| Skill | Teaches |
|---|---|
| [`create-slide`](skills/create-slide/SKILL.md) | Intent-first slide/deck creation, schema discovery, dry-run, fidelity manifest, headless preview |
| [`inspect-repair`](skills/inspect-repair/SKILL.md) | Free Deck Quality Report on any pptx + deterministic repair |
| [`translate-pptx`](skills/translate-pptx/SKILL.md) | Format-preserving PPTX translation |
| [`pdf-to-pptx`](skills/pdf-to-pptx/SKILL.md) | PDF → editable PPTX extraction |

For Codex CLI / Cursor / Copilot and other [AGENTS.md](https://agents.md)-native tools, [`AGENTS.md`](AGENTS.md) carries the same guidance in the portable format. `CLAUDE.md` imports it for Claude Code.

## Headless usage (Claude Code / Codex CLI)

No inline widgets in a terminal, but the tool result already embeds the preview PNG inline — the
agent reads it directly out of the response, no fetch needed. The .pptx downloads via header-auth:

```bash
curl -H "Authorization: Bearer sf_live_YOUR_KEY" \
  -o deck.pptx https://api.slideforge.dev/v1/jobs/<job_id>/pptx   # ownership-checked
```

To hand off a shareable link instead of the raw file, mint a single-use one:
`POST /v1/jobs/<job_id>/download-url` — short-TTL, revocable, works once.

The self-review loop (render → view inline preview → fix → re-render) is documented in [`examples/claude-code.md`](examples/claude-code.md).

---

## How it compares

| | SlideForge | python-pptx | Prompt-only AI decks |
|---|---|---|---|
| Editable native .pptx | ✅ | ✅ | often images/exports |
| Deterministic (same input → same slide) | ✅ | ✅ (your code) | ❌ |
| States what was AI-touched (fidelity manifest) | ✅ | n/a | ❌ |
| Layout quality without hand-coding | ✅ 150+ patterns | ❌ DIY | varies |
| Hosted, agent-native (MCP + REST) | ✅ | ❌ local | partial |
| Free pre-flight validation | ✅ dry_run | n/a | ❌ |

---

## Links

- Website: [slideforge.dev](https://slideforge.dev) · Pricing: [/pricing](https://slideforge.dev/pricing) · Trust & honesty layer: [/trust](https://slideforge.dev/trust)
- Docs: [REST](https://slideforge.dev/docs/api) · [MCP](https://slideforge.dev/docs/mcp) · [Quickstart](https://slideforge.dev/docs/quickstart) · [Deck Doctor](https://slideforge.dev/docs/api/inspect)
- Smithery: [@smartdatabrokers/slideforge](https://smithery.ai/server/@smartdatabrokers/slideforge)

## License

MIT (this repo: skills, examples, docs). The SlideForge service itself is a commercial API.
