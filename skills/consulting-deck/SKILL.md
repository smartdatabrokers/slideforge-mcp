---
name: consulting-deck
description: "Generate a consulting-grade multi-slide PowerPoint deck from a topic or brief. Use when the user asks for: (1) a multi-slide deck, presentation, or board review; (2) a strategy deck, KPI review, or executive update; (3) any consulting-style deliverable (McKinsey, BCG, Bain style) with cover, executive summary, body, and recommendations; or (4) converting research or data into a polished .pptx. Requires the slideforge MCP server to be connected (slideforge.dev)."
---

# Consulting Deck Generator

## Overview

This skill guides Claude in producing a consulting-grade multi-slide PowerPoint deck using the `slideforge` MCP server. It encodes the structural conventions of management-consulting decks (narrative arc, density per slide, layout choice, visual hierarchy) so that outputs read like an MBB deliverable rather than a generic AI presentation.

Trigger when the user asks for any multi-slide deliverable with a business or strategy framing. Do **not** trigger on single-slide requests — use `create_slide` directly instead.

## Prerequisites

- The `slideforge` MCP server must be connected in Claude Desktop or your MCP client.
- The user must have a funded wallet on slideforge.dev. A new account receives $3 of free trial credit, enough for ~15 creative slides or 100 template renders. Top-up starts at $10.

## Workflow

### 1. Clarify the deck shape before generating

Before calling the MCP, confirm:
- **Topic and audience** (executive / management / operational) — drives vocabulary density
- **Slide count** (5–12 is the consulting sweet spot; 3–4 for an exec-briefing; 15+ for a full board pack)
- **Theme** (`consulting_blue` is the default; `corporate_formal` for conservative audiences; `investor_pitch` for startups)
- **Must-have data** (numbers, charts, comparisons the user wants prominent)

If the user gives a one-line request like "make me a deck about X", propose a narrative outline first:
1. Cover
2. Executive summary (one slide, key takeaway)
3. Context / problem framing
4. 3–5 body slides (one idea per slide — do not cram)
5. Recommendations / next steps
6. Appendix (data tables, methodology) — optional

### 2. Call `create_deck`

Use mode=`generate` with the `slides` array. Each slide entry can be either:
- A brief (`{"generate": {"brief": "..."}}`) — Claude routes to the right engine
- A template + params (`{"render": {"template": "...", "params": {...}}}`) — deterministic, <1s, $0.03-0.05

Example:
```json
{
  "mode": "generate",
  "theme_id": "consulting_blue",
  "title": "Q3 Strategy Review",
  "slides": [
    {"generate": {"brief": "Cover: Q3 Strategy Review, Acme Corp, November 2026", "name": "cover"}},
    {"generate": {"brief": "Executive summary: revenue grew 18% YoY, driven by enterprise segment. Risk: CAC up 22%. Recommendation: shift spend to product-led growth.", "name": "exec_summary"}},
    {"generate": {"brief": "Q3 financial performance: revenue $12.4M (+18% YoY), new clients 847 (+23%), NPS 71, retention 94%. Emphasize retention.", "name": "financials"}},
    {"generate": {"brief": "Three-horizons view of our roadmap: Horizon 1 (defend core API, Q4), Horizon 2 (enterprise features, H1), Horizon 3 (marketplace, H2).", "name": "horizons"}},
    {"generate": {"brief": "Recommendations: (1) redirect 30% of paid acquisition to PLG; (2) hire two enterprise AEs; (3) launch beta of marketplace in March.", "name": "recommendations"}}
  ]
}
```

### 3. Iterate on specific slides

If a slide misses, use `create_slide` with `mode=iterate`, pass the slide's `job_id`, and describe the change in plain language ("make the financial numbers bigger", "change the three-horizons chart to use our brand colors"). Iteration is cheap ($0.10) and fast (<2s).

### 4. Deliver

Return the deck's `download_url` to the user and mention:
- File is hosted on HMAC-signed URL with 1-hour expiry
- Fully editable `.pptx` — every shape is a real PowerPoint element, not a flattened image
- Speaker notes, animations, and embedded media can be added manually in PowerPoint after download

## Anti-patterns

- **Don't cram one slide with everything.** One idea per slide is the consulting rule. If the user's brief has 5 ideas, that's a 5-slide deck, not one cluttered slide.
- **Don't use a generic theme for a named company.** Upload their brand via `upload_asset` with `purpose=theme` and pass the returned `theme_id`.
- **Don't generate a 30-slide deck in one call** without checking with the user. Decks over 15 slides risk over-spend and over-production; offer a 10-slide version first.
- **Don't invent data.** If the user hasn't given numbers, ask — don't fabricate revenue figures or KPIs.

## Examples

### Exec briefing (5 slides)
> *"Build me a 5-slide exec briefing on our Q3 performance. Revenue $12.4M, 847 new clients, NPS 71."*

Outcome: cover, exec summary, KPI dashboard, risks, next steps. ~$1 total.

### Strategy review (10 slides)
> *"Create a 10-slide strategy deck: where we are, where competitors are, three options, recommendation, roadmap, resource needs."*

Outcome: full narrative arc, mix of AI generation (creative slides) and template renders (structured slides). ~$2 total.

### Board pack (15 slides with appendix)
> *"Generate a 12-slide board deck on FY26 strategy, plus 3 appendix slides with the detailed financial model."*

Outcome: use `mode=generate` for the 12 narrative slides, then `mode=assemble` to append appendix slides rendered from templates.

## Pricing reminder

Surface cost before generating long decks. Typical spend:
- 5-slide exec briefing: ~$1
- 10-slide strategy deck: ~$2
- 15-slide board pack: ~$3

## References

- slideforge MCP server: `https://api.slideforge.dev/mcp/`
- Docs: `https://slideforge.dev/docs/mcp`
- Component reference: `https://slideforge.dev/guides/slideforge-component-reference`
- Full 8-tool list in `../README.md`
