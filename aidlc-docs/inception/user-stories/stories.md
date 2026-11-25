# User Stories — Personalized Cultural Travel Planner

Status: User Stories baseline approved at 2026-11-25T01:09:54Z; reconciled with actual AD1–AD6 choices approved at 2026-11-25T01:32:46Z. Still 17 stories and 59 Given / When / Then scenarios. Generated design approval is separate; no implemented functionality or passing tests claimed.

## Basis and organization

The story plan was approved in the team's recorded “Ok, user stories approval is done” response, with SC1 subsequently removing Fiancees. The selected method is user-journey organization (S2=A) and Given / When / Then criteria (S3=A). Traveler personas are P01 Recent Graduate, P02 Abroad Student, and P03 Cultural Explorer; R01 Team Evaluator is a separate project role.

Sources: [requirements](../requirements/requirements.md), [personas](personas.md), [resolved story plan](../plans/story-generation-plan.md), and [actual clarification](../plans/story-planning-clarification-questions.md). All 19 FRs, all 6 NFRs, and all 7 DEF items are traced below. Any later change to those requirements must be recorded through the workflow.

The six journey sections express user outcomes, not sprint priorities, architecture units, or an implementation schedule. Dependencies state needed context; they do not require combining stories into one large delivery. Application Design answers now resolve the cities, rate source/policy and high-level contracts; remaining detailed implementation/verification stays explicitly deferred. See [Application Design](../application-design/application-design.md).

## Story index

| ID | Outcome | Personas / role |
| --- | --- | --- |
| US-01 | Enter valid trip preferences | P01, P02, P03 |
| US-02 | Clarify interests and confirm the summary | P01, P02, P03 |
| US-03 | Receive relevant local recommendations | P01, P02, P03 |
| US-04 | Inspect the recommendation sources | P01, P02, P03 |
| US-05 | Review a clear daily plan | P01, P02, P03 |
| US-06 | Receive a feasible local-time schedule | P01, P02, P03 |
| US-07 | Understand comparable costs and uncertainty | P01, P02, P03 |
| US-08 | Rate activities without immediate changes | P01, P02, P03 |
| US-09 | Replace only the disliked activities | P01, P02, P03 |
| US-10 | Understand when no replacement is possible | P01, P02, P03 |
| US-11 | Confirm preference changes as a new trip | P01, P02, P03 |
| US-12 | Recover from generation or search failures | P01, P02, P03 |
| US-13 | Keep evidence tied to the active session | P01, P02, P03 |
| US-14 | Use the desktop flow accessibly | P01, P02, P03 |
| US-15 | Record an anonymous evaluation round | R01 |
| US-16 | Calculate KPIs from final itineraries | R01 |
| US-17 | Delete evaluation ratings after the demo | R01 |

## 1. Confirm the trip

### US-01 — Enter valid trip preferences

As a traveler, I want to provide my destination, dates, interests, and activity budget so that the plan starts from my actual constraints.

**Personas / role:** P01, P02, P03. **Requirements:** FR-01, FR-10, NFR-02.

**Dependencies / design boundaries:** No earlier story outcome required. AD6 sets initial bounds; exact schema implementation remains DEF-04.

**Acceptance criteria:**

1. **Given** a single destination and complete required preferences, **when** the traveler submits a trip starting today or later in destination-local time and lasting one to five inclusive calendar days, **then** the dates are accepted for preference confirmation; a same-day trip counts as one day.
2. **Given** a reversed date range, past live start date, or trip longer than five inclusive days, **when** the traveler requests generation, **then** the app explains the invalid dates and requests correction before generation; historical dates remain allowed only in deterministic tests.
3. **Given** a missing or invalid required field, **when** the intake is checked, **then** the app requests the needed correction and does not invent a destination, dates, budget, currency, or interests.
4. **Given** a traveler entering a total activity budget, **when** the budget is collected, **then** it refers to one person for the whole trip, has a selected currency defaulting to USD, and excludes flights, lodging, meals, and local transport.

### US-02 — Clarify interests and confirm the summary

