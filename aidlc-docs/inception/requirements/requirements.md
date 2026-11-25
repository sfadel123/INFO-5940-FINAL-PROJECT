# Personalized Cultural Travel Planner — Requirements

Status: Requirements baseline approved at 2026-11-24T21:03:33Z; reconciled with AD1–AD6 and plan approval recorded 2026-11-25T01:32:46Z. Generated Application Design separately approved with "approve & continue", recorded 2026-11-25T02:02:35Z. No implementation, passing tests, model suitability or working rate integration is claimed.

## 1. Intent analysis

- User request: run one shared AI-DLC v1.0.1 Inception workflow from approved inputs, record actual team answers/approvals, and stop after Units Generation approval before Construction.
- Request type: new product. Existing code consists only of the illustrative trip-validation example reviewed in Reverse Engineering.
- Scope: a single local application with multiple responsibilities: conversational intake, bounded retrieval, model/tool orchestration, currency conversion, itinerary validation, session provenance, feedback, and evaluation.
- Complexity/depth: moderate; Standard requirements depth with explicit acceptance criteria and traceability.
- Product purpose: help travelers discover cultural activities matched to their interests, dates, and budget, including less-promoted local experiences.
- Why an LLM: interpret natural-language interests, propose focused search queries, assess retrieved evidence for relevance, explain matches, and revise disliked activities. Python enforces budgets, scheduling, source ownership, and tool boundaries.

## 2. Sources, precedence, and team decisions

Source keys used below:

- R: [README.md](../../../README.md).
- V: [vision.md](../../../vision.md).
- T: [tech-env.md](../../../tech-env.md), the actual technical-input filename.
- Q1–Q18: [original verification answers](requirement-verification-questions.md).
- C1–C5: [first clarification answers](requirements-analysis-clarification-questions.md).
- D1–D2: [remaining clarification answers](requirements-analysis-remaining-questions.md).
- [Audit](../../audit.md): verbatim answer snapshots and actual UTC recording timestamps.
- User Stories [S1–S3](../plans/story-generation-plan.md) and [SC1](../plans/story-planning-clarification-questions.md): later persona grouping decisions; requirements behavior unchanged.
- Milestone assignment: attached assignment read at workflow start; requires requirements, stories/personas, workflow plan, application design, units/dependencies/story map, and audit/state records. Milestone due November 24, 2026; Construction belongs to the final-project stage.

All 25 Requirements answer tags and six Application Design answer tags are filled and validated. Later explicit answers resolve earlier wording; original answers remain unchanged as historical evidence. AD1–AD6 are in [the approved design plan](../plans/application-design-plan.md); the generated [Application Design](../application-design/application-design.md) supplies the current contracts and fixtures.

| Decision | Current agreed interpretation | Evidence |
| --- | --- | --- |
| Geographic coverage | English interface accepts any single destination; evaluation uses ten profiles across three destinations | Q1, C1=B |
| Evaluation city names | New York City, London, Paris; ten fixtures distributed 4/3/3 | AD3=A resolves D1=B |
| Currency handling | Preserve traveler-selected budget/currency; convert budget and activity prices to USD for comparison and totals | Q4, C2=B |
| Rate source | ECB daily reference data; pinned trip snapshot and source/date labels; implementation unverified | AD4=A supersedes C3/D2 source choice |
| Duration estimates | Activity-based, visibly estimated, no fixed 30–180-minute range; must fit schedule constraints | Q5, C4=B |
| Activity-search allowance | Shared across initial generation and all revisions of the same trip; baseline is separate | Q9=B, V, T |
| Security extension | Disabled; project-specific security/privacy requirements remain | C5=B supersedes Q16=A |
| Resiliency extension | Disabled; agreed failure-handling requirements remain | Q17=B |
| Property-based testing | Partial, for pure functions and serialization round-trips | Q18=B |
| Shared workflow operator | Sophia; teammates join calls for shared decisions and approvals | Q15=X |

## 3. Users and boundaries

