# Existing Example: Interaction Flows

Text sequence representations provide the complete interactions without requiring a diagram renderer.

## Successful duration transaction

1. Caller sends date fields to POST /api/v1/trip-duration.
2. FastAPI/Pydantic parses TripDates.
3. validate_trip_dates calls trip_length_days.
4. trip_length_days returns inclusive duration.
5. Endpoint returns TripDuration, serialized as JSON.

## Reversed-date transaction

1. Caller sends a start date later than the end date.
2. Parsed TripDates reaches the endpoint.
3. trip_length_days raises ValueError.
4. Endpoint catches it and raises HTTPException with status 422 and the message.
5. Caller receives an error response.

## Test interactions

The direct unit test checks a date range crossing a year boundary. Two TestClient tests check a successful API response and a reversed-date error. No tool-call, search, storage, or LLM interactions exist in the example.