As a traveler, I want a short clarification conversation and a preference summary so that the itinerary reflects what I meant.

**Personas / role:** P01, P02, P03. **Requirements:** FR-02.

**Dependencies / design boundaries:** Valid required preferences from US-01 before generation.

**Acceptance criteria:**

1. **Given** required fields are collected but an interest is vague, **when** the assistant clarifies that interest, **then** it asks no more than three additional interest-clarification turns before presenting the valid preference summary for confirmation.
2. **Given** the interest-clarification limit has been reached but a required field is missing or invalid, **when** the intake is evaluated, **then** the app still requests the required correction rather than treating the turn limit as permission to guess.
3. **Given** a valid preference summary is displayed, **when** the traveler has not confirmed it or requests a correction, **then** generation waits; it begins only after the traveler explicitly confirms the valid summary.

## 2. Discover and review the itinerary

### US-03 — Receive relevant local recommendations

As a traveler, I want recommendations matched to my interests with evidence of local relevance so that I can discover experiences beyond the usual tourist list.

**Personas / role:** P01, P02, P03. **Requirements:** FR-03, FR-04, FR-05, NFR-02.

**Dependencies / design boundaries:** Confirmed preferences from US-02. AD6 defines high-level matching/ownership; detailed algorithms and provider access remain DEF-04/DEF-07. Baseline failure follows US-12.

**Acceptance criteria:**

1. **Given** a confirmed trip of d days, **when** activity searches are requested for initial generation or later revisions, **then** the same trip uses at most min(2 * d, 10) activity searches in total, each returning at most five results; retries do not reset or exceed that allowance.
2. **Given** a new itinerary generation, **when** the system builds the popularity baseline, **then** it runs the separate Tavily search top things to do in [destination] once for that generation, returns up to ten results, and caches it for revisions; this search is outside the activity-search allowance and five-result cap.
3. **Given** baseline results include titles, URLs, snippets, or provider-returned page content, **when** attractions are identified for comparison, **then** only evidenced names are used, with Python checking name/URL overlap; no browser scraping or invented attraction names are added.
4. **Given** a candidate itinerary is checked against a usable baseline, **when** activities are accepted, **then** at most one activity matches the baseline; every other activity is absent from it and cites evidence that it is independent/not a chain, a time-limited event, or found through a local source such as local news, city/venue listings, or a community organization.
5. **Given** an activity is recommended, **when** it is shown to the traveler, **then** one sentence explains its fit to the confirmed interests, and a non-baseline activity without evidence of a local criterion is not accepted merely because it is absent from the baseline.

### US-04 — Inspect the recommendation sources

As a traveler, I want source links for recommended activities so that I can inspect the evidence and confirm details with the venue.

**Personas / role:** P01, P02, P03. **Requirements:** FR-06, NFR-02.

**Dependencies / design boundaries:** Retrieved candidates from US-03 and source ownership from US-13.

**Acceptance criteria:**

1. **Given** a recommended activity references a source, **when** the itinerary is accepted and displayed, **then** the backend resolves a retrieved, session-owned source ID to its URL instead of trusting a model-written URL.
2. **Given** a proposed activity has a missing, invented, unknown, or cross-session source ID, **when** the itinerary or revision is validated, **then** the affected submitted data is rejected before acceptance.
3. **Given** source text and links are displayed, **when** the traveler reads or follows them, **then** text is escaped, link schemes are limited to HTTP/HTTPS, and a source link is not presented as a guarantee of price, hours, or availability; unknown prices, hours, or availability are labeled unverified.

### US-05 — Review a clear daily plan

As a traveler, I want activities organized by day with useful details so that I can understand the proposed trip and any gaps.

**Personas / role:** P01, P02, P03. **Requirements:** FR-07, FR-17.

**Dependencies / design boundaries:** Valid sourced recommendations from US-03/04, with schedule and cost checks from US-06/07.

**Acceptance criteria:**