The main audience is travelers in their 20s and 30s who want interest-based local experiences without extensive research. The product remains useful to other travelers. The team selected three traveler personas during User Stories planning: Recent Graduate, Abroad Student, and Cultural Explorer (S1, refined by SC1). The Team Evaluator is a separate project role for the existing evaluation process. Hobby activities and pop-ups remain supported; this persona grouping does not change the single-traveler scope or functional requirements.

The MVP runs on one user's laptop in a local desktop browser. Each trip covers one traveler and one city for one to five inclusive calendar days. It does not promise worldwide evaluation coverage merely because users can enter any destination.

Out of scope: direct booking/payment, account registration, persistent traveler profiles, multi-city/group trips, route optimization, calendar export, social-media scraping, personality quizzes, mobile-specific layout testing, cloud hosting, containers, and public deployment. Post-trip satisfaction surveys remain future scope. No paid provider access, subscription, or rate API is assumed available.

## 4. Functional requirements and acceptance criteria

### FR-01 — Trip scope and date validation

Accept one destination, start/end dates, a total activity budget with currency, and interests. Dates are interpreted in the destination's local time zone. A live trip must start today or later, end on or after its start, and span no more than five inclusive days.

Acceptance: a same-day trip is one day; reversed, past-start, and over-five-day live trips are rejected with an understandable correction request before generation. Historical dates may be used in deterministic tests. Sources: V, T, Q1, Q3, C1.

### FR-02 — Conversational intake and confirmation

Collect valid required fields, ask up to three additional interest-clarification turns, then show a preference summary for explicit confirmation. Missing or invalid required fields still need correction; reaching the clarification cap does not authorize generating from invented preferences.

Acceptance: an ambiguous interest can receive a follow-up; generation starts only after the valid summary is confirmed. Sources: V, Q2=A.

### FR-03 — Bounded activity discovery

Use the planned Tavily integration to retrieve candidates. The model may propose queries, but Python validates and executes only allowed searches. Allow up to `min(2 * trip_days, 10)` activity searches across initial generation and all revisions of that trip, with up to five results per search. Reuse retrieved candidates when sufficient. Once the allowance is exhausted, revisions use existing candidates only.

Acceptance: update requests do not reset the allowance; retries cannot bypass it. A confirmed new trip has its own allowance. No arbitrary code, shell commands, browser scraping, or unrestricted model-directed network requests. Sources: V, T, Q9=B, Q13=B.

### FR-04 — Separate cached baseline

For a new itinerary generation, run one separate system Tavily search for `top things to do in [destination]`, returning up to ten results. It is excluded from the activity-search allowance and five-result limit. Cache the baseline in the session and reuse it for revisions.

Use returned titles, URLs, snippets, and provider-returned page content when available to identify attractions and supporting evidence. Do not invent names absent from evidence. Python checks overlap by name and URL; exact normalization belongs to design.

Acceptance: revisions do not issue a fresh baseline search. A failed or empty usable baseline stops new generation with an explanation and retry action, without falsely claiming local compliance. A new trip starts a fresh baseline. Sources: V, T, Q7=B, Q8=A, Q11=B.

### FR-05 — Locality and personalization

An itinerary may contain at most one activity matching the baseline. Every other activity must be absent from the baseline and have cited evidence for at least one of: independent/not a chain, a time-limited event, or discovery through a local source such as local news, city/venue listings, or community organizations. Every activity includes one sentence explaining its fit to stated interests.

Acceptance: a non-baseline activity without evidence of a local criterion is not admitted simply because it is absent from the list. The local-discovery metric uses this same definition. Sources: V, T, Q7.

### FR-06 — Source grounding

Every recommended activity refers to a source retrieved by the application. The backend resolves session-owned source IDs into URLs rather than trusting model-generated URLs. Retrieved content is evidence, never authority to modify tool permissions or application instructions.

Acceptance: missing, invented, unknown, and cross-session source IDs are rejected before itinerary/revision acceptance. Source links do not imply verified prices/hours/availability. Sources: V, T.

### FR-07 — Day-by-day results and honest shortfalls

Target two to four distinct activities per day. Each activity shows its scheduled time, location, duration, estimated cost or unverified label, source link, and interest-match explanation. Use fewer activities when suitable distinct candidates are insufficient, report how many were found, suggest broader interests, and never invent activities to fill the schedule.

