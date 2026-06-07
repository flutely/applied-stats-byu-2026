# applied-stats-byu-2026

Workshop materials for the **50th Summer Institute of Applied Statistics (SIAS)** at Brigham Young University, 17-18 June 2026, taught by Julia Silge. Title: *Programming with LLMs for Data Practitioners*. Two days:

- Day 1, "Build on AI": programming with LLMs from R (`ellmer`) and Python (`chatlas`). Four sessions: (1) Talking with LLMs, (2) Programming with LLMs, (3) Prompt engineering and RAG, (4) Beyond prompts (tool calling, MCP, an agents teaser, querychat as a bonus).
- Day 2, "Build with AI": using AI coding assistants (inline completions, chat, agentic). Currently mostly TODO placeholders.

## Status and next steps

**Day 1 (decks 01-04) is built out** and Anthropic-only for participants: slides, exercises, and demos are in place (the OpenAI / multi-provider exceptions are the three demos listed under Demos below).

**Day 2 (decks 05-08) is the next work, start here.** The decks exist as slide skeletons (section headings, but no `## Your turn` activities or demos yet) and need building out. Day 2 is "Build with AI": AI coding assistants (Positron Assistant, inline completions, chat, agentic workflows), where MCP and agents (previewed on Day 1) get their full treatment. There are no Day-2 exercises in `code/` or demos in `demo/` yet.

Open items:

- `code/15-querychat.{R,py}` is the only remaining Day-1 placeholder (still `TODO`), waiting on a dataset; when it is filled, add `querychat` to `requirements.txt`.
- MCP is a Day-1 preview only; the `17-mcp` exercise was removed. Build the real MCP material into Day 2.
- The agentic "databot" demo was removed, to be rebuilt for Day 2 (deck 08).
- Verification gap: the Shiny apps and `.qmd` demos are checked by parse/compile and API introspection, not a live run. Do a local smoke test (`shiny run` / `runApp` / run the `.qmd` chunks) before the workshop. `faicons` and `playsound3` are listed in `requirements.txt` but were not installed in this dev env.

## Layout