1. **Given** sufficient suitable distinct activities fit the constraints, **when** the itinerary is displayed, **then** it targets two to four activities per day in day-grouped cards, each showing scheduled time, location, duration, estimated cost or unverified status, source link, and interest-match explanation.
2. **Given** too few suitable distinct activities are available, **when** the itinerary is displayed, **then** it shows fewer, states how many were found, and suggests broadening interests without silently changing them or inventing/repeating activities to fill slots.
3. **Given** no candidate survives the applicable constraints despite a usable baseline, **when** the result is displayed, **then** the app reports zero suitable activities and an honest empty outcome rather than fabricating a complete itinerary.

### US-06 — Receive a feasible local-time schedule

As a traveler, I want an itinerary that respects time constraints so that the suggested activities can fit together.

**Personas / role:** P01, P02, P03. **Requirements:** FR-08, FR-09.

**Dependencies / design boundaries:** Candidate evidence from US-03/04. Detailed time schemas remain DEF-04.

**Acceptance criteria:**

1. **Given** activities have durations and proposed destination-local times, **when** the schedule is validated, **then** each activity fits entirely between 9:00 AM and 10:00 PM, no activities overlap, and at least a 30-minute buffer separates consecutive activities.
2. **Given** a source provides opening hours, **when** an activity is scheduled, **then** its scheduled interval fits those hours; when hours are not known, the displayed hours are labeled unverified.
3. **Given** a source supplies a duration or one must be estimated, **when** the schedule is validated, **then** the source duration is used when available; otherwise the estimate is based on activity type/similar activities and visibly labeled; every duration is positive and fits the schedule, with no fixed 30–180-minute estimate range.
4. **Given** a time-limited event lacks retrieved evidence of an occurrence during the trip or has incompatible dates, **when** candidate activities are scheduled, **then** the event is omitted and the honest-shortfall rule applies; unknown opening hours do not justify inventing an event occurrence.

### US-07 — Understand comparable costs and uncertainty

As a traveler, I want an understandable activity total with conversion and uncertainty labels so that I can assess it against my budget.

**Personas / role:** P01, P02, P03. **Requirements:** FR-10, FR-11.

**Dependencies / design boundaries:** Budget from US-01 and sourced prices from US-04. AD4 selects ECB after the WSJ access review; AD5/AD6 resolve the rate policy and missing-budget behavior. Integration remains unverified.

**Acceptance criteria:**

1. **Given** a selected-currency budget and verified activity prices have valid conversions, **when** the itinerary total is calculated, **then** the original budget amount/currency remains visible, the budget and comparable prices are expressed in USD for comparison, and conversions are labeled estimates with their source and rate date.
2. **Given** all included comparable prices and the budget have valid conversions, **when** a candidate itinerary is checked, **then** the known comparable total must fit the converted budget; only activity tickets/fees for one traveler are counted.
3. **Given** an activity price is unknown or lacks a valid conversion, **when** the subtotal is displayed, **then** that cost is flagged as unverified and excluded from the verified subtotal, not treated as a verified zero; the app does not claim full budget compliance.
4. **Given** the selected budget cannot be validly converted, **when** generation or revision is requested, **then** it pauses with an explanation and retry/correction action, preserving the inputs and last valid itinerary; changing confirmed preferences requires a confirmed new trip (AD5=A).
5. **Given** currency conversion is implemented later, **when** rates are obtained, **then** they use the explicitly selected ECB reference data (AD4=A), with positive finite dated rates, the approved seven-day freshness/direction/rounding policy and a snapshot pinned for revisions (AD6=A); values are not invented, obtained from model memory, scraped through a browser or silently sourced elsewhere. Runtime integration must be verified in Construction.

## 3. Give feedback and revise

### US-08 — Rate activities without immediate changes

As a traveler, I want to mark what I like and dislike so that I control which activities can change.

**Personas / role:** P01, P02, P03. **Requirements:** FR-12, NFR-02.

**Dependencies / design boundaries:** An itinerary from US-05. Replacement occurs only through US-09.

**Acceptance criteria:**

