# SlideForge is a REMOTE MCP server (https://api.slideforge.dev/mcp/, OAuth 2.1 or API key).
# This image is a thin stdio bridge for platforms that boot MCP servers from a container
# (e.g. Glama's inspector): it proxies stdio <-> the hosted Streamable HTTP endpoint.
# Provide SLIDEFORGE_API_KEY (an sf_live_... key from https://slideforge.dev/console) at run time.
FROM node:22-slim
ENV MCP_URL=https://api.slideforge.dev/mcp/
# Pre-fetch the bridge so container start is fast and offline-safe
RUN npm install -g mcp-remote@latest
ENTRYPOINT ["sh", "-c", "mcp-remote \"$MCP_URL\" --transport http-only --header \"Authorization: Bearer ${SLIDEFORGE_API_KEY}\""]
