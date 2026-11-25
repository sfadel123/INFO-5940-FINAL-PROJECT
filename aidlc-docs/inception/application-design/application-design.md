# Application Design — Personalized Cultural Travel Planner

Status: Application Design artifacts approved by the team with "approve & continue", recorded 2026-11-25T02:02:35Z. Units Generation may begin. No implementation, integration, performance or test success is claimed.

## 1. Decision basis and scope

The team approved Python-guided orchestration (AD1), an open request with waiting UI (AD2), New York City/London/Paris and ten fixtures (AD3), ECB daily reference data replacing WSJ (AD4), pausing when budget conversion is unavailable (AD5), and the listed design defaults (AD6). The later question about download effort and Asia requested explanation; it did not change those answers. Actual inputs/answers and timestamps are preserved in [audit.md](../../audit.md) and the [design plan](../plans/application-design-plan.md).

Keep one local modular Python 3.12 application, FastAPI/Pydantic v2/Uvicorn, Jinja2 and minimal JavaScript. Planned qwen3:4b runs through the OpenAI Python client and local Ollama; qwen3:8b is a fallback requiring Construction evidence and appropriate hardware. Tavily remains the planned search provider. No cloud deployment, accounts/database, saved profiles, group/multi-city trips, route optimization, social scraping, booking/payment integration, job queue or orchestration framework is added.

This design supplies interfaces and high-level rules. Exact schema implementations, algorithms, clients, tests and dependency pinning belong to Construction. Units Generation follows only after design approval. Stop after Units Generation approval.

## 2. Artifact index

| Artifact | Content |
| --- | --- |
| [components.md](components.md) | Nine logical responsibilities, interfaces, ownership and trust boundaries |
| [component-methods.md](component-methods.md) | Shared types, public operations, method signatures and error meanings |
| [services.md](services.md) | Intake, generation, feedback/revision, new-trip, failure and evaluation flows |
| [component-dependency.md](component-dependency.md) | Dependency matrix, provider/storage boundaries, data-flow diagrams and text alternatives |
| This document | Consolidated design, approved rules/defaults, fixtures, coverage, remaining work and review boundary |

## 3. Components, dependencies and interfaces

| Component | Main responsibility | Direct internal calls |
| --- | --- | --- |
| C01 UI/API | Desktop chat/cards and typed request/response boundary | C03 |
| C02 Preferences | Required-field/date/budget validation and confirmation | None |
| C03 Coordinator | Python-controlled sequencing and mutation boundaries | C02, C04, C05, C06, C07, C08, C09 |
| C04 Model | Bounded interpretation, query/candidate/schedule proposals | None; local Ollama only |
| C05 Search | Baseline/activity retrieval and evidence batches | None; Tavily only |
| C06 Currency | Dated rate acquisition and separate pure conversion functions | None; ECB acquisition only |
| C07 Validation | Deterministic evidence, locality, schedule/budget and preservation checks | C06 pure arithmetic only |
| C08 Session store | Ephemeral canonical trip/evidence/counters/receipts | None |
| C09 Evaluation | Safe link checks, anonymous final records and metrics/cleanup support | None; eligible public links and local ratings file |

These dependencies are acyclic; internal components communicate through typed function calls, not network services. C03 registers C05 results with C08 and supplies immutable ValidationContext values to C07. C04 cannot call providers, execute code, authorize a state change or manufacture an authoritative source URL. All accepted activity citations resolve to retrieved, session-owned SourceRecord entries.

Shared contracts include CommandMeta, PreferenceDraft, ConfirmedPreferences, SourceRecord/Baseline, RateSnapshot, CandidateActivity/ScheduledActivity/Itinerary, RatingCommand, ValidationContext/ValidationReport, SessionSnapshot/TripView, OperationResult and EvaluationRecord. The method artifact defines their ownership and input/output expectations.

Public operations are GET /, session bootstrap, chat, confirm-preferences, generate, feedback, update-itinerary, confirm-new-trip and explicit evaluation completion under /api/v1/. Only bootstrap lacks an existing session ID. Mutating commands include request ID and expected state version. Invalid inputs return 422; proposed stale-session/conflict/provider mappings distinguish expiry, concurrent changes and external failures. Generation/revision keeps one request open and shows a waiting indicator; no polling job contract is added.