1. **Given** an activity is displayed, **when** the traveler selects thumbs down, **then** the activity is marked disliked and remains in place; the rating alone does not invoke replacement.
2. **Given** an activity is displayed, **when** the traveler selects thumbs up, **then** the activity is locked against itinerary-update replacement.
3. **Given** the traveler adds an optional rating reason, **when** structured feedback is accepted, **then** the reason is absent or one of too touristy, too expensive, wrong time, or not my interest; no free-text feedback field is offered and unrestricted feedback strings are rejected, without disabling ordinary conversational chat.

### US-09 — Replace only the disliked activities

As a traveler, I want an explicit update to replace only disliked activities so that the rest of my plan stays intact.

**Personas / role:** P01, P02, P03. **Requirements:** FR-13, FR-03, FR-04, FR-06.

**Dependencies / design boundaries:** Existing itinerary and feedback from US-05/08. No-candidate behavior is US-10.

**Acceptance criteria:**

1. **Given** activities have been marked disliked, **when** the traveler clicks Update itinerary or explicitly asks in chat, **then** only the thumbs-down activities are considered for replacement; ratings alone do not trigger this action.
2. **Given** a suitable replacement exists, **when** the revision is accepted, **then** it is distinct and meets the applicable locality, evidence, schedule, budget, and session-source rules while every locked or unaffected activity and every preference remains unchanged.
3. **Given** an update needs additional activity evidence, **when** searches are made, **then** it reuses the cached baseline and the original cumulative activity-search allowance; the update does not create a new baseline or reset the allowance.
4. **Given** a proposed revision changes a locked/unaffected activity or a preference, **when** the revision is validated, **then** it is not accepted as the requested targeted update.

### US-10 — Understand when no replacement is possible

As a traveler, I want an honest explanation when no replacement fits so that I can decide whether to keep the plan or start again.

**Personas / role:** P01, P02, P03. **Requirements:** FR-13, FR-03, FR-07.

**Dependencies / design boundaries:** An explicit update from US-09. Changing interests requires US-11.

**Acceptance criteria:**

1. **Given** no distinct suitable replacement fits the remaining constraints, **when** an update is attempted, **then** the original activity remains visibly disliked, the app explains that no replacement was found, and it suggests broader interests for a new itinerary without changing preferences or other activities.
2. **Given** the cumulative activity-search allowance is exhausted, **when** a replacement is requested, **then** only existing candidates are considered; if none fits, the same retain-and-explain result applies rather than a fresh search allowance or an invented activity.

## 4. Start a different trip

### US-11 — Confirm preference changes as a new trip

As a traveler, I want to confirm a new trip before changing my preferences so that I do not accidentally lose the current itinerary.

**Personas / role:** P01, P02, P03. **Requirements:** FR-14, FR-16, FR-04, FR-03.

**Dependencies / design boundaries:** Current preferences/itinerary. A confirmed new trip follows US-01/02 for valid intake.

**Acceptance criteria:**

1. **Given** the traveler asks to change destination, dates, budget, or other trip preferences, **when** chat proposes a new trip, **then** the old itinerary, preferences, and locks remain intact until explicit confirmation.
2. **Given** the traveler declines or has not confirmed the new trip, **when** the existing state is used, **then** the old trip is not discarded or silently revised.
3. **Given** the traveler confirms the new trip, **when** the new trip begins, **then** the old itinerary is replaced through a fresh session and valid preference confirmation; its generation has a fresh baseline and activity-search allowance rather than being counted as a revision of the old trip.

## 5. Recover and use the interface

### US-12 — Recover from generation or search failures

As a traveler, I want clear progress and recoverable errors so that a service failure does not erase my useful work or produce fabricated results.

**Personas / role:** P01, P02, P03. **Requirements:** FR-15, FR-04, NFR-06, NFR-02.

**Dependencies / design boundaries:** Generation or revision attempt. AD6 sets initial call/output/deadline bounds; detailed enforcement remains DEF-04 and model measurements remain DEF-06.

**Acceptance criteria:**

