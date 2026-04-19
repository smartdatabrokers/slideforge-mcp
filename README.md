# SlideForge MCP Server

> Remote MCP server that generates consulting-quality PowerPoint slides.
> Real .pptx files from templates ($0.03) or AI-designed custom layouts ($0.20).
> 8 tools. No installation required.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Features

- **Template rendering** — 58 consulting frameworks (SWOT, KPI dashboard, timeline, comparison, Gantt, waterfall...). Instant results, $0.03-0.05/slide.
- **Creative AI design** — Describe any slide in plain English. AI designs the optimal layout with consulting-grade typography. $0.20/slide.
- **Deck generation** — Generate multi-slide decks in parallel. Mix template + creative slides. Auto-compiled into a single .pptx.
- **Iterate & refine** — Improve any slide with text feedback. Works on all strategies (template, spec, creative, code).
- **30 design system components** — Metric, BarList, Card, Table, Donut, LineTrend, Gantt, OrgTree, and more.
- **Brand themes** — Upload your corporate .pptx or define colors/fonts. All future slides match your brand.
- **Data-driven reports** — Connect Zoho Sprints, Jira, etc. via OAuth. Generate sprint retrospectives, PI progress, portfolio health.

---

## Quick Start

### Claude Desktop (OAuth — recommended)

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "slideforge": {
      "url": "https://api.slideforge.dev/mcp/"
    }
  }
}
```

That's it. Claude Desktop discovers OAuth automatically — sign in with Google on first use. No API key needed.

### Claude Code

```bash
claude mcp add slideforge --transport http https://api.slideforge.dev/mcp/
```

### Cursor / Windsurf / Other MCP Clients (API Key)

1. Sign up at [slideforge.dev](https://slideforge.dev) — free $3 credit on signup
2. Get your API key from the Console
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
| `search_catalog` | Browse 58 templates, 30 components, and themes. Search by query, match by brief, or list all. | Free |
| `upload_asset` | Upload a logo, theme PPTX, or image. Returns asset_id or theme_id. | Free |
| `manage_account` | Balance, usage, job history, feedback, onboarding guide. | Free |

### Guided Workflows (MCP Prompts)

| Prompt | Description |
|--------|-------------|
| `create_presentation` | Step-by-step multi-slide deck creation from a topic |
| `quick_slide` | Generate a single consulting-quality slide from a description |

---

## How It Works

```
1. "Make me a KPI dashboard: revenue $12.4M (+18% YoY), 847 new clients"
   → create_slide(brief="...") auto-routes to KPI Dashboard template
   → instant .pptx + inline preview (<2s, $0.05)

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

## Output Format

All generated slides are real `.pptx` files (Microsoft PowerPoint format):
- Editable text, shapes, and layouts
- Compatible with PowerPoint, Google Slides, Keynote
- PNG preview included for quick visual review
- PDF export available on all slides

---

## Support

- **GitHub Issues:** [Report setup problems or bugs](https://github.com/smartdatabrokers/slideforge-mcp/issues)
- **In-tool feedback:** Use `manage_account(action=feedback)` directly from your MCP client
- **Email:** hello@slideforge.dev
- **Website:** [slideforge.dev](https://slideforge.dev)

---

## About

Built by [Smart Data Brokers GmbH](https://slideforge.dev) (Switzerland).

SlideForge is a hosted service — this repository contains setup documentation and configuration examples. The MCP server runs at `api.slideforge.dev/mcp/`.

Star this repo if you find it useful — it helps others discover SlideForge.

---

## License

[MIT](LICENSE)
