# Technical Environment Document — Personalized Cultural Travel Planner

## 1. Project Technical Summary

Our project is a personalized travel-planning application that helps travelers discover cultural activities aligned with their interests, travel dates, and budgets. Users will describe their trip and interests to a chatbot, receive a daily itinerary with supporting source links, and request revisions.

| Item | Planned approach |
| --- | --- |
| Project type | Greenfield: a new application |
| Team size | Six members |
| Primary runtime | Local development on team laptops |
| Cloud hosting provider | None |
| Deployment model | Local Python web application and local Ollama server |
| Coding agent | OpenAI Codex |
| Development methodology | AI-DLC v1.0.1 |

The team has selected Python. The architecture will prioritize a small number of dependencies and clearly separated responsibilities so members can understand, test, and maintain the application together.

For the mid-semester milestone, we will complete Inception and stop before Construction.

## 2. Programming Languages and Package Management

| Language/tool | Version or convention | Purpose |
| --- | --- | --- |
| Python | 3.12 | Backend, search integration, and LLM interaction |
| HTML and CSS | Standard browser-supported features | Chat and itinerary interface |
| JavaScript | Minimal browser-side code | Submit requests and update results |
| pip | Version documented during setup | Install Python dependencies |
| venv | Python standard library | Isolate each developer's environment |

Python will be the only backend language. Additional backend languages are outside the initial scope because they would introduce separate tooling without a demonstrated project need.

During Construction, tested package versions will be pinned in requirements files. Virtual environments will not be committed to GitHub.

## 3. Frameworks and Libraries

| Framework/library | Planned use | Rationale |
| --- | --- | --- |
| FastAPI | Backend HTTP endpoints | Supports typed request validation and API documentation |
| Pydantic v2 | Input and output schemas | Validates user preferences and model-generated structures |
| Uvicorn | Local application server | Runs the FastAPI application |
| Jinja2 | HTML templates | Keeps the interface within the Python project |
| OpenAI Python client | Calls to Ollama | Uses the selected OpenAI-compatible API |
| Tavily Python SDK | External activity searches | Provides a search interface for retrieving activity sources |
| pytest | Automated tests | Tests application rules and failure cases |
| HTTPX / FastAPI TestClient | API tests | Exercises endpoints without starting a separate application server |

