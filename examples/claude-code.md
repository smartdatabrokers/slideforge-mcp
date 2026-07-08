# Claude Code Setup

## Add SlideForge

```bash
claude mcp add --transport http slideforge https://api.slideforge.dev/mcp/
```

Verify: `claude mcp list` → `slideforge` with 7 tools.

Optional — skills + server config as a plugin:

```
/plugin marketplace add smartdatabrokers/slideforge-mcp
/plugin install slideforge@slideforge-mcp
```

## Usage

```
> Make a KPI dashboard slide: revenue $12.4M (+18% YoY), 847 new clients, NPS 62
> Create a 5-slide QBR deck from the numbers in q3.csv
> Translate deck.pptx to German
> Check board_deck.pptx for quality issues before I send it
```

## The headless self-review loop

There are no inline widgets in a terminal, but the tool result embeds the preview PNG inline —
the agent can *look at its own render* directly out of the response and fix it:

```
1. create_slide(form=..., data=..., dry_run=true)   # free validation + fidelity forecast
2. create_slide(form=..., data=...)                  # $0.05 → inline preview PNG in the result
3. (view the inline preview)                         # spot the issue on slide
4. fix the intent → re-render                        # identical input would be free;
                                                     # a changed intent is a fresh $0.05
5. curl -H "Authorization: Bearer sf_live_YOUR_KEY" \
     -o slide.pptx https://api.slideforge.dev/v1/jobs/<job_id>/pptx   # deliverable
```

Read the **fidelity manifest** in every response: `verbatim` means every number came from your
input; `ai_completed`/`mixed` names the fields a model filled — tell the user which is which.

## Unattended runs

- `status: completed_with_errors` never bills — read each error's `remedy`, fix, re-render.
  Never retry an identical failed payload.
- Identical successful input re-renders free (`repeat_of`) — idempotent retries are safe.
- Deck renders are parallel and per-slide isolated: a failed slide never blocks (or bills
  inside) the rest of the deck.
