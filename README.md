# SlideForge MCP Server

> Remote MCP server that generates consulting-quality PowerPoint slides.
> Real .pptx files from templates ($0.03) or AI-designed custom layouts ($0.10–$0.20).
> No installation required.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Features

- **Template rendering** — 39 consulting frameworks (SWOT, KPI dashboard, timeline, comparison, Gantt, waterfall…). Instant results, $0.03–0.07/slide.
- **Creative AI design** — Describe any slide in plain English. AI designs the optimal layout with consulting-grade typography. $0.10–0.20/slide.
- **Deck generation** — Generate multi-slide decks in parallel. Mix template + creative slides. Auto-compiled into a single .pptx.
- **Iterate & refine** — Improve any slide with text feedback. AI converges on quality through visual QA.
- **Brand themes** — Upload your corporate .pptx or define colors/fonts → all future slides match your brand.

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
2. Get your API key from the Console → API Keys page
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

## Available Tools

### Generation & Design

| Tool | Description | Cost |
|------|-------------|------|
| `render_slide` | Render from a consulting template with data or brief | $0.03–0.07 |
| `generate_slide` | AI-designed custom slide from natural language description | $0.10–0.20 |
| `generate_deck` | Multi-slide PowerPoint deck (parallel generation + auto-compile) | Per-slide |
| `iterate_slide` | Improve a previously generated slide based on text feedback | $0.05–0.20 |

### Discovery

| Tool | Description | Cost |
|------|-------------|------|
| `suggest_template` | Find best template(s) for your brief (batch support) | Free |
| `search_templates` | Semantic search across 39 templates | Free |
| `list_templates` | Browse all templates (filterable by category, audience, style) | Free |
| `list_themes` | Available color themes and brand palettes | Free |

### Status & Account

| Tool | Description | Cost |
|------|-------------|------|
| `get_slide_status` | Poll job status + download URLs + inline preview PNG | Free |
| `list_jobs` | Recent generation jobs (filterable by status) | Free |
| `get_usage` | Usage stats, cost breakdown, daily history | Free |
| `get_capabilities` | Account status, available tools, optimal workflow | Free |
| `submit_feedback` | Report bugs, request features, share testimonials | Free |

### Guided Workflows (MCP Prompts)

| Prompt | Description |
|--------|-------------|
| `create_presentation` | Step-by-step multi-slide deck creation from a topic |
| `quick_slide` | Generate a single consulting-quality slide from a description |

---

## How It Works

```
1. suggest_template("KPI dashboard for Q1 board review")
   → finds best-matching template

2a. Good match → render_slide(template=uuid, brief="Revenue $12.4M, +18% YoY...")
    → instant .pptx (~1s, $0.03)

2b. No match → generate_slide(brief="Custom waterfall chart showing margin drivers...")
    → AI designs it (~12s, $0.10)

3. Not happy? → iterate_slide(job_id=..., feedback="Make the title larger, add a takeaway bar")
   → improved version

4. Need a deck? → generate_deck(prompt="Q1 Board Review", slide_count=5)
   → 5 slides generated in parallel, compiled into one .pptx
```

All tools return signed download URLs for `.pptx` files and PNG previews.

---

## Pricing

| | Draft | Pro |
|---|---|---|
| **Generate / Iterate** | $0.10 | $0.20 |
| **Template Render** | $0.03–0.07 | — |
| **AI Image** | $0.05 | $0.10 |

- **Free trial:** $3 on signup — enough for ~30 template renders or ~15 creative slides
- **No subscription.** USD wallet — top up when you need more ($10 minimum)
- **Volume discounts:** $50 → +10% bonus, $100 → +15%, $200 → +20%
- **Feedback rewards:** Approved feature requests earn $5, testimonials earn $2

---

## Authentication

SlideForge supports two auth methods:

**OAuth 2.1 (recommended for Claude Desktop)**
Just add the URL — Claude Desktop handles the rest. Browser opens for Google login on first connection. New users are auto-provisioned with a $3 wallet.

**API Key (for programmatic access / other clients)**
Sign up at [slideforge.dev](https://slideforge.dev), grab your key from the console. Keys start with `sf_live_`. Pass via `Authorization: Bearer sf_live_xxx` header.

---

## Output Format

All generated slides are real `.pptx` files (Microsoft PowerPoint format):
- Editable text, shapes, and layouts
- Compatible with PowerPoint, Google Slides, Keynote
- PNG preview included for quick visual review
- Inline preview in Claude Desktop via `get_slide_status`

---

## Support

- **GitHub Issues:** [Report setup problems or bugs](https://github.com/smartdatabrokers/slideforge-mcp/issues)
- **In-tool feedback:** Use the `submit_feedback` tool directly from your MCP client
- **Email:** hello@slideforge.dev
- **Website:** [slideforge.dev](https://slideforge.dev)

---

## About

Built by [Smart Data Brokers GmbH](https://slideforge.dev) (Switzerland).

SlideForge is a hosted service — this repository contains setup documentation and configuration examples. The MCP server runs at `api.slideforge.dev/mcp/`.

⭐ Star this repo if you find it useful — it helps others discover SlideForge.

---

## License

[MIT](LICENSE)
