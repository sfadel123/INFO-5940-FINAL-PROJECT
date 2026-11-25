# Existing Example: Business Overview

## Scope and evidence

This analysis covers only `examples/trip-validation/`, created before Inception as a standalone transcription of the approved technical document's section 8. The travel planner is a new product, not an existing implemented service. No travel-planner functionality is claimed here.

## Business context (text representation)

A caller submits a start and end date to the example API. The API calls a pure date function. The caller receives an inclusive trip length or an invalid-date error. No external services or persistent data participate.

## Implemented business transaction

Calculate trip duration: accept two dates, reject an end date earlier than the start, and return the number of calendar days including both endpoints. This is the only implemented transaction.

## Business dictionary

- Start date: first calendar date of the trip.
- End date: last calendar date of the trip.
- Inclusive duration: date difference plus one day; same-day trips therefore have one day.

## Components

- `rules.py`: date ordering and inclusive duration calculation.
- `main.py`: typed HTTP input/output and conversion of the business error to HTTP 422.
- `test_trip.py`: three example checks, not demonstrated passing in this workflow.

## Planned versus existing

Chat, Ollama, Tavily, itinerary generation, five-day enforcement, budgets, scheduling, feedback, baseline matching, sessions, and KPI logging exist only as approved plans in README.md, vision.md, and tech-env.md. No implementation or successful integration is asserted.
