# Workflow examples

Conversation-level patterns an agent can run over the SlideForge MCP tools. All prices:
$0.05/slide create, $0.02/slide transform, checks free.

## 1. Data → QBR deck (the reliable path)

```
→ plan_slide(brief="Q3 review: revenue KPIs, pipeline funnel, hiring plan, risks")
  Returns ranked forms per topic: kpi_metrics, funnel, gantt_plan, takeaway_stack
→ browse_catalog(type="schema", form="kpi_metrics")
  Returns the JSON Schema + a copy-pasteable example intent
→ create_deck(slides=[...4 intents with real numbers...], dry_run=true)     # $0
  Per-slide validation manifest; fix any errors by their remedy
→ create_deck(slides=[...same...])                                          # 4 × $0.05
  One merged .pptx; per-slide fidelity rollup — every number bound verbatim
```

## 2. Brand it

```
→ upload_asset(purpose="theme", data=<base64 corporate.pptx>)   # returns theme_id, free
  Big file? Omit `data` — the result card shows a drag/drop zone; bytes never pass through the agent.
→ create_deck(slides=[...], theme_id="thm_...")                  # every slide on-brand
  Uploaded themes render NATIVE by default — the deck is built ON the client's own template
  file (master, layouts, fonts intact). Response: brand_fidelity_level: "native".
```

## 2b. Fill the template's own designed slides (cover, agenda, dividers)

```
→ browse_catalog(type="themes", theme_id="thm_...")
  Lists the template's OWN layouts (cover, agenda, section_divider, closing) + fill schemas
→ create_slide(form="template_layout", theme_id="thm_...",
                data={"layout": "cover", "fills": {"title": "...", "subtitle": "..."}})
  Fills the template's designed slide literally — deterministic, LLM-free, verbatim
```

## 3. Pre-send QA on ANY deck (free)

```
→ POST /v1/inspect {pptx_url: "https://…/board_deck.pptx"}                  # free
  Deck Quality Report: overflow, hidden content, off-canvas leftovers, contrast
→ POST /v1/repair {pptx_url: ..., dry_run: true}                            # free exact quote
→ POST /v1/repair {pptx_url: ...}                                           # $0.02/repaired slide
  Deterministic fixes, never alters words; before/after diff included
```

## 4. PDF → editable deck

```
→ upload_asset(purpose="pdf", data=<base64 report.pdf>)   # $0.01/page: editable intents
→ create_deck(slides=<extracted intents>)                 # render editable pptx
→ POST /v1/inspect on the result                          # free fidelity check
```

## 5. Localize

```
→ translate_deck(target_language="de", pptx_url=...)      # $0.02/slide, formatting preserved
```

## 6. Self-review loop (headless clients)

```
→ create_slide(...)                                    # preview PNG is embedded INLINE in
                                                        # the tool result — the agent LOOKS at
                                                        # its own render directly, no fetch
→ fix the intent where needed → re-render (changed input: $0.05; identical: free)
→ curl -H "Authorization: Bearer sf_live_KEY" \
    -o deck.pptx https://api.slideforge.dev/v1/jobs/<job_id>/pptx   # deliverable, ownership-checked
→ POST /v1/jobs/<job_id>/download-url                  # mint a short-TTL single-use link to
                                                        # hand off, if the caller needs a URL
```
