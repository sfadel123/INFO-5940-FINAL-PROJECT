# Unit of Work Dependencies

Status: Generated Units artifact explicitly approved by the team with "approve and finish inception ", recorded 2026-11-25T02:27:53Z. Units Generation and Inception are complete. Work stopped before Construction; implementation and runtime verification remain future work.

## 1. Unit-level dependency matrix

A row depends on a column. A dash means no dependency on another application unit; internal module calls are listed separately below.

| Dependent unit | U01 |
| --- | --- |
| U01 — Cultural Travel Planner | - |

There is exactly one application unit. U01 does not depend on a second application unit and has no self-dependency. The browser UI, backend and evaluation support belong to U01. Local Ollama, external providers and the ratings file are runtime/data boundaries, not extra units or separate Construction loops.

See the [unit definition](unit-of-work.md), [story map](unit-of-work-story-map.md), approved [component dependencies](component-dependency.md) and [service flows](services.md).

## 2. Internal module dependency matrix

This matrix preserves the approved component matrix exactly. A row calls a column through typed in-process interfaces. D is an ordinary internal call; P is the pure currency arithmetic interface only. A dash means no direct runtime call.

| Caller | C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C01 UI/API | - | - | D | - | - | - | - | - | - |
| C02 Preferences | - | - | - | - | - | - | - | - | - |
| C03 Coordinator | - | D | - | D | D | D | D | D | D |
| C04 Model | - | - | - | - | - | - | - | - | - |
| C05 Search | - | - | - | - | - | - | - | - | - |
| C06 Currency | - | - | - | - | - | - | - | - | - |
| C07 Validation | - | - | - | - | - | P | - | - | - |
| C08 Session store | - | - | - | - | - | - | - | - | - |
| C09 Evaluation | - | - | - | - | - | - | - | - | - |

Text interpretation: C01 calls C03. C03 coordinates C02 and C04–C09. C07 may use C06's pure arithmetic. Other modules have no direct dependency on another business module. The graph is acyclic; the dependency is not a permission for C07 to download rates. A shared listing URL or cached model proposal never establishes independent source authority.

Shared contracts and runtime configuration are support definitions inside U01. They must not import business-module implementations. Startup wiring can instantiate and inject implementations, but it cannot bypass the request-time boundaries. Browser code calls C01's HTTP routes, not internal Python modules directly. No message broker, internal service-to-service HTTP, shared-package release process or independently deployed module is introduced.

## 3. Contract handoffs and state ownership

| Handoff | Data crossing the boundary | Enforcement / failure responsibility |
| --- | --- | --- |
| Browser to C01 to C03 | Typed command, session ID after bootstrap, request ID and expected version | C01 validates the envelope; C03 applies operation routing/guards through C08; browser snapshots are not authoritative |
| C03 to C02 | Draft/summary and explicit destination-local date context | Pure valid/invalid preference result; required fields and confirmation cannot be invented |
| C03 to C04 | Bounded task context and permitted evidence | Typed proposals only; invalid/truncated structure fails safely and cannot commit state |
| C03 to C05 | Python-issued search permit and permitted query | Return EvidenceBatch; no hidden retrieval outside baseline/activity allowances |
| C03 to C08 | Source batches, reservations, validated result and operation outcome | C08 assigns source ownership, retains canonical state and atomically controls counters/version/commit |
| C03 to C06 | Rate-acquisition request or pure conversion inputs | Dated snapshot/availability or conversion result; unsupported budget blocks generation/revision under AD5 |
| C03 to C07 | Immutable ValidationContext and initial/revision proposal | All constraints must pass before commit; validate source ownership and preserve fixed revision fields |
| C07 to C06 | Money and supplied immutable RateSnapshot | Pure conversion only; no provider or store access |
| C03 to C09 | Validated final snapshot with latest votes and actual revision count | C09 checks eligible links and serializes only the six-field projection; no raw traveler profile is persisted |
| C03 to C01 | Safe OperationResult/TripView | Display approved uncertainty, shortfalls, errors and allowed actions without raw caches or secrets |

C08 owns confirmed preferences, the accepted itinerary, votes/locks, sources, baseline, rate snapshot, consumed quotas and request receipts. C03 obtains context and passes immutable snapshots to validators/evaluation. Adapters do not mutate C08 directly; C01 does not bypass C03 to read or write it. No cyclic back-reference to the coordinator is required.

