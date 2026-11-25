# Unit of Work — Cultural Travel Planner

Status: Generated Units artifact explicitly approved by the team with "approve and finish inception ", recorded 2026-11-25T02:27:53Z. Units Generation and Inception are complete. Work stopped before Construction; implementation and runtime verification remain future work.

## 1. Unit definition

| Field | Definition |
| --- | --- |
| Unit ID and name | U01 — Cultural Travel Planner |
| Boundary | The entire local modular application, including the desktop UI, Python backend, adapters and team evaluation support |
| Business outcome | Help one traveler plan a short, interest-matched cultural trip from retrieved evidence, review costs/scheduling, and revise only disliked activities |
| Story allocation | All US-01 through US-17, each assigned once to U01; 59 existing acceptance scenarios remain authoritative |
| Quality scope | All 19 functional requirements and six NFRs, plus the recorded disposition of DEF-01–DEF-07 |
| Deployment | One local FastAPI application; local Ollama is an external runtime dependency, not another application unit |
| Team ownership | Shared by the team under UG1=A; work divided in team meetings, with no permanent named module owners |
| Later implementation | One application-unit Construction loop when separately requested; internal modules may be worked on as smaller tasks |

This follows the [approved unit plan](../plans/unit-of-work-plan.md), [Application Design](application-design.md), [requirements](../requirements/requirements.md) and [stories](../user-stories/stories.md). The installed Units rule groups a monolith into one application unit with internal modules. Nine modules are neither nine microservices nor nine independently deployed units.

The user-facing personas remain Recent Graduate, Abroad Student and Cultural Explorer. Team Evaluator is the separate evaluation role, not a new account type, dashboard or independently deployed product.

## 2. Included capabilities and boundary

U01 includes conversational intake and explicit preference confirmation; bounded discovery and cached baseline retrieval; evidence-grounded itinerary proposals; deterministic locality, date/time, budget and source validation; accessible day cards; preset feedback and controlled revisions; confirmed new trips; ephemeral server sessions; and anonymous team evaluation/cleanup support.

The approved rules remain unchanged:

- One traveler and one destination, one to five inclusive destination-local days. Target two to four distinct activities per day; show fewer or zero honestly, with the actual count and broadening guidance.
- Activity searches across the initial generation and all revisions share `min(2 * trip_days, 10)` attempts, at most five results each. The separate baseline returns up to ten results, is outside that allowance and is cached for revisions.
- At most one activity overlaps the evidenced baseline. Every other activity needs a cited qualifying local criterion; Python checks source ownership, name/URL overlap and deterministic constraints.
- Schedule within 09:00–22:00 destination-local time, without overlaps, with a 30-minute buffer. Respect known hours and evidenced event dates; label unknown hours and estimated durations.
- The budget covers one traveler's whole-trip activity tickets/fees. Preserve original amounts/currencies and use the approved pinned ECB snapshot for estimated USD comparison. Missing budget conversion pauses work; unknown/unconvertible activity prices are flagged and excluded from the verified subtotal.
- Thumbs down only marks an activity; an explicit update replaces eligible disliked activities. Thumbs up locks, and neutral activities/preferences remain unchanged. Confirm a new trip before changing preferences or clearing the old session.
- Server memory owns trip state, evidence, baseline/rates, counters, votes and request guards. Browser memory is a display/input copy. Restart, confirmed reset and the approved idle-expiry rule clear session authority.
- Team evaluation uses the ten approved New York City/London/Paris profiles, final snapshots/latest ratings and agreed denominators. Persist only the six approved anonymous field groups; never commit ratings.jsonl and delete it after the final demo.

The detailed bounds, error meanings, rate policy, fixtures and lifecycle remain in the approved [design](application-design.md), [method contracts](component-methods.md) and [service flows](services.md). This document does not replace or relax them.

Outside U01's MVP scope: multi-city/group trips, accounts or saved profiles, production/cloud hosting, social-media scraping, route optimization, flights/lodging/meals/transport planning, booking/payments, and an evaluator dashboard. Model/provider verification is future work, not an additional feature or a new unit.

