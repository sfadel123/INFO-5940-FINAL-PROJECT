# Application Design Plan and Team Questions

Status: Plan approved by the team with AD1–AD6=A, recorded 2026-11-25T01:32:46Z. All five generated design artifacts separately approved with "approve & continue", recorded 2026-11-25T02:02:35Z; Application Design is complete.

The question/proposal wording below is retained as originally issued; all six actual answers are now recorded and approved. Original instructions: discuss all six questions together and fill each blank `[Answer]:` with a letter. For Other or requested changes, include the concrete change after the letter. Recommendations are not preselected answers. AD6 lets the team approve this concrete plan using its AD1–AD5 answers; approval of the generated design will remain a separate gate.

## Scope and basis

Use Standard depth for one local modular Python application. Read context: [requirements](../requirements/requirements.md), [stories](../user-stories/stories.md), [personas](../user-stories/personas.md), [execution plan](execution-plan.md), prior question answers, the existing-example reverse-engineering records, README.md, vision.md, tech-env.md, and the attached milestone. The actual technical input is tech-env.md; no file is renamed.

Keep the approved model/stack, one-traveler and one-city scope, 1–5 days, search allowances, separate cached baseline, scheduling, locality evidence, targeted revisions, feedback privacy and team-only evaluation. New choices below concern the open design tasks. A provider change in AD4 would explicitly revise the earlier WSJ decision and must be reconciled in affected inputs, requirements and stories after the team chooses it.

This stage defines responsibilities, interfaces, orchestration and dependencies. Detailed algorithms, implementation, dependency installation, runtime tests and model benchmarks belong to Construction. Stop after Units Generation approval.

## Execution checklist

- [x] P1. Record Workflow Planning approval and update its plan checkbox and state.
- [x] P2. Read approved context, installed design/common rules and extension configuration.
- [x] P3. Investigate the deferred rate-access question and document evidence/limitations.
- [x] P4. Evaluate all five question categories and prepare this concrete plan with blank answers.
- [x] P5. Receive and preserve all six actual team answers verbatim in audit.md.
- [x] P6. Analyze answers for contradictions or missing details; obtain targeted clarifications when necessary.
- [x] P7. Record explicit approval of the resolved plan before generating the design artifacts; AD6=A can supply this approval if all other answers are complete and consistent.
- [x] G1. Resolve DEF-01 through DEF-04 at the appropriate high-level design depth; retain genuinely later verification tasks without claiming they passed.
- [x] G2. Generate application-design/components.md with responsibilities and interfaces.
- [x] G3. Generate application-design/component-methods.md with signatures, purpose, and input/output types; defer detailed algorithms.
- [x] G4. Generate application-design/services.md with orchestration responsibilities and interactions.
- [x] G5. Generate application-design/component-dependency.md with a dependency matrix, communication patterns, and validated data-flow diagrams plus text alternatives.
- [x] G6. Generate application-design/application-design.md consolidating the design, evaluation fixtures, decision provenance, and unresolved Construction checks.
- [x] G7. Reconcile only affected prior documents when the team's actual answers change a prior decision; show every such change.
- [x] G8. Validate all FR/NFR and US-01–US-17 coverage, contracts, privacy, extension applicability, Markdown/diagrams and preservation of unrelated files.
- [x] G9. Update audit/state/checklists and present every generated or changed artifact for explicit Application Design approval.
- [x] G10. Record that separate approval before starting Units Generation. Construction remains excluded.

## Design scope and question coverage

| Required category | Proposed treatment | Team review |
| --- | --- | --- |
| Component identification | Separate UI/API, preferences, orchestration, integrations, validation, session state and evaluation within one application | AD1 and AD6 |
| Component methods | Typed requests/results, explicit error/status fields, commands instead of trusting browser copies | AD2, AD5 and AD6 |
| Service layer design | One coordinator controls intake, generation, revision and new-trip confirmation | AD1 and AD6 |
| Component dependencies | Internal function calls; adapters isolate Ollama, Tavily and the approved rate source; no network between internal modules | AD1, AD2, AD4 and AD6 |
| Design patterns | Modular application, provider adapters, deterministic validators, server-owned ephemeral state | AD1 and AD6 |

All five categories apply. Existing stack and deployment decisions are retained rather than reopened.

## Question AD1 — Who controls the generation steps?

Both choices keep the planned Qwen3 model, bounded tool use, Python validation and the single local application. Which coordination approach should the design use?