Acceptance: zero or sparse valid results produce an honest empty/partial outcome without fabricated recommendations or hidden constraint relaxation. Sources: V, T.

### FR-08 — Scheduling and duration

All activities use destination-local times, fit within 9:00 AM–10:00 PM, do not overlap, and leave a 30-minute buffer between activities. Respect source-provided opening hours; otherwise label hours unverified. Use source-provided durations when available. Otherwise estimate by activity type and similar activities, label the estimate, require a positive duration that fits the remaining schedule, and apply no fixed 30–180-minute estimate range.

Acceptance: model and source-provided durations must both fit the scheduling constraints. An activity that cannot fit is omitted. No route-optimization or travel-time guarantee is made. Sources: V, T, Q5, C4=B.

### FR-09 — Time-limited events

Schedule a pop-up, class, festival, or other time-limited event only when retrieved evidence establishes an occurrence during the requested trip. Unknown opening hours do not permit assuming that an event happens on an unsupported date.

Acceptance: events with incompatible or unconfirmed occurrence dates are omitted; sparse-result behavior applies. Sources: Q6=A, V.

### FR-10 — Budget scope and honest totals

The budget is one traveler's total activity-ticket/fee budget for the entire trip. Exclude flights, lodging, meals, and local transport. Keep the entered amount and selected currency (default USD), convert that budget and verified activity prices into USD for comparison and totals, and label conversions.

Acceptance: known, comparable activity totals must fit the converted budget. Unknown prices or prices without valid conversions are flagged as unverified and excluded from the calculated subtotal, never counted as verified zero-cost activities. Do not claim full budget compliance when unverified costs or budget conversion prevent it. If the budget cannot convert, pause generation/revision and offer correction/retry while preserving valid state; a confirmed preference change requires a new trip. Sources: V, T, Q4, C2=B, AD5=A.

### FR-11 — Planned ECB currency conversion

Use the [ECB daily reference-rate download](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html), selected explicitly in AD4=A to replace the earlier WSJ plan. Preserve original amounts/currencies, source URL and source date; label USD conversions as estimates. Do not invent rates, use model memory, add browser scraping or silently substitute another provider.

Acceptance: use positive finite same-date rates with a source date no more than seven calendar days old and not future/undated. Pin one snapshot to the trip, reuse it for activities/revisions, and recheck freshness without silently repricing unaffected activities. USD identity needs no external quote; unsupported activity currencies are unverified, while an unavailable budget conversion pauses generation/revision. Normalize the quoted direction to USD per original-currency unit, compare unrounded decimal amounts, and display cents with half-up rounding after summing unrounded values. Coverage is limited to usable published currency data and is independent of accepted destination cities. Actual ingestion and integration remain Construction checks. Sources: AD4–AD6; generated Application Design.

### FR-12 — Activity feedback

Support thumbs up/down and an optional preset reason: too touristy, too expensive, wrong time, or not my interest. Do not collect free-text feedback. Thumbs down marks an activity without immediately replacing it; thumbs up locks it.

Acceptance: feedback alone does not invoke itinerary replacement. Preset choices are validated and unrestricted feedback strings rejected. Chat remains conversational; the free-text prohibition concerns the structured feedback feature and persisted ratings. Sources: V, T.

### FR-13 — Controlled revisions

Clicking Update itinerary or explicitly asking in chat replaces only thumbs-down activities. Preserve all preferences, locked activities, and unaffected activities. Replacements must fit remaining time/budget and be distinct. If no suitable replacement is found, keep the original activity visibly marked disliked and explain the shortfall; suggest broader interests for a new itinerary without changing preferences silently.

Acceptance: update does not alter a thumbs-up or neutral activity, regenerate the baseline, or reset search allowance. Source and schedule checks still apply. Sources: V, T, Q9=B, Q10=A.

### FR-14 — Confirmed new trip

When the traveler asks to change destination, dates, budget, or other trip preferences, chat may propose starting a new trip. Require explicit confirmation before discarding the old itinerary and starting a fresh session and baseline.

Acceptance: until confirmation, existing preferences, results and locks remain intact. A confirmed new trip is distinct from a revision. Sources: Q11=B.

### FR-15 — Failures and retries

