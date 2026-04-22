---
name: create-slide
description: "Create a single PowerPoint slide from a plain-text brief, or a multi-slide deck from a list of briefs. Use when the user asks to make a slide, generate a PPTX, produce a deck, create a presentation, build a chart slide, draft a dashboard slide, or similar — any request that would result in a .pptx file. Supports iteration (refine a previous slide with feedback) and component specs (precise JSON layouts). Requires the slideforge MCP server."
---

# Create Slide

Use the `slideforge` MCP server to produce editable PowerPoint slides or decks from natural language.

## When to trigger

Any request for a slide, chart slide, dashboard, deck, or presentation. Examples:
- "Make me a slide showing Q3 revenue at $12.4M, 18% YoY growth, 847 new clients"
- "Create a 5-slide pitch deck for Acme Corp"
- "Build a slide with a bar chart comparing our three pricing tiers"

## Tools used

- `create_slide` — single slide
- `create_deck` — multi-slide (use whenever the user wants more than one slide)
- `search_catalog` — browse the 58 templates and 35 components if the user wants to pick a specific look
- `create_slide` with `mode=iterate` — refine an existing slide with text feedback

## Workflow

### Single slide

```json
{
  "mode": "auto",
  "brief": "Q3 revenue dashboard: $12.4M (+18% YoY), 847 new clients, NPS 71, retention 94%. Highlight revenue.",
  "theme_id": "consulting_blue"
}
```

`mode=auto` routes automatically: checks templates first (<2s, $0.03-0.05), falls back to AI generation if no match ($0.20, ~30s).

Other useful modes:
- `mode=creative` — force AI generation for complex/spatial layouts (org charts, scatter plots, architecture diagrams)
- `mode=spec` — precise JSON component layout ($0.05, <100ms); use after `search_catalog` to pick a component
- `mode=iterate` — refine a prior slide: pass `job_id` + `feedback` string ($0.10, <2s)

### Multi-slide deck

```json
{
  "mode": "generate",
  "theme_id": "consulting_blue",
  "title": "Q3 Strategy Review",
  "slides": [
    {"generate": {"brief": "Cover: Q3 Strategy Review, Acme Corp, November 2026"}},
    {"generate": {"brief": "Executive summary: revenue grew 18% YoY; recommend shifting spend to product-led growth"}},
    {"generate": {"brief": "Financial KPIs: $12.4M revenue, 847 new clients, NPS 71, retention 94%"}},
    {"generate": {"brief": "Three recommendations: (1) redirect acquisition spend, (2) hire 2 AEs, (3) launch marketplace beta"}}
  ]
}
```

Slides render in parallel (~8s per 5 slides) and compile into a single PPTX.

## Inline previews

Set `include_preview: "default"` on `create_slide` to embed a 512px PNG of the result in the response — Claude can show it inline without a separate fetch.

## Iteration loop

If the first result misses:

```json
{
  "mode": "iterate",
  "job_id": "<from previous response>",
  "feedback": "Make the revenue number bigger and use brand blue for the accent"
}
```

Cheap ($0.10) and fast (<2s). Works on any mode.

## Pricing reminder

Single slide:
- Template (auto): $0.03-0.05
- Creative AI: $0.20
- Iterate: $0.10
- Spec / code: $0.03-0.05

New accounts get $3 free credit on signup.

## Anti-patterns

- Don't fabricate data. If the user hasn't given numbers, ask — never invent revenue figures.
- Don't chain dozens of `mode=creative` calls for a long deck; use `create_deck` with `mode=generate` instead so slides render in parallel.
- Don't keep iterating past 2-3 rounds. If a slide isn't right after a couple of retries, switch `mode` or rethink the brief.

## References

- MCP server: `https://api.slideforge.dev/mcp/`
- Docs: `https://slideforge.dev/docs/mcp`
- Component reference: `https://slideforge.dev/guides/slideforge-component-reference`
