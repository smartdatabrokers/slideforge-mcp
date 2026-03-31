# SlideForge Workflow Examples

## 1. Quick Template Render

Best for: standard consulting frameworks with your data.

```
User: "Create a SWOT analysis for our mobile app launch"

→ suggest_template(brief="SWOT analysis for mobile app launch")
  Returns: template UUID + param schema

→ render_slide(template="uuid-here", brief="Strengths: strong brand, 2M users...")
  Returns: pptx_url + preview_url (~1s, $0.03)
```

## 2. Creative AI Slide

Best for: custom layouts that don't fit a template.

```
User: "Design a slide showing our 5-year revenue trajectory with key milestones"

→ generate_slide(brief="5-year revenue trajectory line chart with milestones: 2022 Series A $2M, 2023 product-market fit $5M, 2024 expansion $12M, 2025 profitability $28M, 2026 target $50M. Include growth rate annotations.")
  Returns: job_id

→ get_slide_status(job_id="...")  (poll every 3s)
  Returns: pptx_url + preview_url (~12s, $0.10)
```

## 3. Iterate on a Slide

Best for: refining a generated slide based on feedback.

```
→ iterate_slide(job_id="previous-job-id", feedback="Make the title larger, use our brand blue (#1B4F72), and add a takeaway banner at the bottom saying 'On track for $50M ARR'")
  Returns: new job_id with improved slide
```

## 4. Multi-Slide Deck

Best for: full presentations.

```
User: "Create a 5-slide Q1 board review deck"

→ generate_deck(prompt="Q1 2026 Board Review for a B2B SaaS company", slide_count=5)
  Returns: deck job_id

→ get_slide_status(job_id="deck-id")  (poll until complete)
  Returns: compiled .pptx with all 5 slides (~38s, ~$0.50)
```

## 5. Template Discovery

Browse and search before generating.

```
→ list_templates(category="strategy")
  Returns: SWOT, Porter's Five Forces, BCG Matrix, Value Chain...

→ search_templates(query="financial performance dashboard")
  Returns: ranked matches with UUIDs and param schemas

→ suggest_template(briefs=["KPI dashboard", "team org chart", "project timeline"])
  Returns: best template match for each brief (batch mode)
```

## 6. Brand Theme Workflow

Apply your corporate identity to all slides.

```
→ list_themes()
  Returns: available themes (default, corporate_blue, dark_executive, ...)

→ generate_slide(brief="...", theme_id="corporate_blue")
  Returns: slide styled with that theme's colors and fonts
```