FastAPI supports both [Jinja2 templates](https://fastapi.tiangolo.com/advanced/templates/) and [testing with pytest and TestClient](https://fastapi.tiangolo.com/tutorial/testing/).

The proposed search service is Tavily. The team will review its account requirements, usage limits, and any costs before implementation. Its Python interface supports searches and returns information that can be used as source material. [Tavily documentation](https://docs.tavily.com/documentation/api-reference/endpoint/search)

### Prohibited libraries and approaches

These are project-specific scope decisions, not claims that the tools are generally unsuitable.

| Library or approach | Reason for exclusion from the MVP | Alternative |
| --- | --- | --- |
| LangChain, LangGraph, and CrewAI | Additional orchestration abstractions are unnecessary for the initial bounded workflow | Explicit Python-guided stages with bounded model/tool proposals |
| Selenium or Playwright for scraping external websites | Browser scraping adds maintenance and site-access complications | Search API results and official venue sources |
| Direct model hosting through PyTorch or Transformers | Duplicates the role of Ollama | Ollama's API |
| Payment and booking SDKs | Payments and direct reservations are outside the MVP | Links to original activity or booking pages |

A new dependency or external service must have a documented purpose, maintenance/license review, and discussion during a team meeting or pull request. Changes to the agreed environment will be reflected in this document through the AI-DLC workflow.

## 4. LLM, External Services, and Local Deployment

The planned model is Qwen3 4B, using the Ollama identifier `qwen3:4b`, called with the OpenAI Python client through Ollama's OpenAI-compatible API. Its suitability, tool calling, quality, and runtime performance will be tested during Construction, including on an M3 MacBook Air with 8 GB of memory. Model suitability has not yet been verified. Qwen3 8B (`qwen3:8b`) is the fallback on a laptop with more memory. [Model reference](https://ollama.com/library/qwen3:4b)

| Component | Planned location |
| --- | --- |
| Web application | `http://127.0.0.1:8000` |
| Ollama OpenAI-compatible endpoint | `http://localhost:11434/v1/` |
| User interface | Browser on the same laptop |
| Activity search | External Tavily service over HTTPS |
| Currency-rate retrieval | Planned automated download of official ECB daily reference data over HTTPS; runtime integration verified during Construction |

The OpenAI Python client will connect to Ollama using the placeholder key `ollama`, which the local server ignores. This connection does not require a paid OpenAI API key. [Ollama documentation](https://docs.ollama.com/api/openai-compatibility)

The product will run locally but will require internet access for live activity searches. No cloud application hosting, containers, or public deployment are required for the MVP.

External services are the planned search provider, the team-selected [European Central Bank reference-rate download](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html), and GitHub for collaboration. AD4=A explicitly replaces the earlier planned WSJ source after its automated access remained unverified. Use the published structured rate data; no browser scraping, access bypass, invented rates or silent provider substitution. Cache a dated snapshot per trip and reuse it for revisions. Published data is not proof of a working application integration; download/parsing and failures must be checked during Construction. No paid provider account is assumed. Additional services still require team review.

## 5. Architecture and Development Patterns

The application will use a single Python application divided into modules, rather than independently deployed services.

Responsibilities will be separated into:

- Preferences: validate destination, dates, budget, currency, and interests.
- Search: retrieve candidate activities and preserve source information.
- LLM integration: send bounded prompts and process model/tool responses.
- Itinerary: organize activities, validate constraints, and handle revisions.
- Currency conversion: preserve budget input/currency, retrieve validated ECB reference-rate data, convert comparable amounts to USD, and expose source/date and unavailable-rate status.
- Interface/API: display the chat, results, errors, and source links.

The approved coordination approach is a Python-guided flow: the model proposes content at defined steps, and Python controls execution. Generation and revision use one open HTTP request with a waiting indicator, without a background-job/status API.

The intended flow is:

1. Gather required trip preferences, allow up to three additional interest-clarification turns, and require confirmation of a valid preference summary. Missing/invalid fields still require correction.
2. Let the model propose activity-search queries.
3. Validate and execute permitted searches in Python.
4. Provide retrieved information to the model.
5. Validate and display the itinerary.
6. Apply requested revisions to thumbs-down activities while preserving locked and unaffected activities and all preferences.

The model may request the defined search tool, but it will not be allowed to execute arbitrary code, shell commands, or unrestricted network requests. Maximum trip length is 5 days. The initial generation and all revisions of the same trip share up to 2 activity searches per trip day, capped at 10 in total, with up to 5 results each. Once exhausted, revisions use retrieved candidates only. Retries cannot reset or exceed the allowance. These limits apply only to activity searches; the separate system baseline search does not count toward them.

### API conventions

- JSON endpoints will use the `/api/v1/` prefix. Planned endpoints are `POST /api/v1/chat` (send a message and receive the chatbot's reply) and `POST /api/v1/feedback` (rate an activity).
- URLs will use lowercase, hyphen-separated words.
- JSON fields and Python functions will use `snake_case`.
- Dates will use ISO format: `YYYY-MM-DD`.
- Budgets will include an explicit currency.
- Pydantic will validate request and response structures.
- Invalid inputs will return HTTP 422.
- Ordinary model/activity-search failures allow one automatic retry within configured limits; persistent failures show a safe error and retry action while preserving the last valid itinerary and inputs. No invented substitute results. Baseline failure stops new generation as described below.
- The browser sends the random session ID with each request. The backend validates that every source ID in a submitted itinerary or revision belongs to that session and rejects any that do not.

### Trip, budget, and scheduling conventions

- The English interface accepts any single destination. Trips cover one traveler for 1–5 inclusive days and start today or later in destination local time; reversed dates are invalid. Target 2 to 4 activities per day. When there are too few suitable, distinct activities, show fewer, state how many were found, suggest broadening interests, and never invent activities.
- One total activity budget covers tickets and fees for the whole trip for one traveler. Flights, lodging, meals, and local transport are excluded. The user selects the budget currency, default USD. Preserve that original amount/currency, and convert both the budget and verified activity prices into USD for comparison and totals. Show conversion labels, source, and rate date; converted amounts are estimates.
- Unknown prices or prices without a valid conversion are labeled "unverified," flagged, and excluded from verified totals, never treated as verified zero costs. Do not claim full budget compliance when prices or budget conversion are unverified. If the budget itself cannot be converted, pause generation/revision with retry/correction guidance, preserving inputs and any accepted itinerary. Confirmed preference changes require a new trip.
- Use a dated positive finite ECB rate snapshot, at most seven calendar days old at use; reject future/undated data. Normalize EUR-based quotes to USD per source-currency unit from the same snapshot. USD identity needs no external rate. Coverage is USD plus currencies with valid published rates; unsupported activity conversions remain unverified, and destination coverage is separate from currency coverage.
- Pin the snapshot for the trip and reuse it for revisions. Recheck freshness; stale rates must not silently reprice fixed activities. A confirmed new trip can obtain a fresh snapshot. Compare unrounded decimal amounts; display USD cents with half-up rounding and round the subtotal only after summing unrounded values. Retain original amounts, source/date and estimate labels.
- All activity times use the destination's local time zone. Use source-provided durations when available; otherwise estimate from activity type and similar activities, label the estimate, and require a positive duration that fits the remaining schedule. No fixed 30–180-minute range applies.
- Activities must not overlap. Leave a 30-minute buffer between activities and schedule them between 9:00 AM and 10:00 PM. Respect opening hours when known; otherwise label hours "unverified." Route optimization remains out of scope. Time-limited events require retrieved evidence of an occurrence during the trip; omit events with incompatible or unconfirmed dates.

### Local recommendation baseline

Run a separate system Tavily search for "top things to do in [destination]" once per itinerary generation, returning up to 10 results as the baseline. This search does not count toward the activity-search limit and is not subject to the five-results-per-activity-search limit. Cache the baseline in server memory for the session so revisions reuse it rather than running another baseline search. The cached baseline is cleared with the session sources when the server restarts. At most one activity per itinerary may match that baseline. An activity counts as local if it is absent from the baseline and meets at least one criterion:

- Independent (not a chain).
- A time-limited event (pop-up, class, festival).
- Found through a local source: local news, city or venue event listings, or community organizations.

The model must cite its evidence, and Python checks baseline overlap by name and URL. Baseline evidence can include provider-returned page content when available, as well as titles, snippets, and URLs; no browser scraping or invented attraction names. If no usable baseline is available, stop generation with an explanation and retry action. Every activity other than the permitted baseline overlap must meet the local criteria.

### Data and recommendation conventions

The MVP will not require accounts or a database. Server memory owns the confirmed preferences, accepted itinerary, ratings/locks, retrieved sources, baseline, rate snapshot, counters, version and request receipts. A random session ID is created at bootstrap and sent with subsequent requests. The browser holds only an in-memory display/input copy; it cannot restore source authority or change fixed trip state. No localStorage or persistent cookies are introduced. Reloading starts a fresh flow. Clear the old session on confirmed new trip and all sessions on restart; expire inactive sessions after two hours, excluding active operations. Unknown, cross-session or expired source references are rejected.

Mutating commands include request_id and expected_version. Allow one mutation per session; identical request replays return the prior outcome without repeating searches/counts, while conflicting payloads or stale versions receive a conflict. Preserve consumed search counts and successful caches on failure. Concrete contracts and approved text/call/output/deadline limits are documented in [Application Design](aidlc-docs/inception/application-design/application-design.md); detailed schemas and implementation remain Construction work.

Each recommended activity must reference a source retrieved by the application. Python code will resolve validated session-owned source identifiers into URLs rather than accepting arbitrary model-generated citations.

Unknown prices, hours, or availability will be labeled as unverified. Search results and source links do not guarantee factual accuracy, so users will be directed to confirm details with the venue.

Feedback has only thumbs up or down and an optional preset reason: "too touristy," "too expensive," "wrong time," or "not my interest." No free-text feedback is collected. A thumbs-down marks an activity without immediate replacement. Clicking "Update itinerary" or asking in chat replaces only thumbs-down activities. A thumbs-up locks an activity. Unaffected activities and all preferences stay unchanged. If no replacement fits remaining constraints, keep the original visibly marked as disliked and explain the shortfall. Chat may propose changed preferences as a new trip, but requires confirmation before discarding the old itinerary/session and creating a fresh session/baseline.

During team evaluation rounds, persist only anonymous data per itinerary: a random itinerary ID, number of activities, number of revision requests, number of baseline overlaps, link-check results, and activity ratings. Store this in the local JSON Lines file `ratings.jsonl`, listed in `.gitignore`, never committed, and deleted after the final demo. Do not persist destinations, travel dates, budgets, chat text, or session IDs in that file. KPIs are not measured with live users.

Direct booking, persistent profiles, calendar integration, route optimization, social-media scraping, and multi-city or group trips are outside scope.

## 6. Security and Privacy Requirements

We will use the following project-specific security checklist as the risk framework for this local MVP. These controls are planned for Construction; they are not claims of completed security verification.

| Risk category | Planned control |
| --- | --- |
| Exposed credentials | Store API keys in runtime environment variables; exclude local secret files from Git; commit only dummy example configuration |
| Unnecessary personal-data collection | Collect only trip preferences; no payment, passport, home-address, or account credentials |
| Disclosure through search queries | Send only destination, dates, and relevant search interests; do not send entire conversations |
| Malicious retrieved text or prompt injection | Treat retrieved content as untrusted data; enforce tool permissions in Python |
| Unsafe generated output | Validate structured responses; escape displayed text; restrict source links to HTTP/HTTPS |
| Excessive requests or resource use | Bound input sizes, search calls, retries, and model output; apply timeouts |
| Unintended network access | Bind local services to loopback interfaces; do not expose the unauthenticated demo publicly |
| Sensitive logging | Log request identifiers, timings, and error categories rather than complete travel profiles or credentials; evaluation records contain only the anonymous fields listed in section 5 |
| Feedback privacy | No free-text feedback; use only the four preset reasons; ignore `ratings.jsonl` in Git and delete it after the final demo |
| Source provenance | Keep retrieved sources in server memory by random session ID; reject source IDs outside that session; clear sources on server restart |
| Dependency vulnerabilities | Review dependencies before adoption and updates; use pip-audit during Construction and before the demo |

Account authentication is not included because this is a single-user local demonstration without persistent accounts. Per-session source ownership checks remain required. Any later public or multi-user deployment will require a new security review.

Local loopback communication may use HTTP. External service communication must use HTTPS. Apart from the anonymous evaluation records and ratings described above, the application will not intentionally persist traveler data, so database encryption is not applicable to the initial design.

The optional Security Baseline and Resiliency Baseline extensions are disabled by the team (C5=B and Q17=B); the project-specific controls above remain required.

## 7. Testing Requirements

| Test type | Scope | Tools |
| --- | --- | --- |
| Unit | Date validation, budget checks, source mapping, and preference handling | pytest |
| API | Request validation, response structures, and error behavior | FastAPI TestClient |
| Integration | Ollama and search-service adapters | Controlled live checks during Construction |
| User-flow | Chatbot conversation → itinerary → revision | Manual browser testing with documented scenarios |
| Security | Malicious source content, invalid inputs, secret exposure, and unsafe links | Automated tests and review |

Routine automated tests will mock external model, search, and currency-rate responses. Internal business logic will be tested directly.

The team enabled partial property-based testing for pure functions and serialization round-trips. Carry PBT-02/03/07/08/09 into later design and Construction: round-trip/invariant tests, domain-aware generators, shrinking, reproducible seeds, CI integration, and an appropriate framework selected through team review. Other PBT rules are advisory. No framework has been selected or installed by this document.

The initial target is at least 80% line coverage for deterministic preference-validation and itinerary-validation modules, measured with pytest-cov. Coverage will supplement meaningful tests rather than replace them.

Evaluation will use 10 sample traveler profiles across 3 destinations during team evaluation rounds, not with live users. The team selected New York City, London, and Paris, with ten approved synthetic fixtures distributed 4/3/3 in [Application Design](aidlc-docs/inception/application-design/application-design.md). Use final itineraries only for activity-based KPIs, count each final activity once with its latest rating, retain full revision counts, report failures separately, and report empty denominators as N/A. Profiles will vary interests, budgets, and dates. For each itinerary, log only a random itinerary ID, activity count, revision-request count, baseline-overlap count, link-check results, and activity ratings in `ratings.jsonl` as described in section 5.

| KPI | Numerator | Denominator | Target |
| --- | --- | --- | --- |
| Activity approval rate | Thumbs-up ratings | Rated activities | At least 70% |
| Revision rate | Itineraries needing more than two revision requests | Test itineraries | Under 30% |
| Local-discovery rate | Activities absent from the baseline and meeting the local criteria | All recommended activities | At least 70% |
| Source coverage | Activities whose source link loads in an automated check | All recommended activities | 100% |

After each test round, the team will calculate these KPIs and check relevance, source traceability, treatment of unknown details, and preservation of constraints during revisions. Automated link loading checks measure source coverage; they do not establish factual accuracy.

Tests will not require identical LLM wording across runs. Instead, they will check structured properties and failure handling.

The UI scope is desktop Chrome and Safari with chat alongside day-grouped cards, keyboard-operable controls, visible focus, readable contrast, text rating labels, and clear progress/errors. Mobile-specific testing is out of scope.

During Construction, unit and API tests must pass before merging changes. Live integration and browser checks must pass before the final demo. Model latency and memory use will be measured on the demonstration laptop before establishing a realistic performance target.

## 8. Example Code and Conventions

The following examples establish a small validation pattern: business logic is separate from HTTP handling, requests are typed, and errors are tested.

They belong in a standalone `examples/trip-validation/` folder, with an explanation of how to run them. They illustrate conventions rather than implement itinerary generation. The examples below are unchanged from the supplied draft's code; they do not implement the new five-day trip limit.

### Example function — rules.py

```python
from datetime import date


def trip_length_days(start_date: date, end_date: date) -> int:
    """Calculate the inclusive trip length."""
    if end_date < start_date:
        raise ValueError("End date must be on or after start date.")

    return (end_date - start_date).days + 1
```

### Example endpoint — main.py

```python
from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from rules import trip_length_days

app = FastAPI()


class TripDates(BaseModel):
    start_date: date
    end_date: date


class TripDuration(BaseModel):
    days: int = Field(ge=1)


@app.post("/api/v1/trip-duration", response_model=TripDuration)
def validate_trip_dates(trip: TripDates) -> TripDuration:
    try:
        days = trip_length_days(trip.start_date, trip.end_date)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return TripDuration(days=days)
```

### Example tests — test_trip.py

```python
from datetime import date

from fastapi.testclient import TestClient

from main import app
from rules import trip_length_days

client = TestClient(app)


def test_trip_length_includes_both_dates():
    assert trip_length_days(
        date(2026, 12, 31),
        date(2027, 1, 2),
    ) == 3


def test_endpoint_returns_trip_duration():
    response = client.post(
        "/api/v1/trip-duration",
        json={
            "start_date": "2026-12-01",
            "end_date": "2026-12-03",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"days": 3}


def test_endpoint_rejects_reversed_dates():
    response = client.post(
        "/api/v1/trip-duration",
        json={
            "start_date": "2026-12-03",
            "end_date": "2026-12-01",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == (
        "End date must be on or after start date."
    )
```

The example's README explains that this pattern applies to deterministic validation endpoints. Developers may customize the route, fields, and business rules while retaining typed validation and corresponding tests. It does not demonstrate the model/search orchestration, which will require separate timeout and error-handling patterns.

The team will run these examples with pytest and report the result. No passing test result is claimed. From `examples/trip-validation/`, after installing the dependencies described in its README, run `python -m pytest test_trip.py`.

## 9. Applicability and Changes

Brownfield inventories, migration plans, cloud regions, production infrastructure, and message queues are not applicable to this greenfield local MVP.

The team reviewed the initial input before Inception. Revisions incorporate recorded Requirements Analysis and approved Application Design answers AD1–AD6; the generated design artifacts have a separate review gate. Any later changes to the model, search provider, framework, scope, or security constraints will be discussed and recorded through the shared AI-DLC workflow.
