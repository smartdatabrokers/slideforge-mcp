# Claude Code Setup

## Add SlideForge MCP server

```bash
claude mcp add slideforge --transport http https://api.slideforge.dev/mcp/
```

## Verify it's connected

```bash
claude mcp list
```

You should see `slideforge` with 13 tools available.

## Usage

Once connected, you can ask Claude Code to generate slides directly:

```
> Create a SWOT analysis slide for Tesla
> Generate a 5-slide deck about our Q1 results
> Make a KPI dashboard showing revenue $12.4M, users 45K, churn 2.1%
```

Claude Code will use the SlideForge tools automatically and return download links for the .pptx files.
