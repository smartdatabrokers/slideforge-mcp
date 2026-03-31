# SlideForge MCP Server Installation

This is a remote MCP server. No local installation required.

## Setup

1. Add to your MCP config with URL: `https://api.slideforge.dev/mcp/`
2. Authentication is handled via OAuth 2.1 (Claude Desktop) or API key (other clients)
3. For API key auth, sign up at [slideforge.dev](https://slideforge.dev) and get a key from Console → API Keys
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

- 13 tools + 2 guided workflow prompts
- Template rendering (39 consulting frameworks)
- Creative AI slide design
- Multi-slide deck generation
- Iterative refinement with visual QA
- Brand theme support
