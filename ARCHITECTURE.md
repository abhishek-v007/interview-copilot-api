# Architecture

Phase 1 of the interview copilot backend is a FastAPI service that turns an interview question into a suggested answer via a dedicated LLM service (Gemini today).

## Boundaries

This service owns HTTP APIs and AI processing only. It does **not** include frontend, Electron, WebSockets, audio, Deepgram, VAD, authentication, payments, Redis, or S3.

PostgreSQL and SQLAlchemy are scaffolded so later phases can persist data without restructuring. The Phase 1 answer path does not open a database session.

## Layout

| Path | Responsibility |
| --- | --- |
| `app/main.py` | App factory, lifespan, exception handlers |
| `app/api/` | HTTP routes and dependency injection |
| `app/api/v1/` | Versioned API (`/api/v1`) |
| `app/core/` | Settings, logging, domain errors |
| `app/schemas/` | Pydantic request/response contracts |
| `app/services/interview.py` | Interview use-case (prompt + response mapping) |
| `app/services/llm/service.py` | Dedicated LLM service |
| `app/services/llm/gemini.py` | Gemini SDK adapter |
| `app/db/` | Engine, session factory, declarative base |
| `app/models/` | Future ORM models (empty in Phase 1) |
| `tests/` | Pytest suite with a fake LLM |

`GET /health` is mounted at the application root. Interview routes live under `/api/v1`.

## Request flow

```text
Client
  → POST /api/v1/interview/answer
    → Interview endpoint (HTTP)
      → InterviewService
        → LLMService
          → GeminiProvider
            → Gemini API
```

The HTTP layer never imports the Gemini SDK. Routes depend on `InterviewService` only.

## LLM abstraction

- `LLMProvider` — raw `generate(prompt) -> LLMResult`
- `LLMService` — calls the provider and returns `{answer, key_points}`
- `GeminiProvider` — Phase 1 implementation of `LLMProvider`

`get_llm_provider()` is the only place that constructs Gemini. Tests inject a fake provider through FastAPI dependency overrides.

The Gemini API key is loaded from the environment, omitted from settings `repr`, redacted from logs, and never included in HTTP responses.

## Configuration and startup

Settings are loaded from environment variables (and `.env` locally) via `pydantic-settings`.

On startup, if `APP_ENV` is not `test`, the app fails fast when `GEMINI_API_KEY` is missing. The database engine is created lazily and is not required to boot.

## Error mapping

| Condition | HTTP |
| --- | --- |
| Invalid request body / empty question | 422 |
| LLM timeout or Gemini failure | 502 |
| Unexpected error | 500 (no stack trace in the response) |

Logs include question length, whether a role was present, key-point count, and latency. Full question text and the API key are not logged.

## Out of scope for Phase 1

WebSockets, audio ingestion, Deepgram, VAD, auth, payments, Redis, S3, Alembic migrations, and persisting Q&A rows.
