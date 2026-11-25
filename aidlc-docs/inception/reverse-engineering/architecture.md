# Existing Example: Architecture

## System overview

One standalone Python example directory, with a FastAPI application, a pure rule function, and tests. It is not an installed/distributed package and is not the planned travel planner.

## Architecture (text representation)

HTTP caller -> FastAPI route in main.py -> trip_length_days in rules.py -> typed JSON response.

TestClient in test_trip.py invokes the API in process. One test invokes the rule function directly.

## Components and types

- Application/model: `main.py`, containing `app`, `TripDates`, `TripDuration`, and `validate_trip_dates`.
- Business utility: `rules.py`, containing `trip_length_days`.
- Tests: `test_trip.py`, containing three pytest test functions.

## Data flow

1. FastAPI/Pydantic receives and parses date fields.
2. The endpoint calls the pure rule function.
3. Ordered dates produce an inclusive integer duration, wrapped in TripDuration.
4. Reversed dates raise ValueError, translated to HTTP 422.

## Integration and infrastructure

No model client, search client, database, persistent store, deployment script, container, cloud resource, or network topology is implemented. HTTPX/TestClient is a test dependency. The approved product plan specifies local execution; this review did not launch a server.