A) A Python-guided flow: the model interprets interests, proposes searches and candidates, and drafts an itinerary at defined steps. Python decides which step runs next and enforces every limit. This makes failures and revisions easier to trace. (Recommended)

B) A bounded agent loop: the model chooses the next allowed search or draft action repeatedly, while Python checks each action and stops at the same hard limits. This is more flexible but adds loop/state handling to test.

X) Other (describe the coordination approach after the answer tag).

[Answer]: A

## Question AD2 — How should the browser show generation progress?

Both choices show waiting/errors, preserve the previous valid itinerary, and prevent duplicate generation from repeated clicks. Neither adds cloud hosting or a queue service.

A) Keep one request open until the result is ready; show a waiting indicator and retry text, then display the validated result. This is the smaller local-demo implementation. (Recommended)

B) Start an in-memory job and have the browser poll its status to show named stages such as searching and validating. This needs an additional job/status contract; jobs disappear on server restart.

X) Other (describe the desired progress interaction after the answer tag).

[Answer]: A

## Question AD3 — Evaluation destinations and ten sample profiles

Choose a city set and the concrete fixture proposal below. These are synthetic test inputs, not researched travel recommendations or claims that matching activities are available.

A) New York City, London, and Paris, using the ten fixtures below: four for New York City, three for London, and three for Paris. This exercises three local time zones and USD/GBP/EUR examples. (Recommended)

B) Ithaca, London, and Paris, using the same fixtures with Ithaca replacing City 1. This lets the team evaluate a smaller nearby city as well as the two larger cities.

X) Other (name three cities and any changes to the ten fixtures after the answer tag; otherwise the 4/3/3 distribution and fixture values below apply in the named order).

[Answer]: A

### Proposed evaluation fixtures for AD3

For each round, R is the round's starting calendar date in that fixture's destination time zone. Start date is R plus the listed offset; end date is start plus duration minus one. Keep those resolved dates fixed throughout the round. Budgets cover one traveler's whole-trip activity tickets/fees, not project spending. Persona labels describe motivations, not additional stored personal data.

| Fixture | City slot | Persona | Start offset | Days | Budget | Interests |
| --- | --- | --- | --- | --- | --- | --- |
| F01 | City 1 | Recent Graduate | +7 days | 1 | USD 40 | Street art and independent galleries |
| F02 | City 1 | Abroad Student | +14 days | 2 | USD 120 | Pottery and community cultural events |
| F03 | City 1 | Cultural Explorer | +21 days | 3 | EUR 180 | Local history and small live-music venues |
| F04 | City 1 | Cultural Explorer | +28 days | 5 | GBP 250 | Printmaking and small museums |
| F05 | City 2 | Recent Graduate | +7 days | 2 | USD 90 | Architecture and public art |
| F06 | City 2 | Abroad Student | +14 days | 3 | GBP 140 | Theater workshops and local history |
| F07 | City 2 | Cultural Explorer | +21 days | 4 | EUR 220 | Textile arts and independent exhibitions |
| F08 | City 3 | Recent Graduate | +7 days | 1 | EUR 25 | Free galleries and sketching in public gardens |
| F09 | City 3 | Abroad Student | +14 days | 3 | USD 150 | Local music and cultural classes |
| F10 | City 3 | Cultural Explorer | +21 days | 5 | GBP 300 | Pottery and photography exhibitions |

Do not force an activity count or favorable rating. Rate actual results, make actual revision requests when warranted, and use only the final snapshot for activity KPIs. Boundary/failure cases remain separate deterministic tests, not substitutes for these ten team-evaluation profiles. Fixture labels, cities, dates, budgets and interests do not go into ratings.jsonl; no mapping from a persisted random itinerary ID to a profile is added.

## Question AD4 — Exchange-rate source after the access check

Supported automated WSJ access remains unverified. See the [access review](application-design-access-review.md) for the check and its limitations. The earlier D2 answer explicitly sends an infeasible/unverified integration back to the team before implementation. Choose a concrete path; no provider has been changed yet.

A) Change the planned source from WSJ to the European Central Bank's documented daily reference-rate download. Keep estimated USD conversions and source/date labels. This offers a published machine-readable format, with implementation and runtime verification still required. (Recommended)

