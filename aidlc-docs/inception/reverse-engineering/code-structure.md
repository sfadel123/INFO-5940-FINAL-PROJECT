# Existing Example: Code Structure

## Inventory

| File | Purpose |
| --- | --- |
| examples/trip-validation/rules.py | Pure date-validation function |
| examples/trip-validation/main.py | FastAPI endpoint and two Pydantic models |
| examples/trip-validation/test_trip.py | One rule test and two API tests |
| examples/trip-validation/README.md | Manual virtual-environment setup and test instructions |

## Module hierarchy (text representation)

`main` imports `rules`; `test_trip` imports `main` and `rules`. Tests require the example directory to be importable, as the example README's working-directory instructions provide.

## Build system

No pyproject.toml, requirements file, lockfile, package.json, or build pipeline is present. The example README describes Python 3.12, venv, and manual pip installation. It specifies Pydantic >=2,<3; other example dependency versions are not pinned.

## Patterns

Typed HTTP boundary with business logic in a separate pure function. Endpoint catches the rule's ValueError and returns an HTTP-specific error. TestClient exercises the route without a separate running server.

## Preservation

These files are untracked at workflow start and are preserved unchanged. No code edits or tests were requested for this Inception stage. Root approved input documents and existing .gitignore are also preserved.