1. **Given** an ordinary model or activity-search timeout/service error occurs, **when** the app retries, **then** it allows at most one automatic retry within existing request/search limits and shows progress without resetting allowances.
2. **Given** that failure persists or a retry cannot occur within the remaining bounds, **when** the app reports the failure, **then** it offers an understandable retry action, preserves the last valid itinerary and inputs, exposes no credentials/internal traces, and invents no substitute results.
3. **Given** a new generation has no usable baseline because results are empty or unavailable, **when** baseline validation runs, **then** generation stops with an explanation and retry action; an empty baseline is not used to declare all activities local.

### US-13 — Keep evidence tied to the active session

As a traveler, I want the itinerary to use evidence from my active session so that stale or unrelated sources cannot be accepted as my recommendations.

**Personas / role:** P01, P02, P03. **Requirements:** FR-16, FR-06, NFR-02.

**Dependencies / design boundaries:** AD6 selects server-authoritative state, bootstrap IDs, two-hour idle expiry, reset/restart clearing and request/version guards; implementation details remain DEF-04. New-trip confirmation is US-11.

**Acceptance criteria:**

1. **Given** retrieved sources and a baseline are in the active session, **when** the browser submits an itinerary or revision, **then** it sends the random session ID and the backend checks every source ID against that session; unknown or cross-session references are rejected.
2. **Given** the server restarts, **when** old source or baseline references are submitted, **then** the server-memory caches have been cleared and stale references are rejected rather than restored from browser claims.
3. **Given** the browser reloads or submits a display/input copy, **when** session state is evaluated, **then** reload starts a fresh flow and server memory remains authoritative for preferences, accepted activities, locks, sources and counters; expired references cannot restore state and no persistent account/profile/browser storage is introduced (AD6=A).

### US-14 — Use the desktop flow accessibly

As a traveler, I want understandable, keyboard-operable controls so that I can complete the planning flow in the supported desktop browsers.

**Personas / role:** P01, P02, P03. **Requirements:** FR-17.

**Dependencies / design boundaries:** Applies across traveler stories; it is a cross-cutting interaction requirement, not a separate implementation sequence.

**Acceptance criteria:**

1. **Given** the app is used in desktop Chrome or Safari, **when** the traveler follows the planning flow, **then** the English interface shows chat alongside day-grouped cards and provides readable source links, progress, and errors.
2. **Given** the traveler uses only a keyboard, **when** they confirm preferences, request generation, rate activities, update the itinerary, or confirm a new trip, **then** the relevant controls are operable and the current focus is visible.
3. **Given** ratings, statuses, or errors are shown, **when** the traveler reads the interface, **then** meaning is available through text labels and readable contrast rather than color alone; mobile-specific layout testing is outside this MVP.

## 6. Evaluate the MVP as a team

### US-15 — Record an anonymous evaluation round

As a Team Evaluator, I want a consistent evaluation round with minimal anonymous records so that the team can assess results without collecting live-user data.

**Personas / role:** R01. **Requirements:** FR-18, NFR-02.

**Dependencies / design boundaries:** AD3 selects ten fixtures across New York City, London and Paris (4/3/3), documented in Application Design; actual evaluation remains future work.

**Acceptance criteria:**

1. **Given** the team has the approved evaluation fixtures, **when** it runs an evaluation round, **then** the round uses ten sample traveler profiles across three destinations, rather than live users, and uses random itinerary identifiers.
2. **Given** evaluation results are persisted, **when** a ratings.jsonl record is written, **then** it contains only random itinerary ID, activity count, revision-request count, baseline-overlap count, link-check results, and activity ratings with permitted preset reasons; destinations, travel dates, budgets, chat text, and session IDs are excluded.
3. **Given** evaluation records exist locally, **when** files are prepared for version control, **then** ratings.jsonl is excluded through .gitignore and is never committed; the evaluation role does not require a new account or dashboard.

### US-16 — Calculate KPIs from final itineraries

As a Team Evaluator, I want reproducible final-itinerary metrics so that repeated revisions do not distort the project evaluation.

**Personas / role:** R01. **Requirements:** FR-19, FR-18.