## 3. Internal modules and responsibilities

The component IDs remain the module IDs. Shared support code is part of U01, not a tenth business module. Each module has shared team ownership; the primary module in the story map denotes technical responsibility only.

| Module | Responsibility | Owned interface/data boundary | Explicit restriction |
| --- | --- | --- | --- |
| C01 Desktop UI/API | Render chat/cards, waiting/errors and accessible controls; accept typed commands | HTTP routes and sanitized TripView/OperationResult display | Calls C03; browser copies cannot authorize mutations or source ownership |
| C02 Preferences | Validate required input, local dates and activity-budget scope; confirm valid summaries | Pure PreferenceDraft/ConfirmedPreferences rules | No external retrieval or mutable session access |
| C03 Trip coordinator | Sequence intake, generation, feedback, revision, new trips and evaluation | Application operations; passes immutable context and commits through C08 | Python controls tools and limits; only validated results may be accepted |
| C04 Model adapter | Interpret interests/evidence and propose bounded queries/schedules | Typed proposals through the OpenAI client and local Ollama | No direct search, code execution, source authority or state mutation |
| C05 Search/evidence adapter | Execute permitted Tavily baseline/activity requests | EvidenceBatch with provider result rank, URLs and available evidence | Does not assign session authority, change quotas or silently retry outside permits |
| C06 Currency | Acquire dated ECB data and provide separately callable pure arithmetic | RateSnapshot/availability and original-plus-USD conversion results | Validation may use only pure arithmetic, never rate-fetching side effects |
| C07 Itinerary validation | Check evidence, locality, distinctness, schedule/budget and preserved revision fields | Immutable ValidationContext to ValidationReport | No network, files or live store access; uses C06 pure arithmetic only |
| C08 Ephemeral sessions | Own preferences, accepted result, votes/locks, sources, pinned caches, quotas, version and receipts | Coordinator-only operation guards, reservations, registration and commit/reset interfaces | No database/browser persistence; failures do not refund consumed searches |
| C09 Team evaluation | Check eligible links, project anonymous records, calculate KPIs and support cleanup | Validated final snapshot input; six-field record projection; bounded link/file effects | No raw chat/profile persistence, live-user telemetry or new account/dashboard |

The [dependency artifact](unit-of-work-dependency.md) defines allowed internal calls and external boundaries. The [story map](unit-of-work-story-map.md) allocates stories, requirements and future verification without duplicating user stories.

## 4. Code organization strategy

These are approved planning locations under the repository root, not files created by Inception. Preserve `examples/trip-validation/` as the separate existing teaching example; do not move, import it as production planner code, or expand its tests during this stage.

| Planned location | Module or purpose |
| --- | --- |
| `src/travel_planner/main.py` | Startup/composition wiring for the single local application |
| `src/travel_planner/contracts.py` | Shared typed commands, proposals, context, views and evaluation projections |
| `src/travel_planner/config.py` | Runtime configuration access; secrets remain environment variables |
| `src/travel_planner/web/` | C01 HTTP boundary |
| `src/travel_planner/templates/` and `src/travel_planner/static/` | C01 Jinja2, CSS and minimal JavaScript |
| `src/travel_planner/preferences.py` | C02 pure preference rules |
| `src/travel_planner/coordinator.py` | C03 orchestration |
| `src/travel_planner/adapters/model.py` | C04 Ollama adapter |
| `src/travel_planner/adapters/search.py` | C05 Tavily adapter |
| `src/travel_planner/currency/` | C06 rate acquisition separated from pure arithmetic |
| `src/travel_planner/validation/` | C07 deterministic itinerary rules |
| `src/travel_planner/sessions.py` | C08 process-memory session store |
| `src/travel_planner/evaluation/` | C09 pure metrics/record projection separated from link/file operations |
| `tests/unit/` and `tests/api/` | Later deterministic and mocked API verification |
| `tests/integration/` | Later integration checks; routine checks use fakes, live runs are deliberate |
| `tests/property/` and `tests/fixtures/` | Later partial PBT and reusable synthetic inputs; framework still deferred |
| `config/`, if a file is needed | Nonsecret configuration only |
| `aidlc-docs/` | Workflow documentation only; never application code |
| `ratings.jsonl` at the repository root | Future local anonymous evaluation output; ignored, never committed, deleted after demo |

