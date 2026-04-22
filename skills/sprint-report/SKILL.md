---
name: sprint-report
description: "Generate a sprint retrospective, executive snapshot, PI progress, portfolio health, or sprint review deck from live data in a connected project-management tool (Zoho Sprints, Jira, Linear, Azure DevOps). Use when the user asks for a data-driven PM report, sprint wrap-up, PI/ART review, or portfolio-status deck. Requires the slideforge MCP server and an active OAuth connection to the user's PM tool. Saves hours of manual deck assembly per sprint."
---

# Sprint Report Generator

## Overview

This skill guides Claude in producing data-driven multi-slide reports from a connected project-management tool via the `slideforge` MCP server. The server fetches live metrics (velocity, burndown, blockers, retrospective items, portfolio health), computes them, and renders an opinionated deck — end-to-end in a single API call.

Trigger when the user asks for any recurring PM-tool report that today requires hours of manual deck assembly.

## Prerequisites

1. **`slideforge` MCP server connected** in Claude Desktop.
2. **An OAuth connection** to a supported PM tool:
   - Zoho Sprints (fully supported)
   - Jira Cloud
   - Linear
   - Azure DevOps
3. **A project ID** (optional — omit for workspace-wide reports).

## Workflow

### 1. Confirm the user has a connection

Call `manage_connections` with `action=list`:
```json
{"action": "list"}
```

If no connection exists, walk the user through authorizing one:
```json
{"action": "authorize", "vendor": "zoho", "integration_id": "zoho_sprints"}
```

The response includes an authorization URL. The user clicks, grants access, and Claude receives a `connection_id`.

### 2. Pick the report type

Five report slugs ship today:

| slug | When to use | Typical slides |
|---|---|---|
| `sprint-retrospective` | End-of-sprint wrap-up: what went well, blockers, lessons | 4 |
| `sprint-review` | Customer-facing sprint demo: completed work + upcoming | 4 |
| `executive-snapshot` | 1-pager for leadership: velocity, risks, hot items | 3 |
| `pi-progress` | SAFe PI (Program Increment) mid-flight status | 5 |
| `portfolio-health` | Multi-project RAG status for portfolio leads | 4 |

Omit `slug` to have `generate_report` list the available types.

### 3. Call `generate_report`

Minimal call (single project):
```json
{
  "slug": "sprint-retrospective",
  "connection_id": "conn_9149d82bef674473",
  "project_id": "12345"
}
```

Workspace-wide (no project filter):
```json
{"slug": "portfolio-health", "connection_id": "conn_9149d82bef674473"}
```

Historical context (look back N sprints):
```json
{
  "slug": "executive-snapshot",
  "connection_id": "conn_9149d82bef674473",
  "project_id": "12345",
  "sprint_history": 6
}
```

### 4. Deliver

Return the deck's `download_url` and summarize what's in it:
- Bullet the 3–5 key findings the deck surfaces (so the user can act without opening the file)
- Note the data cutoff time (reports pull live data at generation time)
- Suggest a follow-up action: "Regenerate this every Friday by scheduling a cron job against the REST endpoint"

## Iteration

Data-driven reports are usually correct on the first run because the metrics come from the source system. If the user wants to change the visual treatment, use `create_slide` with `mode=iterate` on a specific slide's `job_id`.

If the user wants different metrics (e.g., add a carryover-work chart), that requires a feature request — flag it and surface via `manage_account` action=feedback.

## Privacy & data handling

- Connection tokens are stored encrypted; SlideForge never sees the user's raw credentials
- Report data is fetched fresh on every call — not cached between runs
- Generated `.pptx` files live in user-scoped blob storage with HMAC-signed URLs (1-hour expiry)
- Privacy policy: `https://slideforge.dev/privacy`

## Pricing reminder

- `generate_report`: $0.12 per 4-slide report (~$0.03/slide)
- Typical weekly cadence: 1 exec-snapshot + 1 sprint-retro = $0.24/week per team
- Volume discounts apply on top-ups above $50

## Anti-patterns

- **Don't call `generate_report` without a `connection_id`.** Unless the user supplies `prepared_data` (pre-computed metrics dict), the server needs a live connection.
- **Don't ask the user for sprint numbers.** That's the whole point — SlideForge pulls them. If you find yourself asking, something's wrong with the connection.
- **Don't run this on a project the user didn't name.** Cost doubles for workspace-wide reports on big workspaces; confirm scope first.
- **Don't submit raw PM data to Claude.** Let the MCP server fetch + compute; you only consume the resulting deck download URL.

## Examples

### Weekly exec snapshot
> *"Give me an executive snapshot of project ENG-2024 for the last 4 sprints using my Zoho connection."*

Outcome: 3-slide deck with velocity trend, top 5 hot issues, and risk flags. $0.09. <15s.

### End-of-sprint retrospective
> *"Pull up a sprint retrospective deck for the sprint that just ended."*

Outcome: 4-slide deck with completed vs planned, retro themes, action items, next sprint focus. $0.12.

### PI-level status for leadership
> *"Generate a PI progress update for our current PI — all projects in the 'Platform' workspace."*

Outcome: 5-slide deck with per-team velocity, committed vs completed, risks by RAG status. $0.15.

## References

- slideforge MCP server: `https://api.slideforge.dev/mcp/`
- Connection framework: `https://slideforge.dev/docs/mcp#connections`
- Report spec: `docs/specs/21-report-compiler.md` (in slideforge repo)
- Case study — Starweaver PI reports: `https://slideforge.dev/case-studies/starweaver`
