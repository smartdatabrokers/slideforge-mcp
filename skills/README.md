# SlideForge Skills

Claude Agent Skills that mirror the core tools of the [SlideForge MCP server](https://api.slideforge.dev/mcp/). Each skill is a standalone `SKILL.md` file with YAML frontmatter — Claude auto-activates the matching one when the user's intent lines up.

## Skills

| Skill | Core tool | What it does |
|---|---|---|
| **[create-slide](create-slide/SKILL.md)** | `create_slide` / `create_deck` | Turn a brief into a single slide, or a list of briefs into a deck |
| **[translate-pptx](translate-pptx/SKILL.md)** | `translate_deck` | Translate a PPTX into one of 8 languages, preserving formatting |
| **[pdf-to-pptx](pdf-to-pptx/SKILL.md)** | `upload_asset` (purpose=pdf) | Convert a PDF into an editable PPTX (vector extraction, ~18s for 112 pages) |

## Installation

Claude Desktop and Claude Code auto-discover skills in standard locations:

| Scope | Path |
|---|---|
| Personal (all projects) | `~/.claude/skills/` |
| Project (this repo only) | `.claude/skills/` |

```bash
# Personal install — all three skills
mkdir -p ~/.claude/skills
cp -r create-slide translate-pptx pdf-to-pptx ~/.claude/skills/

# Or project-scoped (from inside your project repo)
mkdir -p .claude/skills
cp -r create-slide translate-pptx pdf-to-pptx .claude/skills/
```

Restart Claude Desktop or reload Claude Code. Each skill activates automatically when the user's request matches its `description`.

## Prerequisites

All three skills need the `slideforge` MCP server connected:

1. Claude Desktop → Settings → Connectors → Add
2. Server URL: `https://api.slideforge.dev/mcp/`
3. Sign in with Google / GitHub / email — free $3 wallet on signup

Setup walkthrough: [slideforge.dev/docs/mcp](https://slideforge.dev/docs/mcp)

## License

MIT — copy, adapt, and ship your own skills on top.

## Related

- **MCP server:** this repo — [smartdatabrokers/slideforge-mcp](https://github.com/smartdatabrokers/slideforge-mcp)
- **Hosted service:** [slideforge.dev](https://slideforge.dev)
- **Free public tools:** [slideforge.dev/tools/pdf-to-pptx](https://slideforge.dev/tools/pdf-to-pptx) (no signup, rate-limited)
