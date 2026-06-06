# Choosing a Model

An R demo for the "Choosing a model" section of deck 02 (Programming with LLMs).
It sends the same prompt to several providers and compares the answers, latency,
and token usage. The key idea: switching providers is a **one-string change**,
`chat("anthropic/...")` vs `chat("openai/...")` vs `chat("google_gemini/...")`.

## Why this is an instructor demo

Comparing providers needs API keys for more than one provider. Workshop
participants only have **Anthropic** set up, so this runs as an instructor demo:
you run it from your own machine with several providers configured, and
participants watch. (The comparison table still makes the point with Anthropic
alone, since it spans the Haiku / Sonnet / Opus tiers.)

## Requirements

- R, with the `ellmer` package (plus Quarto if you want to render rather than
  run the chunks live).
- API keys for whichever providers you want to compare, read automatically from
  your `.Renviron`: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`, and
  so on. Comment out any provider you have not set up. Ollama needs a local
  server.

## Running

Open `02-models.qmd` and run the chunks interactively (Positron or RStudio), one
at a time, so you can show each provider's response and then the side-by-side
comparison table. Model ids change over time; adjust the strings to models you
currently have access to.

## Credit

Adapted from [work by Garrick Aden-Buie](https://github.com/posit-conf-2025/llm/tree/main/_solutions/07_models).

## License

MIT License, see the LICENSE file for details.
