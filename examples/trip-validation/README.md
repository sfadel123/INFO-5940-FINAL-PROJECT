# Trip validation example

These files reproduce the examples in `tech-env.md` section 8. They demonstrate deterministic validation endpoints: business logic separate from HTTP handling, typed requests and responses, and corresponding tests. Routes, fields, and rules can be customized while retaining that pattern.

From the repository root, using Python 3.12:

```sh
cd examples/trip-validation
python3.12 -m venv /tmp/info5940-trip-validation-venv
source /tmp/info5940-trip-validation-venv/bin/activate
python -m pip install fastapi 'pydantic>=2,<3' httpx pytest
python -m pytest test_trip.py
```

These examples do not implement itinerary generation, the new five-day limit, or model/search orchestration. Orchestration will need separate timeout and error-handling patterns during Construction. The team will run these three tests and report the result; no passing result is claimed here.
