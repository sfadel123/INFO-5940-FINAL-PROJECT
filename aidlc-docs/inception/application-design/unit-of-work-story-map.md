# Unit of Work Story Map

Status: Generated Units artifact explicitly approved by the team with "approve and finish inception ", recorded 2026-11-25T02:27:53Z. Units Generation and Inception are complete. Work stopped before Construction; implementation and runtime verification remain future work.

## Mapping conventions

Every approved story is assigned exactly once to **U01 — Cultural Travel Planner**. The six sections retain the approved user-journey organization; they are not six units or fixed sprint commitments. C01–C09 retain their approved meanings from [components.md](components.md) and [unit-of-work.md](unit-of-work.md).

The primary module coordinates or supplies the central behavior of that story. Collaborators implement its supporting behavior/checks; this is a logical responsibility map, not an additional call graph or a named teammate assignment. Calls still follow [unit-of-work-dependency.md](unit-of-work-dependency.md). Some related capabilities appear as collaborators because a complete user outcome spans modules. C04 and C05 support several stories without needing an artificial standalone end-user story.

UG1=A establishes shared team ownership for every row. Sophia remains the shared-session operator, not an assumed implementation owner. P01 Recent Graduate, P02 Abroad Student and P03 Cultural Explorer share US-01–US-14; R01 Team Evaluator uses US-15–US-17.

[stories.md](../user-stories/stories.md) remains the authoritative acceptance text. Existing AC 1–n refers to its numbered Given/When/Then scenarios within that story; no criteria are deleted, rewritten or claimed to have passed. The verification column allocates later checks, not new product requirements. Shared NFRs also apply as mapped below.

## 1. Confirm the trip

| Story and outcome | Unit | Primary module; collaborators | Existing requirements | Existing AC | Later verification focus |
| --- | --- | --- | --- | --- | --- |
| US-01 — Enter valid trip preferences | U01 | C02; C01, C03, C04, C08 | FR-01, FR-10, NFR-02 | 1–4 (4) | Pure preference/date/money boundaries; mocked intake/API corrections |
| US-02 — Clarify interests and confirm the summary | U01 | C03; C01, C02, C04, C08 | FR-02 | 1–3 (3) | Clarification cap, valid-summary confirmation and blocked premature generation |

## 2. Discover and review the itinerary

| Story and outcome | Unit | Primary module; collaborators | Existing requirements | Existing AC | Later verification focus |
| --- | --- | --- | --- | --- | --- |
| US-03 — Receive relevant local recommendations | U01 | C03; C01, C04, C05, C06, C07, C08 | FR-03, FR-04, FR-05, NFR-02 | 1–5 (5) | Search permits/attempt counts, cached baseline, evidenced locality and interest explanation |
| US-04 — Inspect the recommendation sources | U01 | C01; C03, C04, C05, C07, C08 | FR-06, NFR-02 | 1–3 (3) | Owned-source validation, rejected invented/cross-session IDs and escaped safe links |
| US-05 — Review a clear daily plan | U01 | C01; C03, C04, C06, C07, C08 | FR-07, FR-17 | 1–3 (3) | Complete day-card fields and honest sparse/zero-result UI with distinctness checks |
| US-06 — Receive a feasible local-time schedule | U01 | C07; C01, C02, C03, C04, C05, C08 | FR-08, FR-09 | 1–4 (4) | Local-time intervals, buffers, opening hours, duration labels and sourced event dates |
| US-07 — Understand comparable costs and uncertainty | U01 | C06; C01, C02, C03, C04, C05, C07, C08 | FR-10, FR-11 | 1–5 (5) | Pure conversions/subtotals; pinned/fresh rate fakes, missing-budget block and uncertainty display |

## 3. Give feedback and revise

| Story and outcome | Unit | Primary module; collaborators | Existing requirements | Existing AC | Later verification focus |
| --- | --- | --- | --- | --- | --- |
| US-08 — Rate activities without immediate changes | U01 | C03; C01, C08 | FR-12, NFR-02 | 1–3 (3) | Allowed feedback/reasons, latest vote/lock and no generation on rating |
| US-09 — Replace only the disliked activities | U01 | C03; C01, C04, C05, C06, C07, C08 | FR-13, FR-03, FR-04, FR-06 | 1–4 (4) | Only disliked replacements; unchanged fixed fields/preferences; same baseline and allowance |
| US-10 — Understand when no replacement is possible | U01 | C03; C01, C04, C05, C06, C07, C08 | FR-13, FR-03, FR-07 | 1–2 (2) | Exhausted-quota/candidate failures retain disliked original and explain without invention |

## 4. Start a different trip

