# SlideForge — agent instructions

SlideForge (slideforge.dev, by Smart Data Brokers GmbH) turns typed slide intents into native,
fully editable PowerPoint files. It is a **compiler, not a generator**: a deterministic engine
renders 150+ catalog patterns from structured content — no LLM in the render path — and every
response carries a **fidelity manifest** stating what was bound verbatim vs. model-completed.
Copy this file (or its rules) into a project where an agent produces .pptx deliverables.

## Connect

MCP (preferred — tools + schemas are self-describing):

```bash
# Claude Code
claude mcp add --transport http slideforge https://api.slideforge.dev/mcp/
# Codex CLI / Cursor / Windsurf: streamable-http MCP server at the same URL,
# header "Authorization: Bearer sf_live_YOUR_KEY"
```

REST (everything also works without MCP): `https://api.slideforge.dev/v1/…` with the same
Bearer key. Reference: https://slideforge.dev/docs/api — machine-readable rate card at
`GET /v1/pricing`.

## The workflow that works

1. **Discover the form.** `browse_catalog` (or `GET /v1/catalog`) → pick a `form`
   (kpi_metrics, waterfall_bridge, gantt_plan, org_structure, funnel, data_table, …).
   `browse_catalog type=schema form=<form>` returns the JSON Schema **and a copy-pasteable
   example intent** — start from the example, swap in real content, keep the field names.
   Unsure which form? `plan_slide` with the brief is free.
2. **Dry-run first.** Send the intent with `dry_run: true` → validation + a fidelity forecast
   at $0. Fix `errors[]` (each has a machine code + remedy), then resend without `dry_run`.
3. **Render.** `create_slide` (one) or `create_deck` (`slides[]`, parallel, failed slides are
   isolated and free). $0.05/slide, usable-or-free: a render with blocking errors never bills.
4. **Verify like an agent.** The response carries signed URLs — download `preview_url` (PNG)
   and *look at it* before declaring done; download `pptx_url` for the deliverable. In
   terminals there are no inline widgets — always fetch the preview.
5. **Trust the manifest, not vibes.** `fidelity: verbatim` = every number/word came from your
   input. `ai_completed`/`mixed` = the response names which fields a model filled. Surface
   that distinction to the user when the content is business data.

## Rules

- **Put real content in typed fields** (`data.*` per the form schema), not prose into a brief,
  whenever the content matters — typed input binds verbatim and forecasts `fidelity: verbatim`.
- **Never retry an identical failed payload** — fix what the error's `remedy` says. Identical
  *successful* input re-renders free (`repeat_of`), so idempotent retries are safe on success.
- **Decks:** one `create_deck` call, not N `create_slide` calls — parallel render, one merged
  pptx, per-slide manifest rollup.
- **Layouts the catalog can't express:** `mode=code` (sandboxed python-pptx + a widget/chart
  helper toolkit — list it via `browse_catalog type=widgets`). Still $0.05, still deterministic.
- **Check any existing deck for free:** `POST /v1/inspect` (REST) returns a Deck Quality Report
  for any pptx — overflow (real font metrics), content hidden behind shapes, off-canvas
  leftovers, WCAG contrast, hidden slides. `POST /v1/repair` applies deterministic fixes
  (never alters words; $0.02 per repaired slide; `dry_run` = free exact quote).
- **Transform:** `translate_deck` ($0.02/slide, 8 languages, formatting preserved);
  `upload_asset purpose=pdf` extracts a PDF into editable intents ($0.01/page).
- Costs are bounded and machine-readable (`GET /v1/pricing`); trial accounts start with
  60 free slides. Never invent prices in user-facing summaries — read the rate card.

## Files in this repo you can reuse

- `skills/` — agent skills (SKILL.md standard) for Claude Code, Copilot, Cursor & friends:
  `create-slide`, `inspect-repair`, `translate-pptx`, `pdf-to-pptx`.
- `examples/` — client configs (Claude Desktop, Cursor) and the headless self-review loop.