For ordinary model or activity-search timeout/service errors, allow one automatic retry within existing request/search limits, showing progress. If failure persists, show a safe error and retry action while preserving the last valid itinerary and user inputs. No invented substitute results. Baseline failure follows FR-04.

Acceptance: retries cannot reset allowances or exceed configured bounds; errors do not expose credentials or internal traces. AD6 supplies resource bounds, including 120-second model calls, 30-second search/rate calls, a 300-second operation deadline and at most twelve model calls including retries per generation/update. These are limits, not measured performance. Sources: T, Q8=A, Q13=B, AD6=A.

### FR-16 — Session lifecycle

Server memory is authoritative for confirmed preferences, accepted itinerary, ratings/locks, sources, baseline, rates, counters, version and request receipts. Create a random session ID at bootstrap; the browser sends it with later commands and holds only a display/input copy. Mutations include a request ID and expected version; one mutation per session and replay/conflict guards prevent duplicate work or changed fixed state.

Acceptance: reject unknown/cross-session/stale evidence; clear the old session on confirmed new trip and all state on restart; expire after two idle hours excluding active operations. Reload starts a fresh flow. Browser storage cannot recreate authority; no database, persistent browser storage or saved profiles. Failed attempts preserve accepted content but retain consumed quota/successful caches. Sources: V, T, Q11, AD6=A.

### FR-17 — Desktop interface and accessibility

Provide an English-language desktop interface with chat alongside day-grouped activity cards in Chrome and Safari. Include keyboard-operable controls, visible focus, readable contrast, text labels for ratings, source links, and understandable progress/error messages. Mobile-specific layout testing is excluded.

Acceptance: the confirmed-trip, generation, feedback, revision, and new-trip flows can be completed with the keyboard, and rating/error meaning is available as text. Sources: Q12=A, R, V.

### FR-18 — Anonymous evaluation records

Measure KPIs during team evaluation rounds only, using ten sample profiles across three destinations. AD3 selects New York City, London and Paris with the ten synthetic fixtures distributed 4/3/3 in Application Design. Persist only random itinerary ID, activity count, revision-request count, baseline-overlap count, link-check results, and activity ratings (with allowed preset reasons). Do not persist destinations, travel dates, budgets, chat text, or session IDs in evaluation records.

Store records in local ratings.jsonl, excluded from Git and deleted after the final demo. The existing .gitignore exclusion is present locally but has not been committed in the approved-input commit.

Acceptance: recorded fields are checked against this allowlist; the application must not depend on live-user telemetry or retain raw conversations for KPI calculation. Sources: V, T, Q14=A, C1=B, D1=B.

### FR-19 — Evaluation calculations

Use the final itinerary per profile for activity-based KPIs, count each final activity once, and use its latest rating. Preserve the full revision-request count for each test itinerary. Report generation failures separately. An empty denominator is N/A, not 100%.

| Metric | Numerator | Denominator | Target |
| --- | --- | --- | --- |
| Activity approval | Final rated activities with thumbs up | Rated final activities | At least 70% |
| Revision rate | Test itineraries needing more than two revision requests | Test itineraries | Under 30% |
| Local discovery | Final activities absent from baseline and satisfying a cited local criterion | All final recommended activities | At least 70% |
| Source coverage | Final activities whose source link loads in an automated check | All final recommended activities | 100% |

Acceptance: replaced activities are not pooled with final activities, and manual/automated evaluation can reproduce each numerator and denominator. Link loading checks measure availability, not factual accuracy. No successful evaluation or achieved target is claimed yet. Sources: V, T, Q14=A, C1, D1.

## 5. Non-functional and technical requirements

### NFR-01 — Local deployment and model plan

Use Python 3.12 with pip/venv, FastAPI, Pydantic v2, Uvicorn, Jinja2, HTML/CSS, and minimal JavaScript in one modular application. Run the application and Ollama on the same laptop; use external HTTPS for search and planned ECB reference-data retrieval. The planned model is qwen3:4b via Ollama, called with the OpenAI Python client through the OpenAI-compatible API. qwen3:8b on a higher-memory laptop is the fallback. Suitability, tool-call quality, latency, and memory usage remain Construction verification tasks; availability of a fallback laptop is not asserted. Sources: R, T.

