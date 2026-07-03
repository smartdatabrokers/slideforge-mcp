@AGENTS.md

# Claude Code specifics

- Install the server: `claude mcp add --transport http slideforge https://api.slideforge.dev/mcp/`
- Install the skills as a plugin: `/plugin marketplace add smartdatabrokers/slideforge-mcp`
  then `/plugin install slideforge@slideforge-mcp` — or copy folders from `skills/` into
  `~/.claude/skills/`.
- Responses have no inline widgets here: always `curl -o preview.png "<preview_url>"` and Read
  the PNG to check a render before declaring it done.
