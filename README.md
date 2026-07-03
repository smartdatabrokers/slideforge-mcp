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
- **The honesty layer.** Every response carries a **fidelity manifest**: per field, was your content bound `verbatim`, `mixed`, or `ai_completed`? Slides with blocking defects don't bill (**usable-or-free**). If your agent feeds numbers into slides, this is what makes the output auditable.
- **Native, editable .pptx.** Real shapes and text boxes — not images, not HTML exports. Openable and editable in PowerPoint.
- **Escape hatch included.** `mode=code` runs your own python-pptx in a sandbox (with a widget/chart toolkit) when the catalog can't express your layout.
- **Check for free.** `dry_run` validates any payload + forecasts fidelity at $0. Free deck inspect (`POST /v1/inspect`) runs a deterministic quality report on **any** pptx.

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

## The 9 MCP tools

| Tool | What it does | Cost |
|---|---|---|
| `create_slide` | ONE slide from a structured intent (form + typed fields) or a brief; `mode=code` for sandboxed python-pptx. Response carries the fidelity manifest. | $0.05 (usable-or-free) |
| `create_deck` | Whole deck: `slides[]` of intents, parallel render, one merged .pptx, per-slide fidelity rollup. Failed slides isolated + free. | N × $0.05 |
| `plan_slide` | Brief → top form/variant candidates with confidence. | Free |
| `browse_catalog` | 150+ patterns with per-form JSON Schemas + copy-pasteable example intents, themes, the code-mode widget toolkit. | Free |
| `translate_deck` | Translate any PPTX preserving formatting (8 languages). | $0.02/slide |
| `upload_asset` | Logos, theme PPTX, images; `purpose=pdf` extracts a PDF into editable slide intents; or AI-generate an image. | Free / $0.01/page / $0.05/image |
| `generate_report` | Data-driven multi-slide report from a connected tool (e.g. Zoho Sprints). | Per-slide |
| `manage_connections` | OAuth connections for data-driven reports. | Free |
| `manage_account` | Balance, usage, jobs, security status, feedback. | Free |

`dry_run: true` on create tools = validation + fidelity forecast at $0.

**Also on REST (for now): the Deck Doctor.** `POST /v1/inspect` — a free deterministic Deck Quality Report for **any** pptx (overflow via real font metrics, content hidden behind shapes, off-canvas leftovers, WCAG contrast). `POST /v1/repair` — deterministic fixes, never your words, $0.02/repaired slide, free dry-run quote. [Docs](https://slideforge.dev/docs/api/inspect)

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

No inline widgets in a terminal — the response JSON carries signed URLs instead:

```
preview_url  → curl -o preview.png "<url>"   # the agent can LOOK at its own render
pptx_url     → curl -o deck.pptx "<url>"
```

The self-review loop (render → view preview → fix → re-render) is documented in [`examples/claude-code.md`](examples/claude-code.md).

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