**Dependencies / design boundaries:** Permitted records and final validation context from US-15; source links use the evidence rules in US-04. KPI targets are evaluation goals, not claimed achievements.

**Acceptance criteria:**

1. **Given** an itinerary has undergone revisions and ratings, **when** activity metrics are calculated, **then** only its final recommended activities are counted, each once, using its latest rating; replaced activities are not pooled with final activities.
2. **Given** final activity ratings exist, **when** activity approval is calculated, **then** the numerator is thumbs-up rated final activities and the denominator is all rated final activities; the target is at least 70%.
3. **Given** test itineraries have revision-request counts, **when** revision rate is calculated, **then** the numerator is test itineraries needing more than two revision requests and the denominator is test itineraries; use the full request count, with a target under 30%.
4. **Given** final recommendations have validated locality evidence, **when** local discovery is calculated, **then** the numerator is activities absent from the baseline and satisfying a cited local criterion, and the denominator is all final recommended activities; the target is at least 70%.
5. **Given** final recommendations have source links, **when** automated link-loading checks run, **then** source coverage is activities whose source link loads divided by all final recommended activities, with a 100% target; loading is not reported as proof of factual accuracy.
6. **Given** generation failures or an empty metric denominator occur, **when** the evaluation is reported, **then** failures are reported separately and the empty-denominator metric is N/A, never 100%.

### US-17 — Delete evaluation ratings after the demo

As a Team Evaluator, I want the ratings file removed after the final demo so that the agreed retention limit is respected.

**Personas / role:** R01. **Requirements:** FR-18, NFR-02.

**Dependencies / design boundaries:** The local evaluation file from US-15; deletion is future operational work, not performed by this story document.

**Acceptance criteria:**

1. **Given** the final demo has concluded and ratings.jsonl exists, **when** the team carries out the agreed cleanup, **then** the local ratings file is deleted rather than retained for a later project phase.
2. **Given** evaluation and cleanup are reviewed, **when** the team checks the repository and retained records, **then** ratings were never committed and no raw conversation or extra traveler-profile fields were collected as a substitute.

## Cross-cutting technical and quality acceptance obligations

These constraints apply to the relevant stories and later design/test artifacts. They are not fabricated end-user features, completed implementations, or additional personas.

### NFR-01 — Local deployment and planned model

One modular Python 3.12 application using pip/venv, FastAPI, Pydantic v2, Uvicorn, Jinja2 and minimal browser JavaScript; app and Ollama on the same laptop. qwen3:4b through the OpenAI Python client and Ollama-compatible API is planned, with qwen3:8b on higher-memory hardware as fallback. External search and the selected ECB reference-data download use HTTPS. Model/tool quality and hardware suitability remain unverified Construction work.

**Coverage:** All traveler stories; DEF-02, DEF-06, DEF-07.

### NFR-02 — Security and privacy across all stories

Keep secrets in runtime environment variables and out of Git, browser responses and logs. Validate typed input/output and sizes, source ownership and model structures; escape text and limit links to HTTP/HTTPS. Retrieved instructions are untrusted data; Python enforces permitted tools, with no arbitrary code/shell/network execution. Bind local services to loopback and use HTTPS externally. Send search only needed destination/dates/interests, not entire conversations. Collect no payment/passport/home-address/account credentials. Bound tool calls, retries, output and timeouts. Diagnostics use request IDs, timings and error categories, not raw profiles. No accounts or public deployment.

**Coverage:** US-01, US-03, US-04, US-08, US-12, US-13, US-15, US-17; DEF-04.

### NFR-03 — Maintainability and API constraints

Separate approved responsibilities within the local app; design exact modules later. Use typed JSON /api/v1/ endpoints, snake_case fields/functions, ISO dates and HTTP 422 for invalid inputs. Respect tech-env.md exclusions: no LangChain/LangGraph/CrewAI, external browser scraping, direct PyTorch/Transformers model hosting, or payment/booking SDKs. Review dependency purpose/maintenance/licenses, pin tested versions, and run pip-audit during Construction. Existing example endpoints are not implemented planner features.

