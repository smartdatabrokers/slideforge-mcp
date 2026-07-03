---
name: inspect-repair
description: "Run a free deterministic quality report on ANY PowerPoint file (yours or generated elsewhere) and optionally auto-repair it. Use when the user asks to check/lint/QA/review a pptx, find broken slides, fix overflowing or hidden text, clean up a deck before sending, or verify a generated deck. Uses the SlideForge REST API (works without the MCP server); repair never alters words."
license: MIT
metadata:
  author: smartdatabrokers
  version: "1.0"
---

# Inspect & repair any deck (Deck Doctor)

`POST /v1/inspect` returns a Deck Quality Report for **any** .pptx — decks SlideForge never
rendered included. Free, deterministic, no LLM: the file is analyzed with real font metrics
and geometry, never sent to a model. Repair is $0.02 per repaired slide, and its `dry_run`
returns the exact fix plan (and therefore the exact price) free.

## Inspect

```bash
curl -X POST https://api.slideforge.dev/v1/inspect \
  -H "Authorization: Bearer sf_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"pptx_base64": "'"$(base64 -w0 deck.pptx)"'"}'
```

Sources (exactly one): `pptx_base64` (≤25 MB), `pptx_url` (https), or `job_id` (a SlideForge
render). First 50 slides; 30 requests/hour.

**What it finds** — each with a machine `code`, severity, message, remedy, and the offending
`shape_id`: text overflow / clipping (measured with real font metrics, autofit-aware), content
hidden behind opaque shapes (z-order), off-canvas leftovers (parked notes leak content!),
WCAG contrast, sub-9pt fonts, image-only slides, empty slides, hidden slides (marked; they
never fail the deck), density.

**Read it honestly:** `status` is clean | review | failed. `summary.font_size_coverage` /
`contrast_coverage` state how much of the deck the checks could actually resolve — inherited
theme values it can't resolve are skipped, never guessed. Report findings to the user by
slide number with the remedy; don't paraphrase severities up or down.

## Repair (deterministic, never your words)

```bash
# free exact quote first
curl -X POST https://api.slideforge.dev/v1/repair -H "Authorization: Bearer sf_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"pptx_url": "https://…/deck.pptx", "dry_run": true}'
# then apply
curl -X POST https://api.slideforge.dev/v1/repair -H "Authorization: Bearer sf_live_YOUR_KEY" \
  -H "Content-Type: application/json" -d '{"pptx_url": "https://…/deck.pptx"}'
```

Actions (subset via `actions[]`, default all): `shrink_to_fit` (measured, floor 9pt),
`raise_min_font` (only when it still fits), `remove_off_canvas` (fully-invisible junk only),
`fix_contrast` (WCAG AA, hue-preserving). **No characters are ever altered** — the response
carries a computed `visible_text_untouched` proof, a before/after report diff, and
`flagged_not_fixed[]` for anything ambiguous (with remedies). A run that fixes nothing bills
nothing; the repaired deck comes back as signed `pptx_url` + preview.

## Workflow patterns

- **Pre-send QA:** inspect → show the user errors/warnings by slide → offer repair dry-run
  quote → apply on confirmation → return the repaired file + the before/after diff.
- **Verify generated decks:** after any tool (SlideForge or otherwise) produces a pptx,
  inspect it before delivering — it's free and takes ~1s per 30 slides.
- **Hygiene sweep:** off-canvas findings often reveal parked working notes (names, comments)
  that ship inside the file — flag these as a content-leak risk, not just a visual issue.
