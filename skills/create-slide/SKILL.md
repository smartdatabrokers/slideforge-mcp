---
name: create-slide
description: "Create editable PowerPoint slides or whole decks with SlideForge. Use when the user asks to make a slide, deck, presentation, dashboard slide, chart slide, QBR/board exhibit, or anything that results in a .pptx file. Structured intents render deterministically with a fidelity manifest (verbatim vs ai_completed); briefs work too. Requires the slideforge MCP server (or the REST API)."
license: MIT
metadata:
  author: smartdatabrokers
  version: "5.1"
---

# Create slides & decks

SlideForge is a compiler: a slide is a typed intent (`form` + typed content fields) rendered
deterministically into native, editable .pptx — no LLM in the render path. $0.05/slide,
usable-or-free; identical input re-renders free.

## The reliable path (use for real content)

1. **Pick the form.** `browse_catalog` lists 150+ patterns (kpi_metrics, waterfall_bridge,
   gantt_plan, funnel, org_structure, data_table, comparison_matrix, timeline_roadmap, …).
   Unsure? `plan_slide` with a one-line brief returns ranked candidates, free.
2. **Get the contract.** `browse_catalog` with `type=schema` + the form returns the JSON Schema
   **and a copy-pasteable example intent**. Start from the example; swap in the user's real
   content; keep the advertised field names exactly.
3. **Dry-run.** Send the intent with `dry_run: true` → `status: validated` + a
   `fidelity_forecast` at $0. If `errors[]` come back, each carries a machine `code` and a
   `remedy` — fix and re-dry-run. Never pay to discover a validation error.
4. **Render.** Same payload without `dry_run`. The response embeds a preview PNG inline, cost,
   and the **fidelity manifest**. The editable file downloads separately (see below).

For a whole deck: ONE `create_deck` call with `slides[]` (a list of create_slide intents).
Parallel render, one merged pptx, per-slide fidelity rollup; failed slides are isolated and free.

Grammar worth knowing (v5.104 surface):
- **Stat prominence**: list/workflow block items take `metric: {value, label}` — the number
  renders as a stat column instead of hiding in prose. Keep values bare (`42` or `"42"`),
  no % signs, units, or currency symbols inside numeric fields.
- **Architecture depth**: layer stacks take `orientation: "horizontal"` (left-to-right
  pipeline with crossing control rails) and per-component `state: current|target|gap`
  (capability-heat tinting) — consulting capability-map staples from one typed payload.
- **`quality_profile`** (executive/technical/appendix) answers on ANY form — the response's
  `layout.presentation_ready` is judged against it; measurement only, never blocks or bills.

## Quick path (throwaway / exploratory)

A plain-text `brief` renders in one call — the engine routes it to a form. Fine for drafts;
expect `fidelity: ai_completed` (the model structured your prose). For business numbers,
always prefer typed fields.

## Reading the response honestly

- `fidelity: verbatim` — every word/number came from the user's input. Say so.
- `fidelity: mixed / ai_completed` — the manifest names which fields a model completed.
  Tell the user which parts to double-check.
- `fidelity: partial` — some supplied content did not make it onto the slide. The manifest
  names what was dropped. Never deliver a `partial` render without telling the user what's
  missing.
- `status: completed_with_errors` — the render is flawed and was NOT billed. Read the error
  remedies, fix the intent, re-render. Do not deliver the artifact as if it were fine.
- `warnings[]` — quality advisories (density, contrast, overflow) with remedies; the slide
  billed and is usable, but mention material ones.

## Headless verification (Claude Code / Codex CLI — no widgets)

The preview PNG is embedded inline in the tool result — read it directly, no fetch needed.
Always look at your own render before declaring done. Download the deliverable via header-auth:

```bash
curl -H "Authorization: Bearer sf_live_YOUR_KEY" \
  -o slide.pptx https://api.slideforge.dev/v1/jobs/<job_id>/pptx   # ownership-checked
```

If the preview shows a problem, fix the intent and re-render — refinement is a fresh $0.05
render (identical input is free, so only actual changes cost).

## Escape hatch: mode=code

When no catalog form fits, `create_slide` with `mode=code` runs your python-pptx in a sandbox
(same $0.05, deterministic). `browse_catalog type=widgets` / `type=helpers` lists the bundled
board-grade widget + chart toolkit so you don't hand-roll primitives.

## Do / don't

- DO put real content in `data.*` typed fields; DON'T paste it into a brief when it matters.
- DO fix errors by their `remedy`; DON'T retry an identical failed payload.
- DO use one `create_deck` for multi-slide; DON'T loop `create_slide`.
- DO pass `min_font_pt` when the user demands a minimum font size (binding: type grows to
  meet it; unmeetable content = $0 error naming the size it needs); DON'T shrink-to-fit by
  cutting the user's words yourself — `allow_truncation` drops whole items, never words.
- DO pass `theme_id` (or upload a theme PPTX via `upload_asset(purpose="theme", data=<base64>)`)
  for branding — uploaded themes render NATIVE by default, built ON the client's own template
  file (master, layouts, fonts).
- DO use `create_slide(form="template_layout", theme_id=..., data={"layout": ..., "fills": ...})`
  to fill the template's own designed cover/agenda/divider slides verbatim.
- DO expect topical design on the default themes: an unpinned render may take a subject-informed
  accent palette + designed cover (the response's design note names the choice). Pass
  `styling: "clean"` for the neutral default look; a pinned `theme_id`/uploaded theme never
  takes topical styling.
