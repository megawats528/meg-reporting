# meg-reporting
meg playground for reporting on agentic workstreams


# Daily Chat Report — Automated pipeline


This repository runs a daily job that ingests Unity chat traces, clusters user messages into themes, and produces a human-friendly "themes + insights + learnings" Markdown report. It can optionally call an LLM to polish insights and post a short summary to Slack.


## What you get
- `daily_chat_report.py` — main pipeline (loading, embedding, clustering, summarization)
- `send_to_slack.py` — optional helper to post summary to Slack
- `.github/workflows/daily-report.yml` — scheduled GitHub Actions job
- `requirements.txt` — pinned Python deps
- `.env.example` — environment variable template


## Setup
1. Create a new GitHub repo and push the files from this scaffold.
2. Add the following **Repository Secrets** (Settings → Secrets → Actions):
- `OPENAI_API_KEY` (optional, only if you want LLM polishing)
- `SLACK_BOT_TOKEN` (optional, for Slack delivery)
- `SLACK_CHANNEL` (e.g. `#product-insights`)
- `UNITY_API_TOKEN` (if you want the workflow to pull traces via API)
- `UNITY_API_URL` (base URL or endpoint to fetch traces, if used)
3. Edit `daily_chat_report.py` fetch_from_api() with your Unity API contract if you prefer direct pulls. If not, upload traces into the repo `input/` folder before the run (or use an artifact/upload step).
4. Adjust schedule in `.github/workflows/daily-report.yml` (cron uses UTC).


## CI behavior
- Workflow runs at the cron schedule and executes `daily_chat_report.py`.
- Output artifacts are uploaded for inspection. The script will write `output/daily_chat_report_{DATE}.md`.
- If `OPENAI_API_KEY` is present, the script will call the LLM to produce polished titles/insights.


## Security notes
- Keep secrets in GitHub Secrets or a Vault; do not commit them.
- Redact PII before embedding. The pipeline includes a `redact_text()` placeholder you can replace with your company tool.


## Extending
- Replace BERTopic with your preferred clustering approach if desired.
- Replace the embedding model with a private or on-prem model for extra privacy.


---
