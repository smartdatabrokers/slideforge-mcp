# SlideForge local stdio MCP server — a real MCP server that runs locally over stdio.
# It bakes the tool schemas in (so `tools/list` works with no network and no key) and
# forwards tool calls to the SlideForge REST API (https://api.slideforge.dev) using an
# API key. NOT an mcp-remote proxy: the MCP protocol is served locally.
#
# Provide SLIDEFORGE_API_KEY (an sf_live_... key from https://slideforge.dev) at run time
# to make tool calls. Schema discovery needs neither a key nor network.
FROM python:3.12-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

# Install deps first for layer caching, then the package.
COPY pyproject.toml README.md ./
COPY src ./src
RUN uv pip install --system --no-cache .

# Non-root.
RUN useradd -m appuser
USER appuser

ENV PYTHONUNBUFFERED=1 \
    SLIDEFORGE_API_BASE="https://api.slideforge.dev" \
    SLIDEFORGE_API_KEY=""

# Launch the stdio MCP server (single process, JSON-RPC over stdin/stdout).
CMD ["slideforge-mcp"]
