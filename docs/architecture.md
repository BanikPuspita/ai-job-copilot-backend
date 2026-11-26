# Backend architecture

The backend is a modular FastAPI application. This document describes the foundation that both feature branches build on. Product behavior is not implemented yet.

## Request flow

```text
Client
  -> FastAPI route          app/api/v1
  -> Pydantic schema        app/schemas
  -> Service                app/services
  -> Repository             app/repositories
  -> SQLAlchemy model       app/models
  -> PostgreSQL

A service may also call OllamaService when it needs a local model.
```

Route handlers stay thin. They validate input, call a service, and return a response schema. SQL queries belong in repositories. Prompts and model calls belong in services, with HTTP access to Ollama going through `OllamaService` only.

## Package responsibilities

| Package | Responsibility |
| --- | --- |
| `app/main.py` | Create the app, CORS, exception handlers, and the public root routes |
| `app/api/v1` | Version 1 routers. New feature routers are registered in `router.py` |
| `app/core` | Settings, the SQLAlchemy engine and session, shared HTTP errors |
| `app/schemas` | API input and output models |
| `app/models` | Persistence models only |
| `app/repositories` | Queries and writes against a session |
| `app/services` | Use-case logic and the shared Ollama client |
| `app/utils` | Small helpers with no feature ownership |

## Configuration

`app/core/config.py` is the only place that reads environment variables. Other modules call `get_settings()`. Defaults are safe for local development. Secrets stay in `.env`, which is not committed.

## Database

`app/core/database.py` owns the engine, session factory, and `get_db()` dependency. `Base` is the single declarative base. Alembic loads `Base.metadata` from `alembic/env.py`.

Importing the application does not connect to PostgreSQL, and startup does not create tables. Schema changes ship as Alembic revisions.

When a model module is added, import it from `app/models/__init__.py`. That import is what makes the table visible to autogenerate.

## Ollama

`app/services/ollama.py` is the shared local-LLM boundary. It reads `OLLAMA_BASE_URL` and `OLLAMA_MODEL` from settings and talks to Ollama's HTTP API.

Today the service can only check connectivity with `GET /api/tags`. Text generation and structured JSON generation will be added on this class so feature modules do not each invent their own client. If Ollama is down, `check_availability()` returns a failed status. It does not run during startup, and the API still boots.

Do not add OpenAI, Anthropic, or other paid model SDKs.

## API versioning

Public product routes live under `/api/v1`. The unversioned `/` and `/health` routes identify the process for local development and simple probes. Breaking API changes go to a new version prefix rather than changing a released contract in place.

## What is intentionally absent

- CV upload and parsing
- Personal Knowledge Base tables and services
- Job posting extraction and matching
- Cover letters, tailored CVs, and application answers
- Playwright or any browser automation
- Authentication

Add those as feature modules that plug into the packages above. Do not place them in `app/main.py` or `app/core`.

## Independent feature work

`feature/profile-kb` and `feature/job-intelligence` can add their own models, schemas, repositories, services, and routers. They share `Settings`, `Base`, `get_db()`, `OllamaService`, and `api_router`. Changes to those shared pieces need agreement from both developers before they land on `main`.
