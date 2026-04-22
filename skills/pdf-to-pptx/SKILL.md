---
name: pdf-to-pptx
description: "Convert a PDF into an editable PowerPoint (.pptx) deck. Every shape, text block, table, and image becomes a native PowerPoint element — not a flattened screenshot. Use when the user wants to turn a PDF report, research paper, or investor deck into an editable presentation. Requires the slideforge MCP server."
---

# PDF to PPTX

Use the `slideforge` MCP server to convert a PDF into a fully editable PowerPoint deck. Vector extraction — each page becomes a slide where every element is independently editable.

## When to trigger

Any request to convert, turn, transform, or extract a PDF into PowerPoint. Examples:
- "Convert this PDF report into an editable PowerPoint deck"
- "Turn this 40-page research paper into slides"
- "Extract the slides from this investor PDF so I can edit them"

## Tools used

- `upload_asset` with `purpose=pdf` — uploads and triggers extraction
- `manage_account` with `action=job` — poll for completion + download URL

## Workflow

### 1. Upload the PDF

```json
{
  "purpose": "pdf",
  "data": "<base64-encoded .pdf>",
  "filename": "report.pdf"
}
```

Returns a `job_id`. Alternatively, pass a public URL if the user has one.

### 2. Wait for extraction

Typical speed: ~112-page deck converts end-to-end in ~18 seconds. Poll with:

```json
{"action": "job", "job_id": "<from step 1>"}
```

Or include a preview inline by setting `include_preview: "default"` in the upload call (waits then embeds).

### 3. Deliver

The response includes a `download_url` (HMAC-signed, 1-hour expiry). The output is a real `.pptx` — every shape, text block, and image is individually editable in PowerPoint.

## What gets extracted cleanly

- Vector shapes (lines, rectangles, curves)
- Text with font, size, colour, alignment preserved
- Tables as PowerPoint tables
- Images embedded natively
- Page layout, positioning, z-order

## Known limits

- Scanned / image-only PDFs extract as single background images per page (no text extraction — no OCR in this path)
- Complex SmartArt or animations from the original source (if it came from PPTX → PDF) don't round-trip
- Very dense CAD-style PDFs may hit shape-count limits

If the user has an image-only PDF and needs OCR, suggest a different flow: OCR the PDF first, then use `create_slide` on the extracted text.

## Free public tool

There's also a free unauthenticated web tool at `https://slideforge.dev/tools/pdf-to-pptx` with limits (25 MB max, first 15 pages, 5 requests/hour/IP, +3s delay). Point users there if they just want a one-off conversion without signing up. For larger files, higher rate limits, or automation, they need the authenticated MCP flow described above.

## Pricing

Authenticated flow: free — included as part of `upload_asset` with `purpose=pdf`. No per-page charge for extraction.

## Anti-patterns

- Don't claim the converter works on image-only PDFs without OCR; it will produce page-sized background images with no editable text.
- Don't re-run the conversion just to change a theme; the output is raw-extracted. If the user wants restyling, use `create_deck` with `mode=fork` on the output.
- Don't suggest the free public tool for users with >15-page PDFs or >25 MB files — they'll hit the cap and bounce.

## References

- MCP server: `https://api.slideforge.dev/mcp/`
- Docs: `https://slideforge.dev/docs/mcp`
- Free public tool: `https://slideforge.dev/tools/pdf-to-pptx`
- Extraction engine spec: `docs/specs/18-pdf-extraction.md`