### NFR-02 — Project-specific security and privacy

Keep secrets in runtime environment variables, out of Git, browser responses, and logs. Validate request/response types, formats, sizes, source-session ownership and structured model output. Escape displayed text and restrict source links to HTTP/HTTPS. Treat retrieved instructions as untrusted data. Bind services to loopback; use HTTPS for external traffic. Collect no payment/passport/home-address/account credentials. Send only needed destination/dates/search interests to external search, not entire conversations. Bound input sizes, tool calls, retries, model output, and timeouts.

Acceptance: design and tests cover malicious retrieved content, unsafe links, malformed inputs, secret exposure, and cross-session source IDs. Account authentication remains out of scope, while source/session checks remain mandatory. Diagnostics use request identifiers, timings, and error categories rather than raw traveler profiles. No production security certification is claimed. Sources: T, C5=B.

### NFR-03 — Maintainability and API conventions

Separate preferences, search, model integration, currency conversion, itinerary validation, and UI/API responsibilities within the single application. JSON endpoints use /api/v1/, snake_case fields/functions, ISO dates, and typed schemas. Invalid API inputs return 422. Planned chat/feedback endpoints remain design targets, not already implemented services.

Retain the prohibited-library table in tech-env.md: no orchestration frameworks, browser scraping, direct PyTorch/Transformers hosting, or payment/booking SDKs for this MVP. Dependencies/services require documented purpose and team review; pin tested versions and run pip-audit during Construction. AD1 selects Python-guided orchestration, AD2 selects open-request progress, and AD4 selects documented ECB data acquisition. Interfaces remain unimplemented; versions/licenses and integration checks stay in Construction. Sources: T, AD1/AD2/AD4.

### NFR-04 — Example-based tests and integration checks

Use pytest and FastAPI TestClient/HTTPX. Mock model/search/rate responses in routine automated tests; test deterministic logic directly. Target at least 80% line coverage for deterministic preference- and itinerary-validation modules. Cover date bounds, budgets/conversion validation, scheduling, source mapping, and revision preservation. Controlled live integration checks and manual Chrome/Safari user-flow checks precede the final demo.

The existing three trip-validation example tests illustrate patterns only; they do not implement the five-day maximum and have no recorded passing execution in this workflow. Coverage percentages and live integration success are not asserted. Sources: T, Q12, C2, D2.

### NFR-05 — Partial property-based testing

Add PBT for applicable pure functions and serialization round-trips, complementing the example tests. Carry PBT-02/03/07/08/09 obligations into later design/Construction: round-trip properties, invariants, domain-aware generators, shrinking, reproducible failure seeds, CI integration, and framework selection documented in tech-stack decisions. Framework/dependency selection is a later design decision; nothing is installed here. Stateful/live-model PBT is not made mandatory by this partial opt-in. Source: Q18=B and installed PBT partial-mode rules.

### NFR-06 — Performance and reliability verification

Enforce bounded requests and safe failures. Benchmark actual model latency/memory on the demonstration laptop during Construction before claiming a numerical performance target. Display progress during generation/retries. Search quota behavior and preservation of prior results must be testable with deterministic failures. Sources: T, Q13.

## 6. User-flow acceptance scenarios

| Scenario | Expected result | Requirements |
| --- | --- | --- |
| Traveler provides ambiguous interests | Bounded clarification and confirmed summary before generation | FR-01/02 |
| Valid five-day trip with enough evidence | Distinct sourced activities, feasible times, USD comparison, local criteria enforced | FR-03–11 |
| No usable baseline | Explain failure and allow retry; no false local-discovery claim | FR-04 |
| Too few valid candidates | Show fewer or none and count found; never invent fillers | FR-05/07/09 |
| Unknown price or unavailable conversion | Flag/exclude from verified subtotal; do not claim full budget compliance | FR-10/11 |
| Feedback then update | No immediate replacement; replace disliked only, respect locks/allowance; keep disliked if no substitute | FR-12/13 |
| User requests changed dates | Confirm a new trip before discarding old itinerary/session | FR-14 |
| Model/search failure | At most one bounded retry, then safe error with valid prior state preserved | FR-15 |
| Cross-session or restart-stale source ID | Reject the affected submitted data | FR-06/16 |
| Final evaluation round | Ten approved profiles across New York City, London and Paris, final-only activity KPIs and full revision counts | FR-18/19 |