| Story and outcome | Unit | Primary module; collaborators | Existing requirements | Existing AC | Later verification focus |
| --- | --- | --- | --- | --- | --- |
| US-11 — Confirm preference changes as a new trip | U01 | C03; C01, C02, C04, C08 | FR-14, FR-16, FR-04, FR-03 | 1–3 (3) | Declined/pending reset preserves state; confirmed new session needs valid new intake |

## 5. Recover and use the interface

| Story and outcome | Unit | Primary module; collaborators | Existing requirements | Existing AC | Later verification focus |
| --- | --- | --- | --- | --- | --- |
| US-12 — Recover from generation or search failures | U01 | C03; C01, C04, C05, C06, C07, C08 | FR-15, FR-04, NFR-06, NFR-02 | 1–3 (3) | Bounded retry/deadline failures preserve accepted state and consumed quotas; unusable baseline stops |
| US-13 — Keep evidence tied to the active session | U01 | C08; C01, C03, C05, C07 | FR-16, FR-06, NFR-02 | 1–3 (3) | Cross-session/stale source rejection, authoritative state, expiry/restart/reload boundaries |
| US-14 — Use the desktop flow accessibly | U01 | C01; C03 | FR-17 | 1–3 (3) | Desktop Chrome/Safari keyboard, focus, labels, contrast and complete traveler flows |

## 6. Evaluate the MVP as a team

| Story and outcome | Unit | Primary module; collaborators | Existing requirements | Existing AC | Later verification focus |
| --- | --- | --- | --- | --- | --- |
| US-15 — Record an anonymous evaluation round | U01 | C09; C01, C03, C07, C08 | FR-18, NFR-02 | 1–3 (3) | Ten-profile round, final snapshot, exact anonymous projection, replay/upsert and Git exclusion |
| US-16 — Calculate KPIs from final itineraries | U01 | C09; C01, C03, C07, C08 | FR-19, FR-18 | 1–6 (6) | Pure KPI denominators/latest final votes, bounded link outcomes, N/A and incomplete/failure reporting |
| US-17 — Delete evaluation ratings after the demo | U01 | C09; None; team invokes cleanup | FR-18, NFR-02 | 1–2 (2) | Later local cleanup and retention verification; no new UI endpoint or account is implied |

## 7. Complete functional-requirement coverage

The following mapping is derived from each approved story's Requirements field. All 19 FRs are covered by U01. The story rows above identify their primary/contributing modules; this table does not create additional story assignments.

| Requirement | Unit | Approved story coverage |
| --- | --- | --- |
| FR-01 | U01 | US-01 |
| FR-02 | U01 | US-02 |
| FR-03 | U01 | US-03, US-09, US-10, US-11 |
| FR-04 | U01 | US-03, US-09, US-11, US-12 |
| FR-05 | U01 | US-03 |
| FR-06 | U01 | US-04, US-09, US-13 |
| FR-07 | U01 | US-05, US-10 |
| FR-08 | U01 | US-06 |
| FR-09 | U01 | US-06 |
| FR-10 | U01 | US-01, US-07 |
| FR-11 | U01 | US-07 |
| FR-12 | U01 | US-08 |
| FR-13 | U01 | US-09, US-10 |
| FR-14 | U01 | US-11 |
| FR-15 | U01 | US-12 |
| FR-16 | U01 | US-11, US-13 |
| FR-17 | U01 | US-05, US-14 |
| FR-18 | U01 | US-15, US-16, US-17 |
| FR-19 | U01 | US-16 |

The existing 59 acceptance scenarios are included through their numbered references: 4, 3, 5, 3, 3, 4, 5, 3, 4, 2, 3, 3, 3, 3, 3, 6 and 2 for US-01 through US-17 respectively. Preserve the full criteria in stories.md rather than copying a second version here.

## 8. Non-functional obligations and later verification locations

All six NFRs belong to U01. Paths below are the approved future organization, not existing tests, installed packages or measured results. Relevant example checks accompany implementation; partial PBT complements them.

| Requirement | Responsible areas within U01 | Later verification / evidence |
| --- | --- | --- |
| NFR-01 Local runtime/model plan | Startup/configuration, C01, C03, C04, C05, C06 | Local app/Ollama setup and deliberate integration checks in tests/integration/; measure planned qwen3:4b and verify any qwen3:8b fallback hardware before claims |
| NFR-02 Project security/privacy | All nine modules and shared contracts/configuration, particularly C01/C03/C07/C08/C09 | Unit/API checks for malformed/oversized data, untrusted instructions, safe display/link targets, secret exclusion, session ownership and the exact record allowlist; review diagnostics/storage behavior |
| NFR-03 Maintainability/API | Shared contracts/startup and all module boundaries | Typed /api/v1/ commands, snake_case/ISO dates, invalid-input 422, permitted dependencies only; module-boundary/API checks and dependency/license review before tested version pinning |
| NFR-04 Example and integration verification | All stories; deterministic C02/C07 coverage specifically | tests/unit/ and tests/api/ with model/search/rate fakes; target at least 80% line coverage for deterministic preference/itinerary-validation modules; controlled live tests and manual Chrome/Safari flows before the demo |
| NFR-05 Partial PBT | Shared serialization, C02, C06 pure arithmetic, C07 and pure C09 transformations | tests/property/ plus reusable domain fixtures/strategies; round-trips/invariants, shrinking, reproducible seeds and CI integration; framework selection remains later DEF-05 |
| NFR-06 Bounds/measured performance | C01 progress, C03 limits, C04/C05/C06 attempts, C08 counters/guards | Deterministic API/integration failure fixtures for bounds, no duplicate work and preservation; actual latency/memory measurements later, without claiming configured limits are measured speed |

