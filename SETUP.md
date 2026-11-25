# Setup

## Install

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), fork this repo, clone your fork and run `uv sync`. Open the repo folder itself in VS Code, so the agent finds `.vscode/mcp.json`, `.mcp.json`, `AGENTS.md` and `.claude/`.

## Gemini API key

Get a free key at <https://aistudio.google.com/apikey>, then:

```bash
cp .env.example .env        # paste your key into .env
uv run python api_key.py    # checks that it works
```

In your code, use `from api_key import load_api_key`. Never commit `.env`. A `GEMINI_API_KEY` environment variable also works.

## Free-tier limits

`gemini-embedding-2` allows about **1,000 texts a day** (each text in a batch counts), per Google Cloud project, reset at midnight Pacific time (09:00 in Spain). Check yours at <https://ai.dev/rate-limit>.

A 50,000-word corpus in 150-word chunks is about 420 texts. Each new chunking costs another full index; changing k, filters or search method does not. Every question your server or evaluation embeds also counts. Save each vector as soon as you get it, so a crash or the daily limit loses nothing.

## MCP server in your editor

`.vscode/mcp.json` and `.mcp.json` register `server.py` as `corpus`. Check its tools in Copilot (Agent mode, tools icon) or Claude Code (`/mcp`).

For Copilot, select `corpus-researcher-copilot` from the agent picker. Its native
profile in `.github/agents/` permits only `corpus/search`. The separate Claude
profile in `.claude/agents/` uses Claude's `mcp__corpus__search` tool name.
Verify the actual tool picker shows only corpus search selected before the demo.
The reusable demonstration prompt is in `eval/copilot_demo_prompt.txt`.

Search returns citation-first readable passages to editor models and an identical
structured payload to application clients. After changing `server.py`, restart
the editor's corpus server through **MCP: List Servers** before trying it again.
Both unedited Copilot exports are preserved at
`eval/copilot_transcript_attempt1.json` and `eval/copilot_transcript_attempt2.json`.
The second was captured after restarting the editor server with the readable
result revision. Each interaction made three searches and received relevant
passages with exact citations, but the editor model still declined to answer.
Neither attempt demonstrates a successful cited answer.

## Dependencies

`uv add <package>`, then commit `pyproject.toml` and `uv.lock`.

## Check your submission

```bash
uv run python check.py              # key, index, test set, both tools, one answer
uv run python check.py --evaluate   # also runs main.py evaluate
```

It does not rebuild the index. A failure here is a failure for the grader too. The same check runs on GitHub: on your fork, enable Actions, add the `GEMINI_API_KEY` secret, and run **Verify Assignment 3**.
