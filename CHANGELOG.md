# Changelog

All notable changes to the SlideForge MCP server.

## 5.1.0 — 2026-07-08

- **Native brand-template rendering**: `upload_asset(purpose="theme", data=<base64 .pptx>)`
  renders NATIVE by default — the output deck is built ON the client's own template file
  (master, layouts, fonts intact), not a color-matched imitation. Responses carry
  `brand_fidelity_level: "native"`.
- **Drag/drop theme upload**: omit `data` on a large theme file and the result card shows a
  drop zone — bytes never pass through the agent.
- **Branded furniture layouts**: `create_slide(form="template_layout", theme_id=..., data=...)`
  fills the template's own designed cover/agenda/section-divider/closing slides verbatim,
  deterministic and LLM-free. Discoverable via `browse_catalog(type="themes", theme_id=...)`.
- **Translation: 8 → 32 languages** (Latin, Cyrillic, and Greek scripts; no CJK/RTL yet), both
  REST and MCP.
- **Security hardening**: tool result bodies are now credential-free (no signed URLs); the
  .pptx downloads via header-auth (`Authorization: Bearer` + ownership check);
  `POST /v1/jobs/<job_id>/download-url` mints a short-TTL single-use handoff link; artifacts
  auto-delete after 30 days; every download is audit-logged;
  `manage_account(action=security_status)` discloses the full posture in-band.
- **New fidelity grade `partial`**: some supplied content did not make it onto the slide; the
  manifest names what was dropped.

## 5.0.0 — 2026-07-03

The v5 surface (the engine consolidation shipped on the service earlier this year, now
reflected here):

- **7 served tools** (+2 enterprise-gated) — `browse_catalog` replaces `search_catalog`; `create_slide` is intent-first
  (form + typed fields bind verbatim; `mode=code` remains); the creative/iterate/template
  modes and per-mode pricing are gone. One price: $0.05/slide, usable-or-free.
- **Fidelity manifest** on every response (verbatim | mixed | ai_completed) — the honesty layer.
- **Deck Doctor**: free `POST /v1/inspect` (Deck Quality Report for any pptx) +
  `POST /v1/repair` ($0.02/repaired slide, never alters words). New `inspect-repair` skill.
- **Plugin marketplace**: `/plugin marketplace add smartdatabrokers/slideforge-mcp` installs
  skills + the MCP server config (`.claude-plugin/`, `.mcp.json`).
- **AGENTS.md** (portable, agents.md standard) + **CLAUDE.md** for agent-native onboarding.
- Skills rewritten for the current surface; README/llms-install/examples refreshed.

## [4.0.1] — 2026-04-22

### Fixed
- Tool annotation semantics corrected for Claude Connectors Directory
  compliance: `destructiveHint=false` on create/translate/generate tools
  (they create content, they don't destroy), `readOnlyHint=false` on
  `manage_account` (feedback submission writes), `idempotentHint=true`
  on `upload_asset` (safe to retry).
- Response size cap added to every inline preview embed (2 MB raw bytes
  / 1920px longest dim in "full" mode) so tool results stay under
  Anthropic's 25K-token MCP limit.

### Added
- Three Claude Agent Skills in `skills/` — create-slide, translate-pptx,
  pdf-to-pptx — mirroring the core MCP tools.

## [4.0.0] — 2026-04-22

### Added
- Component Library v4: flagship primitives (CapabilityMap, ScatterBubble,
  DecisionLog), composition as first-class path (Strategy on a Page,
  Portfolio steering), chart semantics overhaul.

### Changed
- Component catalog rationalized: Tracker.scorecard removed (dup with
  RAGScorecard), StakeholderMap alias removed (now aliased to OrgTree),
  fabricated `quality_score` / `usage_count` stripped from catalog API.
- Feature Grid template merged into Icon Grid (**breaking**: callers
  using `feature_grid` should migrate to `icon_grid`).

## [3.3.0] — 2026-04-21

### Added
- `ArchitectureStack` flagship primitive for enterprise architecture
  decks — semantic zones (layers, externals, cross-cutting), three
  opinionated styles (enterprise/data_ai/application), 10-code soft
  validation via `architecture_warnings` envelope.
- Three flagship templates (Architecture Overview, Data & AI Platform,
  Application Integration Architecture).

## [3.2.0] — 2026-04-20

### Added
- Public unauthenticated free-tier endpoint `POST /v1/tools/pdf-to-pptx`
  — 25 MB / 15-page caps, 5 req/hour/IP rate limit, Tier-1 abuse
  defense. Web UI at `/tools/pdf-to-pptx` with measured benchmark
  (112-page deck → 18 s).

## [2.0.0] — 2026-04-19

### Changed

- **Tool consolidation: 28 → 8 tools.** Fewer tools = faster agent discovery, less context overhead.
- `create_slide` replaces render_slide, generate_slide, iterate_slide, render_spec, render_code, get_slide_status, suggest_layout, render_preflight. Uses `mode` param (auto/creative/spec/code/iterate/status).
- `create_deck` replaces generate_deck, assemble_deck, fork_deck. Uses `mode` param (generate/assemble/fork).
- `search_catalog` replaces list_templates, search_templates, suggest_template, list_components, search_components, list_themes. Uses `type` param (templates/components/themes).
- `manage_account` replaces get_me, get_usage, list_jobs, submit_feedback, get_agent_onboarding, get_capabilities. Uses `action` param.
- `upload_asset` replaces upload_file. Cleaner schema with `purpose` param (logo/theme/image).
- `generate_report` now supports discovery mode (omit slug to list available report types).
- Default `include_preview` changed from "none" to "default" — agents get inline previews automatically.

### Added

- Spec iteration: `create_slide(mode=iterate)` now works on spec-rendered slides (was broken pre-v2.6.3).
- `_to_emu()` helper: shape helpers accept both `Inches()` and float values — no more double-wrapping bugs.
- `_segment_color()`: chart segments (stacked bars, donuts) use distinct primary/accent colors.
- Template enrichment: auto-routed templates enrich sparse briefs before param extraction.

### Fixed

- 12 quality bugs from v2.6.3-v2.6.5 test report (metric delta, tracker value, donut labels, etc.)

## [1.0.0] — 2026-03-31

### Available

- 13 MCP tools (later expanded to 28 before consolidation)
- 2 MCP prompts: `create_presentation`, `quick_slide`
- OAuth 2.1 authentication (Claude Desktop native)
- API key authentication (all MCP clients)
- 39 built-in consulting templates
- Custom brand themes
- Inline PNG preview
- Free trial on signup (today: 60 free slides)
