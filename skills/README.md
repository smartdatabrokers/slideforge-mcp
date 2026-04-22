# SlideForge Skills

Claude Agent Skills that guide Claude in using the [SlideForge MCP server](https://api.slideforge.dev/mcp/) for high-leverage workflows. Each skill is a standalone `SKILL.md` file with YAML frontmatter.

## Skills

| Skill | Purpose | MCP tools used |
|---|---|---|
| **[consulting-deck](consulting-deck/SKILL.md)** | Generate a consulting-grade multi-slide PowerPoint deck from a topic or brief, following MBB narrative conventions | `create_deck`, `create_slide`, `upload_asset` |
| **[sprint-report](sprint-report/SKILL.md)** | Generate sprint retrospective, executive snapshot, PI progress, or portfolio health reports from live Zoho Sprints, Jira, Linear, or Azure DevOps data | `manage_connections`, `generate_report`, `create_slide` |

## Installation

Claude Desktop and Claude Code auto-discover skills placed in standard locations:

| Scope | Path |
|---|---|
| Personal (all projects) | `~/.claude/skills/` |
| Project (this repo only) | `.claude/skills/` |

To use these skills:

```bash
# Personal install
mkdir -p ~/.claude/skills
cp -r consulting-deck sprint-report ~/.claude/skills/

# Project install (from inside your project repo)
mkdir -p .claude/skills
cp -r consulting-deck sprint-report .claude/skills/
```

Restart Claude Desktop or reload Claude Code. The skills will activate automatically when Claude determines the user's request matches their `description` fields.

## Prerequisites

Both skills require the `slideforge` MCP server to be connected to Claude Desktop:

1. Claude Desktop → Settings → Connectors → Add
2. Server URL: `https://api.slideforge.dev/mcp/`
3. OAuth via Google sign-in — free $3 wallet on signup

Detailed setup: [slideforge.dev/docs/mcp](https://slideforge.dev/docs/mcp)

## License

MIT — same as the parent repository. Copy, adapt, and ship your own skills on top.

## Related

- **MCP server:** this repo — [smartdatabrokers/slideforge-mcp](https://github.com/smartdatabrokers/slideforge-mcp)
- **Hosted service:** [slideforge.dev](https://slideforge.dev)
- **Component reference:** [slideforge.dev/guides/slideforge-component-reference](https://slideforge.dev/guides/slideforge-component-reference)
- **Case studies:** [slideforge.dev/case-studies](https://slideforge.dev/case-studies)
