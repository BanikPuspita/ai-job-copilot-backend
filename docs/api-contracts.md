# API contracts

Interactive documentation is generated from the FastAPI routes and Pydantic response models.

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI schema: `/openapi.json`

Update this file when a feature adds or changes a public endpoint. The OpenAPI schema stays the detailed source of request and response fields. This document records the conventions and the endpoints that exist today.

## Versioning

- Product endpoints live under `/api/v1`.
- `/` and `/health` are unversioned process endpoints.
- A breaking change to a released endpoint requires `/api/v2` rather than a silent change to `/api/v1`.
- Additive optional fields are allowed on an existing response when clients can ignore them.

## Naming

- Paths use lowercase plural nouns: `/api/v1/profiles`, `/api/v1/job-postings`.
- Use HTTP methods for actions: `GET` reads, `POST` creates, `PATCH` partially updates, `DELETE` removes.
- Put a verb in the path only when the call is a real action, such as `/api/v1/job-postings/{id}/match`.
- JSON fields use `snake_case`, matching the Pydantic model field names.

## Requests and responses

- Define a Pydantic schema for every request body and response body.
- Do not return SQLAlchemy models directly.
- Error responses use FastAPI's `detail` field. `AppError` in `app/core/exceptions.py` is the shared way to raise an expected HTTP error from a service.
- List endpoints should later accept `limit` and `offset` and return a consistent envelope. That envelope is not needed for the current health routes.

## Endpoints available now

### `GET /`

Returns application information.

```json
{
  "name": "AI Job Application Copilot",
  "environment": "development",
  "version": "0.1.0",
  "docs": "/docs"
}
```

### `GET /health`

Process health. This does not check PostgreSQL or Ollama.

```json
{
  "status": "ok",
  "service": "api"
}
```

### `GET /api/v1/health`

Versioned process health. Same guarantee: no database or model call.

```json
{
  "status": "ok",
  "service": "api-v1"
}
```

## Adding an endpoint

1. Add the request and response schemas under `app/schemas`.
2. Put the use case in a service. Put queries in a repository when the database is involved.
3. Add a thin route and include its router from `app/api/v1/router.py`.
4. Document the path, method, and purpose in this file.
5. Add a Pytest test that does not require a live database unless the test is explicitly marked as an integration test.

## Future contracts

CV upload, knowledge-base reads, job ingestion, matching, and generated documents will each get their own section here when the endpoint exists. Do not document a request body for a feature that has no route yet.
