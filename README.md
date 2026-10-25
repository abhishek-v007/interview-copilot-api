# Interview Copilot API

Backend API and AI processing for the interview copilot. This repository contains **only** the FastAPI service — no frontend or Electron code.

Phase 1 implements a single flow: **question → Gemini → answer**.

## Requirements

- Python 3.11+
- A Gemini API key
- PostgreSQL is configured but **not used** by the Phase 1 answer path

## Setup

```bash
cd interview-copilot-api
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env
```

On macOS/Linux, activate with `source .venv/bin/activate` and copy env with `cp .env.example .env`.

Set `GEMINI_API_KEY` in `.env`. The key is never returned to clients and is redacted from logs.

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

OpenAPI docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Liveness check |
| `POST` | `/api/v1/interview/answer` | Generate an interview answer |

### Example

```bash
curl -X POST http://127.0.0.1:8000/api/v1/interview/answer ^
  -H "Content-Type: application/json" ^
  -d "{\"question\": \"Tell me about yourself\", \"role\": \"Flutter Developer\"}"
```

```json
{
  "answer": "...",
  "key_points": []
}
```

## Tests

Tests use a fake LLM provider. They do not call Gemini.

```bash
pytest
```

## Configuration

See [`.env.example`](.env.example). Important variables:

- `APP_ENV` — `development`, `test`, or `production`
- `LOG_LEVEL` — stdlib log level
- `GEMINI_API_KEY` — required when `APP_ENV` is not `test`
- `GEMINI_MODEL` — default `gemini-2.0-flash`
- `GEMINI_TIMEOUT_SECONDS` — provider timeout
- `DATABASE_URL` — SQLAlchemy URL (scaffold only in Phase 1)

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md).