B) Keep WSJ as the source, but change the MVP to use a small rate table manually prepared and checked by the team, with source URL and rate date. The app converts automatically from that table, but fetching new rates is manual. This requires the team to have access to the actual values; no values are invented here.

C) Keep planned automated WSJ retrieval and supply an official documented access method plus confirmation that the team can use it. Describe access without posting credentials. Design can proceed only after that method is verified; choosing this option alone is not proof of access.

X) Other (describe the rate source/access approach or proposed scope change after the answer tag).

[Answer]: A

## Question AD5 — What if the entered budget cannot be converted?

Unknown activity prices already remain flagged and excluded from the verified subtotal. This question concerns the whole trip budget: without its USD value, the app cannot compare the subtotal with the spending limit.

A) Pause generation or revision, explain the missing conversion, and offer retry or a confirmed budget/currency change. Preserve existing inputs and any valid itinerary. A change after generation follows the existing confirmed-new-trip rule. (Recommended)

B) Explain the missing comparison and allow the traveler to explicitly continue with a visibly budget-unverified itinerary. Keep any comparable activity subtotal, but do not claim that it fits the entered budget. Every affected generation/revision requires this acknowledgement.

X) Other (describe the desired behavior after the answer tag).

[Answer]: A

## Proposed design defaults for AD6 review

These are concrete proposals, not already-approved requirements. AD6 can accept them or request specific changes without making the team answer a separate question for every technical field. AD1–AD5 choices take precedence where indicated.

### Components and coordination

| Proposed responsibility | Boundary and main contract |
| --- | --- |
| Browser UI and FastAPI routes | Display chat/cards; accept typed commands; map validation failures to 422 and safe operation errors to explicit result/status fields |
| Preferences | Extract and validate destination, dates, original budget/currency and interests; confirm a typed preference summary |
| Trip coordinator | Coordinate confirmation, generation and targeted revision; enforce operation bounds and commit only validated results |
| Model adapter | Bounded Ollama calls through the approved client; return typed proposals; never execute model-directed code or arbitrary requests |
| Search and evidence adapter | Planned Tavily searches; register source records; distinguish baseline calls from quota-counted activity calls |
| Currency adapter and arithmetic | Acquire rates by AD4; validate dated rates; expose typed available/unavailable results and labeled USD conversions |
| Itinerary validation | Deterministic checks of dates, time intervals, budget, source ownership, locality overlap, distinctness and revision preservation |
| Session store | Own confirmed preferences, accepted itinerary, ratings/locks, sources, baseline, rate snapshot, quota counters and version in server memory |
| Evaluation | Check source-link availability and compute agreed final-snapshot KPIs; write only the approved anonymous field allowlist |

These are logical responsibilities, not nine deployed services or invented teammate assignments. Exact methods, schemas and dependencies will be written in the generated design after plan approval. Internal calls pass typed objects. Provider adapters allow routine tests to use fakes; deterministic functions remain independent of network I/O.

### State and interface contracts

- Keep authoritative trip state as well as source provenance in server memory. Browser memory is a display/input copy, not authority for preferences, locks, counters or accepted activities. Do not add localStorage, cookies for persistence, a database, or saved profiles.
- Create a random session ID when starting the local flow; send it on subsequent requests. A separate random itinerary ID is used only for evaluation. Reject unknown, expired or cross-session references. Clear all sessions on restart and the old session on a confirmed new trip; expire inactive sessions after two hours, excluding active operations. A browser reload starts a fresh flow; it does not promise recovery.
- Commands include session ID, request ID and expected state version. Keep one mutation in progress per session. Replayed request IDs return the prior result without charging searches or counting a revision twice; stale versions get a conflict response. Session reset/restart invalidates the old identifiers.
- Retain planned `/api/v1/chat` and `/api/v1/feedback`. Define separate typed contracts for confirming preferences, generating, updating and confirming a new trip. AD2 determines whether generation returns a completed result or a job handle with a status route.
- Proposed shared types: confirmed preferences; source record; baseline entry; rate snapshot; candidate/activity; accepted itinerary; rating command; operation result; anonymous evaluation record. Source references contain IDs and supporting evidence, resolved on the server. Do not accept a browser/model URL as proof of retrieval.
- The model may propose destination/country and an IANA time-zone identifier for the confirmation summary. Python validates that identifier; ambiguous destinations/time zones require correction and confirmation, not an assumed city. No additional geocoding provider is selected. Detailed resolution and time-boundary cases belong to Functional Design.