Only validated itinerary changes commit. Failure retains the last accepted content, consumed search attempts and successful caches; it does not refund external calls. Replayed identical requests return the retained outcome; changed payloads under a reused ID and stale versions produce conflict. A confirmed new trip, server restart or approved expiry clears the old session authority. Exact lock/receipt algorithms remain DEF-04.

## 4. External, storage and runtime dependencies

| U01 module | Boundary | Role and limits | Remaining verification |
| --- | --- | --- | --- |
| C01 | Desktop Chrome/Safari and local FastAPI/Uvicorn | Same-origin loopback requests and Jinja2/minimal-JavaScript UI; open generation/update request with a waiting indicator | Keyboard, focus, labels, errors and complete browser flows |
| C04 | Local Ollama through the OpenAI Python client | Planned qwen3:4b; qwen3:8b fallback only after suitability/hardware verification; bounded model requests | DEF-06 quality/latency/memory and fallback hardware; DEF-07 tested dependency compatibility |
| C05 | Tavily over HTTPS | Separate baseline up to ten results; activity attempts use the cumulative trip allowance and up to five results each | DEF-07 account/quotas/cost/access, provider results and retry accounting |
| C06 acquisition | Official ECB structured daily data over HTTPS | Dated trip snapshot; reuse during revisions, check freshness and preserve approved currency labels/policy | DEF-02 actual retrieval/parsing and DEF-03 arithmetic/freshness/failure checks |
| C09 link checks | Retrieved session-owned public HTTP/HTTPS source links | Bounded availability checks; reject unsafe/private/local targets and unsafe redirects; no browser scraping | DEF-04 exact link bounds plus failure/redirect handling |
| C08 | Process memory | Canonical session state/caches only; clear on restart/reset/expiry | Isolation, races, receipts, expiry and consumed-quota retention |
| C09 record I/O | Repository-root ratings.jsonl | Explicit final-evaluation write/upsert of only approved anonymous fields; ignored and deleted after demo | Allowlist, one record per itinerary ID, replay behavior, file-update/cleanup verification |

Source availability is not factual verification, and a documented provider format is not a working integration. No live dependency is needed for routine unit/API tests: supply typed fakes and deterministic fixtures at the adapter boundary. Controlled live checks and actual team evaluation belong to later Construction.

Runtime configuration is shared within U01; secrets remain environment variables and do not enter browser output, Git or diagnostic content. Python 3.12/pip/venv and the approved framework stack remain unchanged. No extra provider, queue, database, package manager or cloud resource is added by this map.

## 5. Future integration order within U01

This is the approved plan's dependency order, not an implementation schedule or a new Construction authorization. Relevant checks accompany each part.

1. Establish shared contracts/configuration and pure C02/C06/C07 rules; keep C09's pure record/metric transformations separately testable. C06 arithmetic precedes its C07 use.
2. Define isolated C08 session operations and C04/C05/C06/C09 external or file boundaries, with fakes for routine verification. Provider availability is not required to validate contracts.
3. Integrate C03 with these boundaries and immutable context; verify confirmation, search reservations, commit/failure behavior, targeted updates and new-trip guards.
4. Connect C01 to C03 through the approved journeys, with accessible controls, safe rendering and open-request waiting/error handling.
5. Connect final-snapshot evaluation and verify the complete flow, including the allowlisted record, KPI denominators, source checks and cleanup instructions. Perform deliberate live/model/browser evaluation only after the relevant prerequisites are checked.

The exact method/error schemas, concurrency mechanics, source/prompt/link numeric bounds and test implementation remain later Functional/NFR/code-planning tasks. The future per-unit stage sequence still applies once to U01; these internal collaboration steps do not bypass it or create separate workflows per teammate.

## 6. Verification and approval scope

The one-unit matrix has no inter-unit edges. The nine-module matrix matches the approved design and is acyclic; the sole validation-to-currency dependency is marked pure. Shared support, provider boundaries and session ownership do not add hidden reverse calls. Story/requirement coverage and later verification are in the story map.

New unit artifacts use tables and text. The already-approved component diagrams remain available in component-dependency.md; no new diagram renderer or visual validation claim is needed here. Current document checks are distinct from runtime/provider tests.

Security/Resiliency extensions remain disabled; partial PBT applicability and each rule's later obligation are recorded in unit-of-work.md. No applicable extension blocker is introduced by these boundaries. The team approved all three generated unit artifacts with "approve and finish inception ", recorded 2026-11-25T02:27:53Z. Inception is complete and work has stopped before Construction.
