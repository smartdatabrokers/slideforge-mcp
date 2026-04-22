---
name: translate-pptx
description: "Translate a PowerPoint (.pptx) deck into another language while preserving all formatting, layouts, charts, tables, and embedded media. Use when the user asks to translate a deck, localize a presentation, convert a PPTX to German/French/Spanish/etc., or similar. Supports 8 languages (en, de, fr, es, it, pt, nl, pl). Requires the slideforge MCP server."
---

# Translate PPTX

Use the `slideforge` MCP server to translate an existing PowerPoint deck without re-creating it from scratch. Every shape, chart, table, and embedded image stays exactly where it was — only the text content changes.

## When to trigger

Any request to translate, localize, or change the language of a PowerPoint file. Examples:
- "Translate this deck to German"
- "Can you localize this presentation into Spanish?"
- "Convert my PPTX from English to French"

## Tools used

- `translate_deck` — main tool
- `upload_asset` with `purpose=translate` — if the user uploads a file rather than passing a URL or job_id

## Workflow

### If the user has a prior slideforge job (preferred)

```json
{
  "target_language": "de",
  "job_id": "<previous slide or deck job_id>"
}
```

No file transfer needed — fastest path.

### If the user pastes a public URL to a PPTX

```json
{
  "target_language": "de",
  "pptx_url": "https://example.com/deck.pptx"
}
```

### If the user uploads a file

First upload via `upload_asset`:
```json
{
  "purpose": "translate",
  "data": "<base64-encoded .pptx>",
  "filename": "my-deck.pptx",
  "target_language": "de"
}
```

Returns a `job_id`; poll or set `include_preview` to get the result inline.

## Supported languages

| Code | Language |
|---|---|
| en | English |
| de | German |
| fr | French |
| es | Spanish |
| it | Italian |
| pt | Portuguese |
| nl | Dutch |
| pl | Polish |

`source_language` is auto-detected by default; override if needed.

## Useful options

- `include_notes: true` — translate speaker notes (default false)
- `include_tables: true` — translate table cells (default true)
- `concise_mode: true` — prefer shorter translations when text boxes are tight (e.g., German is ~30% longer than English; enable to keep layouts clean)

## Pricing

$0.02 per slide. A 20-slide deck = $0.40. 100-slide deck = $2.00.

## Delivery

The response includes a `download_url` (HMAC-signed, 1-hour expiry). The file is a real, editable `.pptx` — every translated element stays as a native PowerPoint shape.

## Anti-patterns

- Don't re-generate the deck from scratch — that loses formatting and costs 10x more. Use `translate_deck` on the existing file.
- Don't translate deck-by-deck in a loop if the user has 10 decks. Mention that the REST API supports batch calls for automation.
- Don't translate placeholder text like `{{company_name}}` — flag these to the user before translating; they usually should stay as-is.

## References

- MCP server: `https://api.slideforge.dev/mcp/`
- Docs: `https://slideforge.dev/docs/mcp`
- Translation API spec: `https://slideforge.dev/docs/api/translate`