### Limits and errors

| Proposed contract | Initial design value |
| --- | --- |
| User text | Destination 1–120 characters; interests 1–1,000; each chat message 1–2,000; total API request body at most 64 KiB |
| Money input | Finite nonnegative decimal, at most 1,000,000,000 in the selected currency and up to six fractional digits; reject NaN/infinity/negative values |
| Model requests | At most two attempts per intake message; at most twelve calls including retries per generation/update; no unbounded repair loop |
| Model output | At most 8,192 output tokens per call and a 64 KiB structured-response limit; invalid/truncated output is not committed |
| Timeouts | Model call 120 seconds; search/rate call 30 seconds; entire generation/update 300 seconds; inner attempts use only remaining time |
| Retries | Existing one automatic retry for ordinary model/activity-search failure, only within remaining call/time/search bounds; failed activity-search attempts consume allowance |
| Result size | At most four activities per day and twenty per five-day trip; fewer/zero allowed under the approved evidence and feasibility rules |

These numbers are proposed resource limits, not measured speed or hardware guarantees. Construction must test them on the demo laptop and return material changes to the team. The confirmed 1–5-day trip rule, three optional clarification turns and cumulative search allowance remain unchanged.

### Baseline, evidence and revisions

- Cache the up-to-ten baseline search-result records, retaining evidenced attraction names/URLs from the returned material. There is no separate crawl or fresh baseline during revisions. The provider's search-result rank defines the baseline; do not claim it is an independently verified popularity ranking.
- Python compares normalized names and URLs. Proposed normalization: Unicode normalization/case-folding, trimmed/collapsed whitespace; lowercase URL host, remove fragments and known tracking parameters, preserve meaningful path/query identity. Use only source-evidenced aliases. Shared listing-page URLs alone do not prove two differently named activities are the same attraction; uncertain identity is excluded rather than classified as local by guesswork.
- A local-criterion claim carries its session-owned source ID and supporting excerpt. Validate that the citation exists and the excerpt occurs in retained evidence; model judgments still require team quality evaluation. A working link is not factual verification.
- A successful baseline is reused even when a later step fails. A failed/empty baseline stops that attempt; the user's retry can try again. No automatic baseline-retry loop is introduced. Activity searches and retries share the existing cumulative allowance across the initial itinerary and all revisions.
- For revision, provide the model with only eligible thumbs-down targets plus the fixed context needed to fit replacements. Compare the submitted result with canonical server state and reject edits to locked/neutral activities or preferences. Commit valid replacements together; preserve the previous itinerary on operation failure and keep an unmatched disliked activity visible.

### Currency policy, conditional on AD4/AD5

- Conversion coverage is USD identity plus currencies with valid dated rates from the approved source; EUR/GBP must be available for the proposed fixtures. The budget currency list reflects that coverage, with USD as default. An unavailable selected budget currency follows AD5; unsupported activity currencies remain unverified and excluded from the verified subtotal. This does not restrict accepted destination cities.
- A rate snapshot must have a source URL, quoted pair/direction and source date. Accept only positive finite rates with a source date no more than seven calendar days old at use; reject future-dated or undated rates. No live rates are chosen in this plan.
- Acquire a snapshot before generation and pin it to the trip for consistent revisions. Recheck freshness on update; if it is stale, explain the problem and require retry/new-trip confirmation as applicable, without silently repricing unaffected activities. A new trip obtains a new snapshot.
- Normalize each usable rate to USD per one unit of the original currency. Invert the opposite quotation explicitly. For an approved EUR-based source, derive the USD cross-rate from its same-date currency/USD quotations. USD-to-USD is identity without an external rate. Reject missing/incompatible pairs rather than guessing.
- Use decimal arithmetic; compare unrounded converted amounts. Display USD values rounded to cents using half-up rounding. Sum unrounded verified amounts before rounding the displayed subtotal and explain possible one-cent display differences. Preserve each original amount/currency and label conversions as estimates with source/date.
- AD4=B means a team-checked local source table instead of automatic fetching; missing/stale table data follows the same policy. AD4=C still needs evidence of a supported accessible method. AD5 controls whether a missing budget comparison stops work or permits explicitly acknowledged uncertainty.

### Evaluation and remaining verification