## 7. Explicitly deferred decisions and verification

These are tracked tasks permitted by the recorded answers, not invented choices or completed checks.

| ID | Item | Stage / required outcome | Basis |
| --- | --- | --- | --- |
| DEF-01 | Evaluation cities and ten fixtures | Resolved by AD3: New York City/London/Paris, 4/3/3; evaluation itself remains Construction work | D1 resolved by AD3=A |
| DEF-02 | Rate-source access decision (originally WSJ) | Team explicitly selected documented ECB data after unverified WSJ access; actual ingestion/integration remains Construction work | AD4=A supersedes prior source choice |
| DEF-03 | Rate and missing-budget policy | Resolved at design level: dated positive rates, seven-day freshness, pinned snapshot, USD direction, decimal/half-up display and pause on unavailable budget | AD5/AD6=A |
| DEF-04 | Components, contracts, state, normalization and limits | High-level design generated under AD1/AD2/AD6; exact schemas, algorithms and remaining evidence/link bounds stay in Functional/NFR Design | AD1/AD2/AD6=A |
| DEF-05 | PBT framework and dependency configuration | Later design/NFR selection: review appropriate framework, then configure in Construction | Q18; PBT-09 |
| DEF-06 | Model quality, laptop suitability, latency/memory targets and fallback hardware | Construction: test actual environment and record evidence; return changed choices to team | R, T |
| DEF-07 | Tavily account access/limits, dependency versions and licenses | Design/Construction before integration: verify availability/cost and pin tested dependencies; no purchase assumed | T |

No further Requirements Analysis clarification is pending. AD3/AD4 supply actual team choices for cities and the replacement rate source; no choice was inferred. Detailed implementation and remaining verification are still deferred, and Construction is not authorized.

## 8. Extension compliance at this stage

| Extension | Status | Scope and rationale |
| --- | --- | --- |
| Security Baseline | N/A — disabled by C5=B | All SECURITY-01 through SECURITY-15 extension rules skipped. Earlier findings closed by explicit opt-out, not implemented controls. NFR-02 and other project-specific protections remain required |
| Resiliency Baseline | N/A — disabled by Q17=B | Full rules not loaded/enforced; FR-15 and NFR-06 remain required |
| Property-Based Testing | Partial — requirements capture compliant | NFR-05 records the applicable obligations. Verification of generated tests/framework configuration belongs to later stages |

| PBT rule | Stage assessment |
| --- | --- |
| PBT-01 | N/A as a blocking rule in partial mode; advisory for later functional design |
| PBT-02 | Obligation captured in NFR-05; actual round-trip tests N/A before test generation |
| PBT-03 | Obligation captured in NFR-05; actual invariant tests N/A before test generation |
| PBT-04 | N/A as a blocking rule in partial mode; advisory |
| PBT-05 | N/A as a blocking rule in partial mode; advisory |
| PBT-06 | N/A as a blocking rule in partial mode; advisory; no automatic stateful-PBT scope expansion |
| PBT-07 | Obligation captured in NFR-05; generator implementation N/A before test generation |
| PBT-08 | Obligation captured in NFR-05; seed/shrinking/CI execution N/A before Construction |
| PBT-09 | Selection/configuration explicitly tracked in DEF-05; implementation N/A at this requirements stage |
| PBT-10 | N/A as a blocking rule in partial mode; existing example-based testing commitments retained |

No unresolved extension finding blocks this requirements review. No tests or production-readiness checks have been represented as completed.

## 9. Approval and next stage

The team approved these requirements and the accompanying review package with "Approved ", recorded 2026-11-24T21:03:33Z. The questions, answer history, updated inputs, audit, and state accompany this approved document. User Stories Part 1 planning is the next stage; its plan and generated artifacts require their own approvals. Later stages remain User Stories, Workflow Planning, Application Design, and Units Generation. Stop after Units Generation approval, before Construction.
