@AGENTS.md

# Claude Code specifics

- Install the server: `claude mcp add --transport http slideforge https://api.slideforge.dev/mcp/`
- Install the skills as a plugin: `/plugin marketplace add smartdatabrokers/slideforge-mcp`
  then `/plugin install slideforge@slideforge-mcp` — or copy folders from `skills/` into
  `~/.claude/skills/`.
- Responses have no inline widgets here, but the tool result embeds the preview PNG inline —
  read it straight out of the response to check a render before declaring it done. Download
  the .pptx via header-auth: `GET /v1/jobs/<job_id>/pptx` with
  `Authorization: Bearer sf_live_YOUR_KEY`.
