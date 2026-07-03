# Claude Code Setup

## Add SlideForge

```bash
claude mcp add --transport http slideforge https://api.slideforge.dev/mcp/
```

Verify: `claude mcp list` → `slideforge` with 9 tools.

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

There are no inline widgets in a terminal — the response JSON carries signed URLs. The agent
can *look at its own render* and fix it:

```
1. create_slide(form=..., data=..., dry_run=true)   # free validation + fidelity forecast
2. create_slide(form=..., data=...)                  # $0.05 → preview_url + pptx_url
3. curl -o preview.png "<preview_url>"               # download the PNG
4. (view preview.png)                                # spot the issue on slide
5. fix the intent → re-render                        # identical input would be free;
                                                     # a changed intent is a fresh $0.05
6. curl -o slide.pptx "<pptx_url>"                   # deliverable
```

Read the **fidelity manifest** in every response: `verbatim` means every number came from your
input; `ai_completed`/`mixed` names the fields a model filled — tell the user which is which.

## Unattended runs

- `status: completed_with_errors` never bills — read each error's `remedy`, fix, re-render.
  Never retry an identical failed payload.
- Identical successful input re-renders free (`repeat_of`) — idempotent retries are safe.
- Deck renders are parallel and per-slide isolated: a failed slide never blocks (or bills
  inside) the rest of the deck.
