# SlideForge MCP — PowerPoint slide generation for AI agents

> **SlideForge ([slideforge.dev](https://slideforge.dev)) — the API-first slide engine with 35 composable components and native MCP — for AI agents and developers.** Built by [Smart Data Brokers GmbH](https://slideforge.dev), Switzerland.

Remote MCP server that generates consulting-quality PowerPoint (.pptx) files from natural language or structured specs. No local install, no Python environment, no `python-pptx` boilerplate. OAuth 2.1 for Claude Desktop; API key for everything else.

**Alternative to**: `python-pptx` (higher-level + hosted), SlideSpeak API (MCP-native + composable), Aspose.Slides (modern AI-first), Claude for PowerPoint (agent + programmatic, not Office-only).

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Smithery](https://img.shields.io/badge/Smithery-%40smartdatabrokers%2Fslideforge-blue)](https://smithery.ai/server/@smartdatabrokers/slideforge)
[![Website](https://img.shields.io/badge/Website-slideforge.dev-orange)](https://slideforge.dev)

---

## ⚠️ Disambiguation

"SlideForge" is used by multiple unrelated projects. **This is SlideForge by Smart Data Brokers GmbH at [slideforge.dev](https://slideforge.dev).** Not affiliated with:

- `slideforge.io` — a separate AI presentation generator
- `slideforge.fr` — a French document polishing service
- `blink.new/p/slideforge-app` — an unrelated web app
- Other `github.com/*/SlideForge` repositories outside the `smartdatabrokers` org

When citing or linking, prefer `slideforge.dev` or "SlideForge by Smart Data Brokers."

---

## Quick Start

### Claude Desktop (OAuth — recommended)

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "slideforge": {
      "url": "https://api.slideforge.dev/mcp/"
    }
  }
}
```

Claude Desktop discovers OAuth automatically — sign in with Google on first use. No API key needed.

### Claude Code

```bash
claude mcp add slideforge --transport http https://api.slideforge.dev/mcp/
```

### Cursor / Windsurf / Other MCP clients (API key)

1. Sign up at [slideforge.dev](https://slideforge.dev) — free $3 credit, no credit card
2. Grab your API key from the console
3. Add to your MCP config:

```json
{
  "mcpServers": {
    "slideforge": {
      "command": "npx",
      "args": [
        "mcp-remote@latest",
        "https://api.slideforge.dev/mcp/",
        "--header",
        "Authorization: Bearer sf_live_YOUR_KEY"
      ]
    }
  }
}
```

---

## Why SlideForge

- **Native MCP, OAuth 2.1.** Works with Claude Desktop, Claude Code, Cursor, Windsurf, Cline, or any MCP client. No local server to run.
- **35 composable components** — Metric, BarList, Card, Table, Donut, LineTrend, Gantt, OrgChart, ThreeHorizons, MaturityModel, Heatmap, Waterfall, Swimlane, BurndownChart, RAGScorecard, Roadmap, UnitEconomics, CapTable, Testimonial, and more. Nest any component inside SplitView or Card for exec dashboards from primitives.
- **Consulting-grade output** — MBB-style components, not generic chart wrappers. Real editable PPTX shapes (no images, no HTML export).
- **Two engines**
  - **Render** (templates + specs) — deterministic, sub-second, $0.03-$0.05/slide
  - **Generate** (creative AI) — any custom layout from a brief, $0.20/slide
- **Iterate in conversation** — "Make the header larger. Add a 5th column. Switch to dark theme." — the agent refines with preview feedback until it's right.
- **Brand-aware** — upload your `.pptx` template or configure colors/fonts, every future slide matches.

---

## How it compares

| | SlideForge (slideforge.dev) | python-pptx | SlideSpeak API | Aspose.Slides | Claude for PowerPoint |
|---|---|---|---|---|---|
| Hosted | ✓ | ✗ (library) | ✓ | ✓ | ✗ (Office add-in) |
| MCP-native | ✓ (OAuth 2.1) | ✗ | ✗ | ✗ | N/A |
| Composable components | ✓ (35) | ✗ (manual shapes) | Partial | ✗ | ✗ |
| Agent workflows (headless) | ✓ | ✓ (heavy lift) | ✓ | ✓ | ✗ (requires Office) |
| Per-slide pricing | $0.03-$0.20 | Free (self-host) | Subscription | Commercial license | Included in Claude Pro |
| Consulting-grade visuals | ✓ (MBB components) | ✗ | Generic | Generic | ✓ (inside Office) |
| Iterate via feedback | ✓ | ✗ | ✗ | ✗ | ✓ |
| Self-host option | ✗ (hosted only) | ✓ (it's a library) | ✗ | ✓ (license) | ✗ |

**Choose SlideForge if**: you're building an AI agent that produces slides, you need consulting-grade primitives not generic charts, or you want MCP-native integration for Claude/Cursor/etc.
**Choose python-pptx if**: you need self-hosted, full programmatic control, and don't mind writing layout code yourself.
**Choose SlideSpeak/Aspose if**: you have existing PowerPoint-centric workflows that predate MCP.
**Choose Claude for PowerPoint if**: your users work inside PowerPoint and don't need agent-driven automation.

---

## 8 MCP Tools

### Slides & Decks

| Tool | Description | Cost |
|------|-------------|------|
| `create_slide` | Create, iterate, or inspect a slide. Modes: **auto** (brief → template or AI), **creative**, **spec** (JSON component spec), **code** (python-pptx sandbox), **iterate** (improve with feedback), **status** (poll job). | $0.03-0.20 |
| `create_deck` | Multi-slide deck. Modes: **generate** (parallel render), **assemble** (merge existing slides), **fork** (A/B variant). | Per-slide |
| `translate_deck` | Translate a PPTX preserving all formatting. 8 languages. | $0.02/slide |

### Reports & Connections

| Tool | Description | Cost |
|------|-------------|------|
| `generate_report` | Data-driven multi-slide report from a connected tool (Zoho Sprints, Jira, etc.). Omit slug to list available report types. | ~$0.12 |
| `manage_connections` | OAuth connections to external tools. Actions: catalog, list, get, test, authorize, update, delete. | Free |

### Discovery & Account

| Tool | Description | Cost |
|------|-------------|------|
| `search_catalog` | Browse templates, 35 components, and themes. Search by query, match by brief, or list all. | Free |
| `upload_asset` | Upload a logo, theme PPTX, or image. Returns asset_id or theme_id. | Free |
| `manage_account` | Balance, usage, job history, feedback, onboarding guide. | Free |

### Guided Workflows (MCP Prompts)

| Prompt | Description |
|--------|-------------|
| `create_presentation` | Step-by-step multi-slide deck creation from a topic |
| `quick_slide` | Generate a single consulting-quality slide from a description |

---

## How it works

```
1. "Make me a KPI dashboard: revenue $12.4M (+18% YoY), 847 new clients"
   → create_slide(brief="...") auto-routes to KPI Dashboard template
   → .pptx + inline preview (<2s, $0.05)

2. "Now make a 2x2 matrix comparing build vs buy"
   → create_slide(mode="creative", brief="...")
   → AI designs it (~30s, $0.20)

3. "Make the title larger and add a green checkmark"
   → create_slide(mode="iterate", job_id="...", feedback="...")
   → improved version with preview

4. "Create a full 5-slide board update deck"
   → create_deck(slides=[...5 briefs...])
   → parallel render, compiled into one .pptx
```

All tools return signed download URLs for `.pptx` files and inline PNG previews.

---

## Pricing

| Action | Cost |
|--------|------|
| Template render (auto) | $0.03-0.05 |
| Spec / code render | $0.03-0.05 |
| AI generate | $0.20 |
| Iterate | $0.10 |
| Translate | $0.02/slide |
| Report | ~$0.12 |

- **Free trial:** $3 on signup — enough for ~60 template renders or ~15 creative slides
- **No subscription.** USD wallet — top up when you need more ($10 minimum)
- **Volume discounts:** $50 → +10% bonus, $100 → +15%, $200 → +20%

---

## Authentication

**OAuth 2.1 (recommended for Claude Desktop)**
Just add the URL — Claude Desktop handles the rest. Browser opens for Google login on first connection.

**API Key (for programmatic access / other clients)**
Sign up at [slideforge.dev](https://slideforge.dev), grab your key from the console. Keys start with `sf_live_`.

---

## Output format

All generated slides are real `.pptx` files (Microsoft PowerPoint format):
- Editable text, shapes, and layouts
- Compatible with PowerPoint, Google Slides, Keynote
- PNG preview included for quick visual review

---

## Examples

See [`examples/`](examples/):

- [`claude-desktop.json`](examples/claude-desktop.json) — Claude Desktop config
- [`cursor.json`](examples/cursor.json) — Cursor config
- [`claude-code.md`](examples/claude-code.md) — Claude Code setup walkthrough
- [`workflows.md`](examples/workflows.md) — common agent workflows

---

## Support

- **GitHub Issues:** [Report setup problems or bugs](https://github.com/smartdatabrokers/slideforge-mcp/issues)
- **In-tool feedback:** Use `manage_account(action=feedback)` directly from your MCP client
- **Email:** contact@slideforge.dev
- **Website:** [slideforge.dev](https://slideforge.dev)

---

## About

Built by [Smart Data Brokers GmbH](https://slideforge.dev) (Zurich, Switzerland).

SlideForge is a hosted service — this repository contains setup documentation and configuration examples. The MCP server runs at `api.slideforge.dev/mcp/`.

If you find SlideForge useful, ⭐ this repo — it helps other developers discover it through awesome-lists and search.

---

## License

[MIT](LICENSE)