- `index.qmd`: landing page with welcome, learning objectives, local-setup prep, and a per-day schedule table.
- `slides/`: eight numbered reveal.js decks (`01-talking-with-llms.qmd` ... `08-agentic-workflows.qmd`) plus `custom.scss` and `title-slide.html` (custom partial).
- `code/`: flat `NN-name.R` / `NN-name.py` Day-1 exercise skeletons (R + Python pairs), numbered `01`-`15`, gapless. (RAG became `demo/03-rag` and the MCP exercise was dropped, so the deck-04 exercises were renumbered to close the gaps; MCP is a Day-1 preview only.) Plus companion Shiny apps (`08-batch-app`, `11-quiz-game-app`), the quiz prompt (`11-quiz-game-prompt.md`), and coding-assistant context docs (`12-coding-assistant-docs-{py,rstats}.md`). Header comments are `# NN-name.ext` then `# Deck NN: <deck title> (<section>)`.
- `demo/`: instructor-run demo apps and docs, one folder per demo, prefixed by the deck number it supports (`01-clearbot`, `01-token-possibilities`, `02-models`, `03-rag`, `04-manual-tools`, `04-weather-tool`). Slides point at these via `## Demo` callouts.
- `data/`: shared data for exercises. `recipes/` (`images/`, `pdf/`, `text/`) feeds the multi-modal, structured-output, and batch exercises; `mtcars.csv` feeds the plot-interpretation exercises.
- `images/`: 8 unDraw SVG illustrations, one per deck. Mapping is fixed; see deck YAML `data-background-image`.
- `_extensions/`: `gadenbuie/countdown` (timer shortcode) and `quarto-ext/fontawesome`.
- `_quarto.yml`: website config; theme is `[zephyr, footer.scss]`. Output dir is `docs/`.
- `footer.scss`: site SCSS. Disables zephyr's Google Fonts import via `$web-font-path: false`, plus footer layout and table-width rules.
- `init-env.sh`: local setup helper for R (renv) + Python (uv). No Codespaces.
- `requirements.txt`: Python packages (`chatlas`, `shiny`, plus deps).
- `DESCRIPTION`: R dependency manifest (`Type: Workshop`). Licensing: course content (slides, prose) is CC BY-NC-SA 4.0 (root `LICENSE.md`, matching the site footer and `DESCRIPTION`); the demos are MIT (built on Garrick Aden-Buie's work), each `demo/*` carries its own MIT `LICENSE`.
- Renamed `footer.scss` from `footer.css` because it contains SCSS (`$var` syntax). Do not rename back, the CSS linter will complain.

## Slide deck conventions

Every deck's YAML uses:

```yaml
format:
  revealjs:
    theme: [default, custom.scss]
    template-partials:
      - title-slide.html
    title-slide-attributes:
      data-background-image: "../images/undraw_<name>.svg"
      data-background-size: "auto NN%"      # tuned per illustration aspect ratio
      data-background-position: "82% 85%"   # uniform across all decks
      data-background-repeat: "no-repeat"
```

- **`title-slide.html`** is a custom Pandoc partial that wraps title / subtitle / author in `<div class="title-slide-inner">` so `custom.scss` can pin it to the top-left.
- **H1 section dividers** repeat the illustration via inline attributes: `# Heading {background-image="..." background-size="..." background-position="..." background-repeat="..."}`. Size and position must match that deck's title slide values.
- **Title and Thanks slides have no `{background-image=...}` attribute** so they show plain (no corner illustration).
- **`# Thanks!` slide** at the end of every deck repeats the contact card from deck 01's `# Hello!` slide, with undraw attribution in `::: footer :::`.

### Activity pattern ("Your turn")

Every place participants do hands-on work uses:

```markdown
## Your turn

::: {.callout-note icon=false}

## Activity

<description, optionally a lead-in plus bullets>
:::

{{< countdown minutes=N >}}
```

The `{{< countdown >}}` shortcode comes from the `gadenbuie/countdown` extension in `_extensions/`.

### Demos

Some sections use an instructor-run demo instead of (or alongside) a participant activity. On the slide this is a `## Demo` (or `## Demos`) heading inside a `::: {.callout-note icon=false}` block, with a code block or path pointing at the matching folder under `demo/`. Demo folders are prefixed by the deck number they support.

This is an **Anthropic-only** workshop for participants: exercises and demos use Claude (`ellmer` / `chatlas`), participants set `ANTHROPIC_API_KEY`, and code targets current Claude model ids (e.g. `claude-opus-4-8`, `claude-sonnet-4-6`, `claude-haiku-4-5`). Three instructor-run demos use OpenAI on the instructor's own keys, because they need a capability Anthropic lacks or compare providers:

- `demo/01-token-possibilities` visualizes token log-probabilities (`logprobs`), which Anthropic's API does not expose.
- `demo/03-rag` uses OpenAI **embeddings** (`embed_openai`) for retrieval, since Anthropic has no embeddings API; the chat model is still Claude.
- `demo/02-models` deliberately compares several providers (Anthropic, OpenAI, Google).

The two tool-calling demos (`demo/04-manual-tools`, `demo/04-weather-tool`) run on Claude: tool calling needs no OpenAI-specific feature, and tools should be shown on the provider participants use.

### Per-deck illustration mapping

| Deck | Illustration | `data-background-size` |
|---|---|---|
| 01 Talking with LLMs | `undraw_chat-with-ai_ir62.svg` | `auto 50%` |
| 02 Programming with LLMs | `undraw_large-language-models_m4no.svg` | `auto 45%` |
| 03 Prompt engineering and RAG | `undraw_ai-research-assistant_cxx0.svg` | `auto 50%` |
| 04 Beyond prompts | `undraw_artificial-intelligence_43qa.svg` | `auto 55%` |
| 05 AI coding assistants | `undraw_coding-assistant_i178.svg` | `auto 40%` |
| 06 Code completions | `undraw_vibe-coding_mjme.svg` | `auto 50%` |
| 07 Chat assistance | `undraw_ai-answers_uxgx.svg` | `auto 50%` |
| 08 Agentic workflows | `undraw_ai-agent_pdkp.svg` | `auto 45%` |

Position is `82% 85%` everywhere. The size varies because the illustrations have different aspect ratios; within a deck, the title slide and all H1 section dividers use the same values.

The index hero is `undraw_vibe-coding_mjme.svg` (shared with deck 06).

## Styling

- Site (HTML pages) uses the `zephyr` Bootswatch theme. Default zephyr colors; no custom palette right now.
- Slides use reveal.js's `default` theme + `slides/custom.scss`. The SCSS is intentionally minimal: just the title-slide layout and section-divider positioning.
- Title slide: title block pinned to the top-left via a `.title-slide-inner` wrapper (custom partial + absolute positioning). Reveal's centering is overridden with `top: 0 !important; height: 100% !important` on `#title-slide`.
- Section divider slides (any `<section>` with an H1 as a direct child) get the same centering override plus `margin-top: 5%` on the H1. The `:has()` selector keeps the rule from affecting the title slide (whose H1 is inside `.title-slide-inner`).

## Available skills

- `.claude/skills/workshop-time-estimate/SKILL.md`: estimates total workshop time by summing countdowns, counting non-exercise slides (1-2 min each), and counting demo slides (`## Demo`) at 5-8 min each, then comparing against the schedule table in `index.qmd`. Trigger by asking about time budget or whether there's enough content.

## Operating notes

- `quarto preview` is typically started by Julia in a separate terminal, not by Claude. Wiping `docs/` and `.quarto/` is the right move when stale builds cause weirdness (e.g., old font imports lingering after SCSS changes).
- Local-only workflow: there is no `.devcontainer/` and no Codespaces wiring on purpose.
- The repo is git-initialized. Julia makes her own commits and PRs; never commit or push on her behalf, stage or prepare changes and stop there.

## Per-user preferences

- No em dashes in any file content, commit messages, or PR text (shareable artifacts). Use commas, semicolons, parens, or two sentences. En dashes and hyphens are fine.
- Julia prefers iterating in small steps with previews; do not make large structural changes without checking in first.
