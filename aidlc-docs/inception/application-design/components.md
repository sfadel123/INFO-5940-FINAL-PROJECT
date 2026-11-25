# Application Components

Status: Application Design artifacts approved by the team with "approve & continue", recorded 2026-11-25T02:02:35Z. Units Generation may begin. No implementation, integration, performance or test success is claimed.

## Architecture and scope

One local modular Python application serves a desktop browser and calls local Ollama plus external Tavily/ECB adapters. AD1=A gives Python control of the sequence; the model supplies proposals within that sequence. AD2=A uses a single open request for generation or revision with a waiting indicator, not a job queue. These are logical components in one deployment, not separately deployed services.

The existing trip-validation example remains a standalone teaching example and is neither altered nor represented as the planner. Application code will later live outside aidlc-docs. Formal unit/module organization belongs to Units Generation; no teammate assignments are invented here.

## Component catalog

| ID | Component / purpose | Responsibilities | Interface boundary |
| --- | --- | --- | --- |
| C01 | Desktop UI and HTTP boundary | Jinja2 page, chat/day cards, accessible controls, typed commands, safe display, HTTP error mapping | Browser sends commands to /api/v1/; routes call C03 and return a sanitized TripView/OperationResult |
| C02 | Preferences | Validate required fields, destination-local dates, budget/currency and confirmed summary; track optional clarification count | Pure validation of PreferenceDraft/ConfirmedPreferences; no external searches or persistence |
| C03 | Trip coordinator | Intake, confirmation, bounded generation, feedback, targeted updates, confirmed new trips and explicit evaluation completion | Application service invoked by C01; coordinates C02 and C04–C09; owns sequencing rather than accepting model-selected arbitrary actions |
| C04 | Model adapter | Bounded calls to planned qwen3:4b through OpenAI Python client/Ollama; interpret interests, propose queries, extract candidates and draft schedules | Receives bounded typed task context; returns validated structural proposals or typed failure; cannot fetch sources or mutate state |
| C05 | Search/evidence adapter | Tavily baseline/activity requests; preserve result rank, title, URL and available evidence | Receives a Python-issued search permit and query; returns EvidenceBatch; coordinator registers session-owned source IDs |
| C06 | Currency adapter and arithmetic | Obtain dated ECB reference data, report availability, derive USD rates, preserve original amounts and estimated conversion labels | Network acquisition is separate from pure conversion/rounding functions; returns RateSnapshot/ConversionResult |
| C07 | Itinerary validation | Grounding, baseline matching/locality evidence, distinctness, schedule/budget rules, unchanged-preference and revision checks | Pure functions consume an immutable ValidationContext and proposal; return ValidationReport/validated snapshot, with no network or file writes |
| C08 | Ephemeral session store | Confirmed preferences, accepted itinerary, ratings/locks, source registry, baseline, rate snapshot, counters, request receipts, version and active-operation guard | Access only by server coordinator; atomic reservations/commits; clear on reset/restart/expiry; browser is not authority |
| C09 | Team evaluation | Bounded source-link checks, final-snapshot metrics, anonymous record serialization, explicit ratings-file writing and cleanup support | Receives validated final snapshot; returns EvaluationResult; only agreed anonymous fields may enter ratings.jsonl |

Detailed contracts are in [component-methods.md](component-methods.md); orchestration is in [services.md](services.md); dependencies/data flow are in [component-dependency.md](component-dependency.md).

## Ownership and trust

C08 is authoritative for preferences, quotas, locks, accepted activities and evidence. The browser holds an in-memory display/input copy and sends the session identifier; no browser copy can restore cleared sources or change canonical preferences during a revision. C04/C05 outputs remain untrusted until typed validation and evidence checks succeed. Every activity citation is resolved through the session source registry, not through a URL supplied by the model.

Retrieved evidence can support an assertion but does not establish guaranteed venue availability or factual correctness. Python checks source ownership/excerpt presence and deterministic constraints; team evaluation checks recommendation quality. No account authentication is added to this loopback-only local demo.

C03 commits an accepted itinerary only after all final invariants pass. Failed attempts preserve the last accepted itinerary and preferences while retaining actual consumed-search counts and cached successful retrievals. Rollback must not refund external calls. C09 writes only when the team deliberately completes an evaluation; normal traveler interaction has no telemetry write.

## Cross-cutting constraints

- Python 3.12, pip/venv, FastAPI, Pydantic v2, Uvicorn, Jinja2 and minimal JavaScript remain the stack. qwen3:8b remains a planned fallback requiring suitable hardware and Construction evidence.
- Follow the approved bounds and lifecycle in [application-design.md](application-design.md). Keep client retries visible to the coordinator so library-level retries cannot exceed product limits.
- Keep secrets in runtime environment variables. API responses and diagnostic logs exclude secrets, full prompts and raw traveler profiles. Source text is escaped and retrieved instructions cannot change tool permissions.
- Preserve the project's no-framework/no-browser-scraping/no-booking constraints. ECB is a structured reference-data download, not a browser scraper. No additional external provider is selected.
- C02/C06/C07 and shared serialization contracts provide the scope for later partial PBT; network/model calls are mocked in routine tests. No framework, dependency version or runtime benchmark is selected here.