## 4. Service flow and invariants

1. **Intake:** collect valid destination/country/time zone, dates, total activity budget/currency and interests. Allow at most three additional interest-clarification turns after required fields are collected. Missing/invalid fields still need correction. Show and explicitly confirm a valid summary before generation.
2. **Generation:** guard the session/version, establish usable budget conversion and baseline, propose/execute allowed searches, register evidence, draft candidates/schedule, validate the complete result, then commit. Return fewer/zero suitable activities honestly with counts and an interest-broadening suggestion.
3. **Feedback:** persist the latest vote only in active server memory unless the team later completes evaluation. Thumbs down marks, thumbs up locks; neither triggers replacement. Preset reasons only.
4. **Revision:** an explicit button/chat update targets only currently disliked activities. Freeze all preferences and locked/neutral activity fields; reuse cached baseline/rates and cumulative search allowance. A missing replacement stays visibly disliked. Operation failure preserves the whole last valid itinerary.
5. **New trip:** stage preference changes and require confirmation before clearing old state. A fresh session then collects/confirms valid preferences and has fresh caches/allowance. No confirmation means no reset.
6. **Evaluation:** deliberate team completion captures final activities/latest ratings and full update-request count, checks links, and writes only the anonymous record projection. Final-demo cleanup deletes the local file later.

The scheduling validator enforces 1–5 inclusive future/live days in destination-local time; 2–4 distinct activities/day is a target, four/day is the cap. Every interval fits 09:00–22:00, with no overlaps and at least 30 minutes between activities. Respect known opening hours or show unverified; use a source duration when available or a visibly labeled positive estimate that fits. No fixed 30–180-minute estimate range. Time-limited events require sourced occurrence within trip dates. No travel-time or route guarantee is implied.

The baseline uses one separate system query for `top things to do in [destination]`, up to ten ranked results. Retain evidenced names/URLs from returned material; do not invent a universal top-ten popularity ranking or crawl additional pages. A successful baseline is cached even if a later generation step fails; revisions reuse it. A failed/empty baseline blocks that attempt and offers a user retry.

Activity searches across the initial itinerary and all revisions share `min(2 * trip_days, 10)` attempts, at most five results each. Reserve an attempt before dispatch; a failed attempt/retry consumes allowance. No allowance refund on rollback. With no slots left, use cached evidence only. Rate retrieval and the separate baseline are not activity searches.

Python compares normalized names and URLs with source-evidenced aliases: Unicode/case/whitespace normalization, lowercase URL host, fragments/known tracking parameters removed, meaningful path/query identity preserved. A shared listing URL alone does not identify two differently named attractions. Ambiguous identity is excluded rather than used to claim local status. At most one activity overlaps the baseline; all others need evidence for independent/non-chain, time-limited event, or local-source criteria. Citation/excerpt checks do not prove real-world truth; quality evaluation remains necessary.

## 5. Currency acquisition, caching and worldwide use

