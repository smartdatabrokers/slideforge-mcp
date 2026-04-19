# Changelog

All notable changes to the SlideForge MCP server.

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
- 39 built-in consulting templates (now 58)
- Custom brand themes
- Inline PNG preview
- $3 free trial on signup