**Coverage:** Cross-cutting design obligation; DEF-04, DEF-07.

### NFR-04 — Example-based and integration verification

Use pytest and FastAPI TestClient/HTTPX; mock model/search/rate responses in routine tests and exercise deterministic rules directly. Target at least 80% line coverage for deterministic preference/itinerary validation. Unit/API checks precede merging; controlled live integrations and manual Chrome/Safari flows precede the final demo. Acceptance scenarios guide those future checks; none has been executed here.

**Coverage:** All stories; especially boundaries and failures; DEF-02, DEF-06, DEF-07.

### NFR-05 — Partial property-based testing

Apply PBT to suitable pure functions and serialization round-trips: PBT-02/03/07/08/09 cover round-trip/invariant properties, domain generators, shrinking, reproducible failure seeds, CI integration and an appropriate framework. Example tests remain complementary. Do not expand into mandatory live-model/stateful PBT, choose a framework, or configure CI in this stage.

**Coverage:** Cross-cutting verification obligation; DEF-05.

### NFR-06 — Bounded operation and measured performance

Preserve request/search bounds and safe failures with progress. Verify quota behavior and retention of the prior itinerary with deterministic failure cases. Benchmark actual model latency/memory on the demonstration laptop during Construction before claiming numerical performance targets.

**Coverage:** US-03, US-09, US-10, US-12; DEF-04, DEF-06.

## Requirement traceability

Every functional requirement has story coverage. All non-functional requirements have a cross-cutting acceptance obligation even where a standalone user story would be artificial.

| Requirement | Story coverage / acceptance obligation |
| --- | --- |
| FR-01 | US-01 |
| FR-02 | US-02 |
| FR-03 | US-03, US-09, US-10, US-11 |
| FR-04 | US-03, US-09, US-11, US-12 |
| FR-05 | US-03 |
| FR-06 | US-04, US-09, US-13 |
| FR-07 | US-05, US-10 |
| FR-08 | US-06 |
| FR-09 | US-06 |
| FR-10 | US-01, US-07 |
| FR-11 | US-07 |
| FR-12 | US-08 |
| FR-13 | US-09, US-10 |
| FR-14 | US-11 |
| FR-15 | US-12 |
| FR-16 | US-11, US-13 |
| FR-17 | US-05, US-14 |
| FR-18 | US-15, US-16, US-17 |
| FR-19 | US-16 |
| NFR-01 | cross-cutting NFR-01 obligation above |
| NFR-02 | US-01, US-03, US-04, US-08, US-12, US-13, US-15, US-17; cross-cutting NFR-02 obligation above |
| NFR-03 | cross-cutting NFR-03 obligation above |
| NFR-04 | cross-cutting NFR-04 obligation above |
| NFR-05 | cross-cutting NFR-05 obligation above |
| NFR-06 | US-12; cross-cutting NFR-06 obligation above |

## Persona-to-story mapping

All three traveler personas can use US-01 through US-14. The emphasis below explains their different motivations; it is not an access restriction or a reason to duplicate shared stories.

| Persona / role | Particularly relevant stories | Value emphasized |
| --- | --- | --- |
| P01 Recent Graduate | US-01, US-05, US-07, US-09, US-10 | Valid preferences, understandable activity costs, honest shortfalls, and controlled replacements |
| P02 Abroad Student | US-02, US-03, US-06, US-11, US-13 | Local exploration, confirmed event dates, feasible schedules, and deliberate session changes |
| P03 Cultural Explorer | US-02, US-03, US-04, US-06, US-08, US-09 | Interest clarification, cited local evidence, relevant events, and preserving useful choices |
| R01 Team Evaluator | US-15, US-16, US-17 | Anonymous evaluation, correct final-itinerary metrics, and ratings cleanup |

## Explicit design and verification dependencies

The table distinguishes decisions resolved by actual Application Design answers from remaining detailed design and verification. No integration, benchmark or test is marked complete merely because a design choice has been made.

