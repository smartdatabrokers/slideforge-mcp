# SlideForge Skills

Agent skills ([SKILL.md standard](https://agentskills.io)) that teach an agent to use
[SlideForge](https://slideforge.dev) well — Claude Code, GitHub Copilot, Cursor, Codex and
friends. Each is a standalone folder; the agent auto-activates the matching one.

| Skill | Surface | What it does |
|---|---|---|
| **[create-slide](create-slide/SKILL.md)** | `create_slide` / `create_deck` / `browse_catalog` (MCP) | Intent-first slides & decks: schema discovery, dry-run, fidelity manifest, headless preview |
| **[inspect-repair](inspect-repair/SKILL.md)** | `POST /v1/inspect` + `/v1/repair` (REST) | Free Deck Quality Report on ANY pptx + deterministic repair (never alters words) |
| **[translate-pptx](translate-pptx/SKILL.md)** | `translate_deck` (MCP) | Translate a PPTX into 32 languages, formatting preserved |
| **[pdf-to-pptx](pdf-to-pptx/SKILL.md)** | `upload_asset purpose=pdf` (MCP) | Convert a PDF into an editable PPTX |

## Install

**Copy (any agent):**

| Scope | Path |
|---|---|
| Personal (all projects) | `~/.claude/skills/<skill-name>/` |
| Project | `.claude/skills/<skill-name>/` |

**Claude Code plugin (skills + MCP server config in one):**

```
/plugin marketplace add smartdatabrokers/slideforge-mcp
/plugin install slideforge@slideforge-mcp
```

The MCP-based skills need the server connected: `claude mcp add --transport http slideforge
https://api.slideforge.dev/mcp/` (the plugin bundles this via `.mcp.json`). The REST-based
inspect-repair skill needs only an API key from [slideforge.dev](https://slideforge.dev).