- Use AD3's fixtures in team rounds; no live-user telemetry or new evaluator account/dashboard. Only deliberate evaluation completion writes a final anonymous record, using the existing six allowed field groups, including the optional preset reasons within ratings.
- Perform bounded HTTP/HTTPS link checks on server-owned source URLs; record load results without persisting source URLs/profile fields in the ratings file. Treat failed/blocked loads as not verified. Restrict redirects/targets away from local/private services; this is part of the project's network-boundary requirement, not a re-enabled extension.
- Under the approved validator, every admitted non-baseline activity has qualifying locality evidence; final local count can therefore be derived as activity count minus baseline-overlap count. Do not infer locality merely from an unchecked count. Persist no new locality/profile field. Calculate empty denominators as N/A and report generation failures separately.
- Preserve the existing example code. Later Functional Design specifies detailed schemas/algorithms; later NFR/design selects the partial-PBT framework (DEF-05). Construction verifies model quality/hardware (DEF-06), provider accounts/quotas and tested dependency versions/licenses (DEF-07). No provider account, paid plan, implementation or test success is assumed here.

## Question AD6 — Approve this concrete design plan or request changes

After answering AD1–AD5, review the component/contract defaults above and the execution checklist. This is approval to generate the design documents, not approval of documents that do not exist yet.

A) Approve this plan with our AD1–AD5 answers and the listed defaults. After validating our answers and any required access evidence, generate the five design artifacts for our separate review. (Recommended if the proposals fit the team's intent)

B) Request changes before generation. List the exact defaults, steps or fixture details to change after the answer tag; leave the design artifacts ungenerated until the revised plan is resolved.

X) Other (describe the requested plan or approval boundary after the answer tag).

[Answer]: A 

## Extension applicability at this planning checkpoint

Security Baseline is N/A (disabled by C5=B). Resiliency Baseline is N/A (disabled by Q17=B). Their skips are recorded in audit.md. Approved project-specific privacy, validation and failure requirements still apply. Partial PBT is preserved without expanding its scope.

| Rule | Status now | Reason / later obligation |
| --- | --- | --- |
| PBT-01 | N/A | Advisory in partial mode; detailed property identification belongs to Functional Design |
| PBT-02 | N/A | No serialization implementation/tests generated; round-trip obligation retained |
| PBT-03 | N/A | No pure-function implementation/tests generated; invariant obligation retained |
| PBT-04 | N/A | Advisory in partial mode; no idempotency implementation |
| PBT-05 | N/A | Advisory in partial mode; no oracle implementation |
| PBT-06 | N/A | Advisory in partial mode; no mandatory stateful-PBT expansion |
| PBT-07 | N/A | Domain generators are future test work |
| PBT-08 | N/A | Shrinking, failure seeds and CI execution are future test work |
| PBT-09 | N/A | Framework selection/configuration is explicitly deferred to later NFR/design and Construction |
| PBT-10 | N/A | Advisory in partial mode; meaningful example-test obligations retained |

No applicable extension finding blocks executing this plan. All six answers are complete and consistent, and the plan is approved. Generated design artifacts are complete and separately approved, recorded 2026-11-25T02:02:35Z. This file contains no diagram; generated design diagrams have structural checks and text alternatives.

## Recorded answer analysis

All six answers select A. AD1 selects Python-guided orchestration; AD2 selects one open request with waiting/error UI; AD3 selects New York City/London/Paris and the ten listed fixtures; AD4 explicitly replaces the previous planned WSJ source with ECB daily reference rates; AD5 pauses generation/revision when budget conversion is unavailable; AD6 approves this concrete plan and listed defaults. The user's accompanying message confirms approval of the choices.

No ambiguous or combined answers require follow-up. AD4 is an intentional approved change to C3/D2, not a reason to infer that WSJ now works. The earlier access check established a documented alternative format, not a working integration; parsing/provider integration remains Construction work. Other option text above is retained as historical question context. No generated-artifact approval is inferred.

## Generated artifact review checkpoint

All five required artifacts and the itemized application-design-review.md have been explicitly approved. P1–P7 and G1–G10 are complete. Original question/option/default wording is retained as the issued plan, with actual A answers unchanged. Units planning has started; Construction remains excluded.

## Generated-artifact approval recorded

The team explicitly approved the generated design with "approve & continue", recorded 2026-11-25T02:02:35Z. G10 and Application Design are complete. This authorizes Units planning; it does not approve a future Units plan/artifact or authorize Construction. The preceding issued question text and raw answers remain unchanged.