| ID | Item | Required later outcome | Basis |
| --- | --- | --- | --- |
| DEF-01 | Three cities and ten fixtures | Resolved by AD3: New York City/London/Paris, 4/3/3; run evaluation later | AD3=A |
| DEF-02 | Rate-source access decision (originally WSJ) | AD4 explicitly replaces WSJ with documented ECB data; runtime ingestion/integration still unverified | AD4=A |
| DEF-03 | Currency and missing-budget policy | Resolved at design level by AD5/AD6; detailed arithmetic/date tests later | AD5/AD6=A |
| DEF-04 | High-level interfaces, lifecycle, normalization and bounds | Defined under AD1/AD2/AD6; detailed schemas, algorithms and remaining evidence/link bounds in Functional/NFR Design | AD1/AD2/AD6=A |
| DEF-05 | PBT framework and dependency configuration | Later design/NFR selection: review appropriate framework, then configure in Construction | Q18; PBT-09 |
| DEF-06 | Model quality, laptop suitability, latency/memory targets and fallback hardware | Construction: test actual environment and record evidence; return changed choices to team | R, T |
| DEF-07 | Tavily account access/limits, dependency versions and licenses | Design/Construction before integration: verify availability/cost and pin tested dependencies; no purchase assumed | T |

US-07 now reflects AD4–AD6: planned ECB data, pinned/fresh rates and pause on unavailable budget conversion. US-15 reflects AD3's cities/fixtures. No rate values, working integration, PBT framework, fallback laptop availability or measured performance target is claimed.

## INVEST and coverage review

The following is a document review, not a claim of passing product tests.

- [x] Independent: each story names an observable user outcome; necessary shared context and dependencies are explicit.
- [x] Negotiable: implementation remains for design, while approved rules and limits are retained.
- [x] Valuable: each narrative states a benefit to a traveler or the existing evaluation role.
- [x] Estimable: sources, scenarios, and dependencies support later sizing; unresolved technical choices are identified rather than guessed.
- [x] Small: feedback, replacement, no-replacement handling, new-trip confirmation, evaluation calculation, and cleanup are separate outcomes.
- [x] Testable: every story has Given / When / Then criteria, with relevant limits, boundaries, uncertainty and failure behavior.
- [x] Coverage: all FR/NFR IDs are mapped; persona references and all DEF items are included.
- [x] Scope: no couples, accounts, bookings, route optimization, social scraping, mobile-specific testing, new dashboard, or extra evaluation data introduced.

## Extension compliance at User Stories generation

Security Baseline is N/A because C5=B disabled it; Resiliency Baseline is N/A because Q17=B disabled it. Project-specific security/privacy and failure rules remain in story criteria and NFR-02/NFR-06. Partial PBT is retained through NFR-05 and DEF-05.

| PBT rule | Stage status | Rationale |
| --- | --- | --- |
| PBT-01 | N/A | Advisory in partial mode; functional property design is later |
| PBT-02 | N/A | No serialization code/tests generated; round-trip obligation retained |
| PBT-03 | N/A | No pure-function implementation/tests generated; invariant obligation retained |
| PBT-04 | N/A | Advisory in partial mode; no idempotency implementation |
| PBT-05 | N/A | Advisory in partial mode; no oracle implementation |
| PBT-06 | N/A | Advisory in partial mode; no mandatory stateful-PBT expansion |
| PBT-07 | N/A | No test generators created; domain-generator obligation retained |
| PBT-08 | N/A | No test execution/CI setup; shrinking, seeds and CI obligation retained |
| PBT-09 | N/A | Framework choice is explicitly deferred to later NFR/design work |
| PBT-10 | N/A | Advisory in partial mode; example-based acceptance coverage retained |

No applicable extension finding blocks this document review. No test, model, source-service, or security verification has been performed in this stage.

## Approval boundary

The team approved stories.md and personas.md with the accompanying review package; approval recorded 2026-11-25T01:09:54Z. User Stories is complete and Workflow Planning may begin. Subsequent stage approvals remain separate. Stop after Units Generation approval, before Construction.