No mandatory live-model or stateful PBT is added by the partial opt-in. Security/Resiliency extensions remain disabled; project-specific NFR-02/06 still apply. The per-rule PBT-01–PBT-10 applicability table is in the unit definition.

## 9. Deferred decisions and verification assigned to U01

| Item | Unit and relevant modules | Design disposition and remaining work |
| --- | --- | --- |
| DEF-01 Evaluation fixtures | U01; C09, with C01/C03 full-flow support | AD3 resolved cities/profiles: New York City, London, Paris, ten profiles 4/3/3. Preserve fixtures and run real rounds later; no ratings/results invented |
| DEF-02 Rate integration | U01; C06 with C03/C08 lifecycle | AD4 selected documented ECB data, replacing WSJ. Verify actual acquisition/parsing and failure handling later; no silent provider substitution |
| DEF-03 Rate/budget rules | U01; C02/C03/C06/C07/C08 and C01 labels | AD5/AD6 resolved policy. Verify direction, date/freshness, pinned snapshots, decimal comparisons/rounding, unsupported prices and missing-budget pause later |
| DEF-04 Detailed contracts/algorithms/bounds | U01; shared contracts and all modules | Approved high-level interfaces remain; specify exact schemas, concurrency/receipt handling, normalization and remaining source/prompt/link numeric bounds in Functional/NFR Design before implementation |
| DEF-05 PBT selection | U01; contracts and pure C02/C06/C07/C09 functions | Select/review an appropriate framework in later NFR/design, then configure dependencies, generators, shrinking/seeds and CI; none is installed now |
| DEF-06 Model/hardware measurement | U01; C04 with C03/C01 integration | Measure quality, latency and memory on actual demo hardware; verify fallback hardware and return material choice changes to the team |
| DEF-07 Access/dependencies | U01; startup/configuration and external adapters | Verify Tavily entitlement/quotas/cost and dependency purpose, maintenance/licenses and tested versions before integration; no paid account or purchase assumed |

These are later obligations with explicit scope, not unresolved team answers that have been silently filled in. The unit assignment does not make a design decision equivalent to a working integration or passing test.

## 10. Cross-story integration checks to carry forward

- Intake/confirmation to discovery: unconfirmed or invalid preferences cannot start provider work; confirmed generation uses the separate cached baseline and cumulative activity quota.
- Discovery to accepted display: session-owned citations, cited locality evidence, feasible time/cost rules and honest uncertainty survive the model-to-validator-to-view boundary. Fewer/zero valid results remain possible.
- Feedback to update: ratings alone cause no replacement; an explicit update preserves all fixed activities/preferences, reuses caches/allowance and retains a disliked original when no suitable replacement exists.
- Failure/replay/reset: preserve accepted content and consumed counters; do not double count network replays or silently restore expired source authority. Confirm new trips before resetting state.
- Final evaluation: count each final activity once with its latest vote and actual full revision count; one final record per itinerary ID, replaced only by explicit reevaluation. Report failures/incomplete rounds and N/A denominators honestly.
- Record privacy/cleanup: persist only itinerary_id, activity_count, revision_request_count, baseline_overlap_count, link_check_results and activity_ratings with approved reasons. No profile-to-itinerary mapping, names, source URLs, session IDs, dates, budgets or raw chat enters ratings.jsonl. Keep Git exclusion and carry out demo-end cleanup later.

These checks connect existing acceptance criteria and approved design contracts. They are not extra stories or evidence that application tests have run. The existing trip-validation examples remain unchanged and separate from future planner tests.

## 11. Generated-artifact review boundary

Coverage is 17 stories, 59 existing scenarios, 19 FRs, six NFRs and seven DEF dispositions, all within U01 and its nine modules. The team approved this map, including its generated primary-module allocations, with the other two unit artifacts through "approve and finish inception ", recorded 2026-11-25T02:27:53Z. The actual final approval is logged; no additional answer or approval is invented. Units Generation and Inception are complete, with work stopped before Construction.
