# Existing Example: Dependencies

## Internal dependency graph (text representation)

`main.py` -> `rules.py` (runtime).

`test_trip.py` -> `main.py` and `rules.py` (test).

## External dependencies

| Dependency | Version evidence | Usage | License verification |
| --- | --- | --- | --- |
| FastAPI | Not pinned | Application, HTTPException, TestClient | Not performed in this source review |
| Pydantic | >=2,<3 in example README | BaseModel and Field | Not performed in this source review |
| HTTPX | Not pinned; named in setup | TestClient dependency | Not performed in this source review |
| pytest | Not pinned; named in setup | Test discovery/execution | Not performed in this source review |

Python's datetime is a standard-library dependency. No dependency manifest or lockfile is present. Dependency/license review and tested version pinning remain planned Construction work; no unsupported license claims or compatibility guarantees are made here.
