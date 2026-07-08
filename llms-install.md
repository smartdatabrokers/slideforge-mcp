# SlideForge MCP Server Installation

This is a remote MCP server. No local installation required.

## Setup

1. Add to your MCP config with URL: `https://api.slideforge.dev/mcp/`
2. Authentication is handled via OAuth 2.1 (Claude Desktop) or API key (other clients)
3. For API key auth, sign up at [slideforge.dev](https://slideforge.dev) and get a key from Console
4. No npm install, no Docker, no local dependencies needed

## Claude Desktop

```json
{
  "mcpServers": {
    "slideforge": {
      "url": "https://api.slideforge.dev/mcp/"
    }
  }
}
```

## Other Clients (API Key)

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

## Capabilities

- 7 tools + guided workflow prompts (2 more enterprise-gated: generate_report, manage_connections)
- `create_slide` — structured intent (form + typed fields, binds verbatim) or brief; `mode=code` for sandboxed python-pptx; every response carries a fidelity manifest
- `create_deck` — multi-slide parallel render into one merged .pptx (failed slides isolated + free)
- `plan_slide` — brief → ranked form/variant candidates (free)
- `browse_catalog` — 150+ patterns with JSON Schemas + example intents, themes, code-mode widgets (free)
- `translate_deck` — PPTX translation, 32 languages, formatting preserved ($0.02/slide)
- `upload_asset` — logos, themes, images; `purpose=pdf` extracts PDFs into editable intents
- `manage_account` — balance, usage, jobs, feedback, security status (free)
- REST-only: free `POST /v1/inspect` (Deck Quality Report for any pptx) + `POST /v1/repair`

Pricing: creating a slide $0.05 · transforming $0.02 (translate, repair) · checking free
(dry_run, plan, inspect). 60 free slides on signup. Machine-readable: GET /v1/pricing