Shared contracts/configuration do not import module implementations. Startup wiring may instantiate modules and supply their dependencies; it does not bypass the request-time graph. Keep pure C06/C09 operations separable from their I/O interfaces. Exact helper files, schemas, injection mechanics and dependency manifests are later design/code-plan work; no versions, framework or package setup is selected here.

## 5. Ownership and coordination

UG1=A explicitly retains shared team ownership. The team divides specific work at meetings and reviews the results together; no permanent owner for C01–C09 is invented. Sophia remains the designated shared-session operator. That role does not assign all implementation, evaluation or technical decisions to her.

Internal module contracts provide manageable task boundaries within U01. Coordinate changes to shared contracts, canonical session state and cross-module invariants together. The approved dependency order is documented in the dependency artifact; it is not a schedule, an automatic parallel-agent assignment or a new workflow per teammate.

## 6. Later verification and readiness boundary

U01 carries all NFRs. Keep Python 3.12, pip/venv, FastAPI, Pydantic v2, Uvicorn, Jinja2 and minimal JavaScript. Planned qwen3:4b via Ollama/OpenAI client and fallback qwen3:8b remain subject to actual Construction measurements and suitable hardware. Tavily entitlement, ECB ingestion, tested dependency versions/licenses and the PBT framework still need their recorded later checks.

After a later explicit Construction request, revisit the approved outlook: Functional Design, NFR Requirements, NFR Design, minimal local Infrastructure Design, Code Generation, then Build and Test. This is one per-unit loop for U01. Integration and browser checks, actual evaluation rounds and demo cleanup remain future obligations. Do not treat an Inception document check as a passing application test or achieved KPI.

The unit definition, module/code organization, dependencies, story/requirement mapping and deferred verification work are documented and validated. Separate generated-artifact approval was received at 2026-11-25T02:27:53Z; it is distinct from the earlier UG2 plan approval.

## 7. Extension applicability

Security Baseline and Resiliency Baseline: N/A, disabled by the team's C5=B and Q17=B. Their extension rules are skipped; project-specific privacy, bounds and failure requirements still apply. Partial PBT remains enabled only for pure functions and serialization round-trips.

| Rule | Current Units status | Rationale / later obligation |
| --- | --- | --- |
| PBT-01 | N/A | Advisory in partial mode; detailed property identification belongs to Functional Design |
| PBT-02 | N/A | No serialization code/tests generated; shared contracts and C09 record projection retain round-trip obligations |
| PBT-03 | N/A | No pure implementations/tests generated; C02/C06/C07 and pure C09 functions retain invariant obligations |
| PBT-04 | N/A | Advisory; request-idempotency semantics remain later functional/example checks |
| PBT-05 | N/A | Advisory; no oracle implementation created |
| PBT-06 | N/A | Advisory; no mandatory stateful/live-model PBT is added |
| PBT-07 | N/A | Domain generators and reusable strategies are later test work |
| PBT-08 | N/A | Shrinking, failure seeds and CI integration remain Construction obligations |
| PBT-09 | N/A | Framework selection/configuration remains DEF-05 for later NFR/design |
| PBT-10 | N/A | Advisory; the 59 story scenarios and complementary example tests remain required |

No applicable extension blocker. This applicability record makes no implementation or test-success claim.

## 8. Final approval boundary

The team explicitly approved this definition, the dependency artifact and the story map with "approve and finish inception ", recorded 2026-11-25T02:27:53Z. This final approval is separate from UG1/UG2. G7, Units Generation and Inception are complete. Work has stopped before Construction; no implementation, commit or push is authorized or performed by this completion.
