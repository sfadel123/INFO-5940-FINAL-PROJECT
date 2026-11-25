# Existing Example: API Documentation

## POST /api/v1/trip-duration

Purpose: calculate inclusive trip length.

Request fields: `start_date` and `end_date`, parsed as Python dates by the TripDates Pydantic model.

Example request:

```json
{"start_date": "2026-12-01", "end_date": "2026-12-03"}
```

Successful response: HTTP 200 with `{"days": 3}`. TripDuration constrains days to an integer >=1.

Reversed-date response: HTTP 422 with `{"detail": "End date must be on or after start date."}`. Framework request-validation errors use FastAPI's validation behavior; runtime behavior has not been independently exercised in this stage.

## Internal API

`trip_length_days(start_date: date, end_date: date) -> int`: raises ValueError for reversed dates, otherwise returns `(end_date - start_date).days + 1`.

`validate_trip_dates(trip: TripDates) -> TripDuration`: wraps the function and translates its ValueError into HTTPException.

## Boundaries

No five-day maximum, future-date rule, budget, timezone, session, model/search orchestration, chat route, or feedback route is implemented. Planned `/api/v1/chat` and `/api/v1/feedback` are not existing endpoints.