AD4 explicitly replaces the earlier WSJ choice with the [ECB's documented reference-rate download](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html). The official page links XML/CSV and quotes currencies against EUR. This is a structured data integration, not website scraping. The reading tool could not parse the linked XML format, so ingestion and runtime access remain Construction checks; a published format is not a claim that the app already works.

Destinations remain any single city through the English interface. Currency coverage is a separate condition: the current ECB table includes currencies such as JPY, INR and KRW but not every Asian currency; VND is an example absent at the research time. Do not infer universal Asian or worldwide conversion coverage. [ECB currency table](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html)

The agreed rate policy is:

- Keep the original budget and each original activity amount/currency. Budget covers one traveler's activity tickets/fees for the whole trip; flights, lodging, meals and local transport remain excluded.
- USD-to-USD is identity. Other supported conversions require positive finite same-date source data; EUR uses the source's unit base. The budget currency list reflects usable coverage with USD default. EUR/GBP support is required for the approved fixtures, not the entire geographic scope.
- Acquire a usable snapshot for a new trip and pin it in server memory. Reuse it across activities, chat and revisions; no download per activity or message. An explicit retry may repeat a failed acquisition. No second provider or hidden manual/model fallback is introduced.
- Require source URL, source date and quotation direction. Accept source dates at most seven calendar days old and never future/undated. Proposed deterministic comparison uses the current UTC calendar date; verify boundary behavior in Functional Design/Construction.
- Normalize to USD per original currency unit. For currency X quoted per EUR, use `amount_X * (USD_per_EUR / X_per_EUR)` from one snapshot. Preserve direction explicitly; reject missing/incompatible pairs. These are cost estimates, not guaranteed payment/card exchange rates.
- Compare unrounded decimal amounts. Display USD to cents using half-up rounding, sum unrounded comparable values before rounding the subtotal, and explain possible one-cent display differences. Unknown/unconvertible activity prices are flagged/excluded, not verified zero.
- If the budget itself cannot convert, pause generation/revision with correction/retry guidance under AD5=A. Retain previous valid state. A changed confirmed budget/currency requires a confirmed new trip.
- Recheck pinned-rate freshness on update. Do not silently acquire a different snapshot and reprice fixed activities. Explain stale rates and require an appropriate new-trip confirmation for refreshed comparison. A USD-only budget does not require an external rate for its identity conversion; missing foreign activity conversions still receive unverified labels.

## 6. Session, request and resource contracts

Server memory owns confirmed preferences, accepted itinerary, ratings/locks, source registry, baseline, rate snapshot, counters, version and request receipts. The browser holds display/input state only; no localStorage, persistent cookies or database. Clear the old session on confirmed new trip and all sessions on restart. Expire a session after two idle hours, excluding an active operation. Reload starts a fresh flow; no recovery promise.

One mutation may be active per session. Replays of identical request IDs return the recorded outcome without duplicate searches/revision counts/writes. A changed payload under the same ID or a stale version produces conflict. An intentional user retry is a new request against the current version within the same remaining trip allowance; a network replay of the previous request is not a new attempt. Release the operation guard on every exit. Counter/cache updates survive failed proposal validation even when accepted content is preserved.

| Bound | Approved design default |
| --- | --- |
| Text | Destination 1–120 characters, interests 1–1,000, chat message 1–2,000, request body at most 64 KiB |
| Budget | Finite nonnegative decimal, at most 1,000,000,000 in selected currency, up to six fractional digits |
| Model attempts | At most two per intake message; at most twelve calls including retries per generation/update |
| Model output | At most 8,192 tokens and 64 KiB structured response per call; reject invalid/truncated output |
| Deadlines | Model call 120 seconds; search/rate call 30 seconds; whole generation/update 300 seconds; inner calls use remaining time |
| Automatic retries | At most one for ordinary model/activity-search failures, and only inside remaining call/time/search bounds |
| Itinerary size | At most four/day, twenty for five days; fewer/zero honest outcomes allowed |

These are resource limits, not measured performance. Construction must measure model suitability/latency/memory. Functional/NFR Design must specify retained-source/prompt size bounds, detailed parse formats, complete errors and link-check timeout/redirect limits before implementation; this does not reopen the approved product scope. All network clients must make retry accounting visible to C03.

Secrets remain in runtime environment variables, never browser output or logs. Displayed text is escaped; links use HTTP/HTTPS. External provider integrations use HTTPS; the approved link-check contract checks eligible public HTTP/HTTPS sources with private/local-target and redirect safeguards. Retrieved instructions cannot authorize requests. Diagnostic logs use identifiers/timings/categories, not raw profiles/prompts. No public unauthenticated deployment is authorized.

## 7. Team evaluation fixtures and records

AD3 selects four profiles for New York City (America/New_York), three for London (Europe/London), and three for Paris (Europe/Paris). These are synthetic evaluation inputs, not claims about available venues or actual travelers. R is the round's starting calendar date in each fixture's destination time zone; start = R plus offset and end = start plus days minus one. Keep resolved dates fixed during the round. Reconfirm live-date validity if a round is postponed.

| Fixture | Destination | Persona | Start offset | Days | Total activity budget | Interests |
| --- | --- | --- | --- | --- | --- | --- |
| F01 | New York City | Recent Graduate | +7 days | 1 | USD 40 | Street art and independent galleries |
| F02 | New York City | Abroad Student | +14 days | 2 | USD 120 | Pottery and community cultural events |
| F03 | New York City | Cultural Explorer | +21 days | 3 | EUR 180 | Local history and small live-music venues |
| F04 | New York City | Cultural Explorer | +28 days | 5 | GBP 250 | Printmaking and small museums |
| F05 | London | Recent Graduate | +7 days | 2 | USD 90 | Architecture and public art |
| F06 | London | Abroad Student | +14 days | 3 | GBP 140 | Theater workshops and local history |
| F07 | London | Cultural Explorer | +21 days | 4 | EUR 220 | Textile arts and independent exhibitions |
| F08 | Paris | Recent Graduate | +7 days | 1 | EUR 25 | Free galleries and sketching in public gardens |
| F09 | Paris | Abroad Student | +14 days | 3 | USD 150 | Local music and cultural classes |
| F10 | Paris | Cultural Explorer | +21 days | 5 | GBP 300 | Pottery and photography exhibitions |

Use actual team ratings and revision requests; do not force favorable results. Evaluation scenarios do not replace separate deterministic failure/boundary tests. Fixture IDs, cities, dates, budgets and interests are not logged with random itinerary IDs.

The only persisted record fields are itinerary_id, activity_count, revision_request_count, baseline_overlap_count, link_check_results and activity_ratings (including optional approved reasons). Arrays correspond to final activity order with latest nullable ratings and source-load outcomes; they do not store URLs, names, source/session IDs, raw text or profile mappings. Keep one final record per itinerary ID, updating that final record only on explicit evaluation completion. Failed generation does not become a fake zero-activity success.

| Metric | Numerator | Denominator | Target |
| --- | --- | --- | --- |
| Activity approval | Final thumbs-up ratings | Rated final activities | At least 70% |
| Revision rate | Evaluated test itineraries with more than two update requests | Evaluated test itineraries | Under 30% |
| Local discovery | Validated non-baseline final activities with local evidence | All final recommended activities | At least 70% |
| Source coverage | Final activities with a successfully loaded source link | All final recommended activities | 100% |

Local count derives from activity count minus baseline overlaps only after the validator has enforced locality evidence for every non-baseline activity. Link loading is availability evidence, not factual verification. Empty denominators are N/A. Report generation failures and attempted/final-itinerary counts separately; a round with fewer than ten evaluated final itineraries is incomplete. This explicit failure/denominator interpretation is presented for team review with the design, not attributed to an additional unrecorded answer.

ratings.jsonl remains locally gitignored, never committed, and deleted after the final demo. No ratings are created by Inception. No live-user telemetry or new evaluation account/dashboard is introduced.

## 8. Requirements and story coverage

| Requirement | Stories | Responsible components / service |
| --- | --- | --- |
| FR-01 | US-01 | C02, C07; intake/date validation |
| FR-02 | US-02 | C02, C03, C04; summary/confirmation |
| FR-03 | US-03, US-09, US-10, US-11 | C03, C05, C08; cumulative activity quota |
| FR-04 | US-03, US-09, US-11, US-12 | C03, C05, C07, C08; separate cached baseline |
| FR-05 | US-03 | C04, C07; cited local evidence and overlap |
| FR-06 | US-04, US-09, US-13 | C01, C03, C07, C08; source ownership and safe rendering |
| FR-07 | US-05, US-10 | C01, C03, C07; honest counts/shortfalls |
| FR-08 | US-06 | C02, C04, C07; local-time feasibility |
| FR-09 | US-06 | C04, C07; evidenced event occurrence |
| FR-10 | US-01, US-07 | C02, C06, C07; budget scope/comparable subtotal |
| FR-11 | US-07 | C06; approved ECB source, pinned rates and labels |
| FR-12 | US-08 | C01, C03, C08; preset ratings/locks only |
| FR-13 | US-09, US-10 | C03, C07, C08; targeted replacement/preservation |
| FR-14 | US-11 | C01, C02, C03, C08; explicit new-trip confirmation |
| FR-15 | US-12 | C01, C03, C04, C05, C08; bounded retries and safe failures |
| FR-16 | US-11, US-13 | C03, C08; ephemeral authority, expiry/reset and provenance |
| FR-17 | US-05, US-14 | C01; keyboard/focus/text labels and desktop browser flows |
| FR-18 | US-15, US-17 | C08, C09; final anonymous projection/retention |
| FR-19 | US-16 | C07, C09; validated final-snapshot denominators |
| NFR-01 | Cross-cutting | One local application and planned model/adapters |
| NFR-02 | US-01, US-03, US-04, US-08, US-12, US-13, US-15, US-17 | Validation/trust/data-minimization boundaries throughout |
| NFR-03 | Cross-cutting | Typed contracts, separated responsibilities, permitted tools only |
| NFR-04 | All stories | Future mocked unit/API checks plus controlled live/browser checks |
| NFR-05 | Cross-cutting | Future pure-rule/serialization PBT; framework still deferred |
| NFR-06 | US-03, US-09, US-10, US-12 | Bounded requests, preserved results and later measurements |

All 19 FRs, six NFRs and 17 stories have a place in the design. Formal assignment to the application unit/modules is the next stage's story-map work.

## 9. Deferred-item disposition and verification

| ID | Current disposition | Remaining work |
| --- | --- | --- |
| DEF-01 | Resolved by AD3: cities and ten concrete fixtures above | Run actual rounds in Construction; no results claimed |
| DEF-02 | Prior WSJ investigation returned to team; AD4 explicitly selects documented ECB reference data | Verify actual download/parsing and failure handling in Construction; do not claim WSJ or ECB integration already works |
| DEF-03 | AD5/AD6 resolve missing budget, coverage, rate date/direction/cache and rounding policy | Detailed arithmetic/date fixtures and implementation tests later |
| DEF-04 | AD1/AD2/AD6 plus these artifacts define high-level components, methods, state, limits and normalization | Exact schemas, algorithms, remaining input/evidence/link bounds and concurrency mechanics in later Functional/NFR Design |
| DEF-05 | Still deferred | Select/review PBT framework in later NFR/design; configure/test in Construction |
| DEF-06 | Still deferred | Measure qwen3:4b quality/latency/memory and verify fallback hardware |
| DEF-07 | Official Tavily documentation informs the interface only | Team account/quota/cost availability, dependency licenses and tested version pinning before integration |

Later verification must cover initial/revised schedule constraints, evidence ownership, prompt-injection boundaries, baseline matching, currency inversions/freshness/rounding, unchanged locked activities, duplicate requests, retries/quotas, expiry, record allowlists, link checks, KPIs and cleanup. Routine tests mock network/model data; controlled integrations/browser checks occur before the final demo. The existing three example tests remain unchanged and have no passing-run claim here.

## 10. Extension compliance

Security Baseline: N/A, disabled by C5=B. Resiliency Baseline: N/A, disabled by Q17=B. Their skips are logged; project-specific controls remain. Partial PBT applies only in its approved scope.

| Rule | Current-stage status | Rationale / later obligation |
| --- | --- | --- |
| PBT-01 | N/A | Advisory in partial mode; detailed property identification later |
| PBT-02 | N/A | Serialization contracts exist, but no code/tests generated; round-trip obligation retained |
| PBT-03 | N/A | Pure-rule boundaries defined, but no implementation/tests; invariants must be tested later |
| PBT-04 | N/A | Advisory; idempotent request semantics documented for later tests |
| PBT-05 | N/A | Advisory; no oracle implementation |
| PBT-06 | N/A | Advisory; no mandatory stateful-PBT expansion |
| PBT-07 | N/A | Domain generator construction is later test work |
| PBT-08 | N/A | Shrinking, failure seeds and CI execution belong to Construction |
| PBT-09 | N/A | Framework selection/configuration remains DEF-05 in later NFR/design |
| PBT-10 | N/A | Advisory; story-based example testing remains required |

No applicable extension finding blocks design review. This is a design applicability assessment, not a claim of implemented security or passing tests.

## 11. Review boundary

The team separately approved all five generated artifacts and the accompanying review package with "approve & continue", recorded 2026-11-25T02:02:35Z. This includes the concrete method names, API status mappings and evaluation failure interpretation presented for review; no extra question answers are invented. Units Generation may now begin. Its plan and generated artifacts require their own review. Stop after Units approval, before Construction.
