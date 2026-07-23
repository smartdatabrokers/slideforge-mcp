# Publishing `slideforge-mcp`

Two distribution channels for the local stdio server. The hosted remote endpoint
(`https://api.slideforge.dev/mcp/`) needs neither.

## 1. PyPI — `pip install slideforge-mcp`

Makes the README's install line real and lets the MCP registry reference the package.

```bash
python -m build                      # builds dist/*.whl + *.tar.gz
python -m twine check dist/*         # must PASS
python -m twine upload dist/*        # needs a PyPI API token for the project owner
```

- Bump `version` in `pyproject.toml` + add a CHANGELOG entry before each upload.
- The wheel bundles `slideforge_mcp/contract/tools_list.prod.json` (verified) — the server
  needs it at runtime.
- The README carries an `mcp-name: dev.slideforge/slideforge` marker (used by the MCP
  registry to prove we own this PyPI package — see below). Keep it.

## 2. Official MCP Registry — `registry.modelcontextprotocol.io`

`server.json` (repo root) is authored + schema-valid (`2025-12-11`). It lists BOTH the
hosted remote and the PyPI package under one canonical entry.

**Publish PyPI first** (the registry validates the referenced package version exists and
carries the `mcp-name:` marker).

### Namespace + auth — pick one

- **DNS (recommended — branded `dev.slideforge/slideforge`).** Proves control of
  `slideforge.dev`. Add a TXT record the CLI prints:
  ```
  slideforge.dev.  IN TXT  "v=MCPv1; k=ed25519; p=<PUBLIC_KEY>"
  ```
  then:
  ```bash
  mcp-publisher login dns --domain=slideforge.dev --private-key=<HEX_PRIVATE_KEY>
  ```
  (HTTP alternative: host the proof at `https://slideforge.dev/.well-known/mcp-registry-auth`
  and `mcp-publisher login http --domain=slideforge.dev`.)

- **GitHub (simplest — `io.github.smartdatabrokers/slideforge-mcp`).** No DNS record; just
  `mcp-publisher login github`. If you choose this, change **both** the `name` in
  `server.json` **and** the `mcp-name:` marker in `README.md` to
  `io.github.smartdatabrokers/slideforge-mcp`, then re-publish PyPI so the marker matches.

### Publish

```bash
mcp-publisher publish --dry-run     # validates schema + package ownership + namespace auth
mcp-publisher publish
```

Keep `server.json` `version` and the `packages[].version` in step with the PyPI release and
the GitHub release tag on each update.
