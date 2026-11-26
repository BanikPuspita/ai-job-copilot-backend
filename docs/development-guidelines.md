# Development guidelines

Two people work in this repository at the same time. The foundation on `main` is shared. Feature work stays on the branch that owns it until it is reviewed.

## Branches

| Branch | Purpose |
| --- | --- |
| `main` | Stable integrated code. Do not commit feature work directly here. |
| `feature/profile-kb` | Personal Knowledge Base, CV upload, and profile extraction |
| `feature/job-intelligence` | Job posting analysis, matching, and application-question answers |

Create a feature branch from an up-to-date `main`:

```powershell
git checkout main
git pull
git checkout -b feature/profile-kb
```

or:

```powershell
git checkout -b feature/job-intelligence
```

Keep branches current by merging or rebasing `main` into the feature branch regularly. Open a pull request into `main` when a slice is ready. Do not create extra long-lived branches without agreeing first.

Browser automation, authentication, and deployment are out of scope until the team explicitly starts them.

## Folder responsibilities

- `app/api` — HTTP only. No SQL and no calls to Ollama from a route.
- `app/schemas` — Pydantic models for the API boundary.
- `app/services` — use-case logic. LLM calls go through `OllamaService`.
- `app/repositories` — SQLAlchemy queries.
- `app/models` — table definitions.
- `app/core` — settings, engine, session, and shared errors.
- `tests` — one test module per behavior, named `test_<subject>.py`.

Name modules, functions, and variables in `snake_case`. Name classes in `PascalCase`. Prefer a full word over an abbreviation (`profile_repository`, not `prof_repo`).

## Shared interfaces

These files affect both developers. Change them only when both people know about the change, and land that change on `main` before building more feature code on top of it:

- `app/core/config.py`
- `app/core/database.py`
- `app/core/exceptions.py`
- `app/services/ollama.py`
- `app/api/v1/router.py`
- `alembic/env.py`
- `requirements.txt` and `requirements-dev.txt`

A feature branch may add a new router, model, schema, repository, or service without waiting, as long as it does not rename or repurpose a shared type.

If both branches need the same table or the same schema field, agree on the name in a short note or pull request before either side migrates it.

## Commits

Use a short imperative subject and say why the change exists.

```text
Add profile repository for CV facts

Knowledge-base routes need a single place to read stored profile data.
```

Keep commits focused. Do not mix a schema migration with an unrelated formatting pass. Do not commit `.env`, virtual environments, or caches.

## Pull requests

- Point the pull request at `main`.
- Describe what changed and how to test it.
- Include the Pytest command you ran.
- Call out migrations, new environment variables, and any edit to a shared interface.
- Keep the pull request reviewable. Split unrelated work.

## Tests and lint

Before opening a pull request:

```powershell
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

New behavior needs a test. Default tests must run without PostgreSQL and without Ollama. Mark a test that needs a real database so the default suite can skip it.

Use type hints on new functions. Ruff is the formatter and linter; do not add a second formatter.

## Configuration and secrets

Read configuration through `get_settings()`. Do not hardcode database passwords, model hosts, or origins in feature code. Add every new variable to `.env.example` and the README table in the same change.

## Dependencies

Add a package only when the foundation or a feature cannot proceed without it. Pin it in `requirements.txt` (or `requirements-dev.txt` when it is only used in development). Do not add paid AI APIs.
