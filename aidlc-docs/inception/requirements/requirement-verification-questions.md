# Requirements Verification Questions

Status: All answers received and validated. Requirements approved by the team; recorded 2026-11-24T21:03:33Z. Original questions and answers remain unchanged as historical evidence; requirements.md applies later clarifications.

Please discuss the questions together and fill every `[Answer]:` with a letter and any requested details. If none fits, use X and describe your decision. Tell the assistant when finished so the exact answers can be appended to the audit log with the time they are read; do not edit audit.md yourself. Alternatively, send numbered answers in chat and the assistant will transcribe them verbatim into this file and the audit log. This question set is not a requirements approval request.

## Decisions already carried forward

These are approved inputs, not new questions: the planned Qwen3 4B/Ollama integration and Qwen3 8B fallback; local Python/FastAPI/Jinja2 application; one traveler and one city for at most five days; two to four activities as a target with honest partial results; total activity-ticket/fee budget with no currency conversion; destination-local scheduling, 30-minute buffers and 9 AM–10 PM bounds; separate cached baseline search; source provenance by session; preset-only ratings and anonymous evaluation records; locked thumbs-up activities and explicit thumbs-down updates; no accounts, booking, route optimization, calendar export, social-media scraping, or multi-city/group trips.

The traveler budget is not the team's project spending. Search limits are request counts, not a monetary budget. Model suitability, service access/limits, dependency versions, and numerical performance targets still need Construction verification; no successful tests or purchases are assumed.

## How to read the choices

Questions 1–15 address remaining product/evaluation/team details. Questions 16–18 are the installed rules' extension opt-in prompts. Choices below are proposals for discussion, not team decisions. Any choice that changes an existing guarantee will be reconciled explicitly before requirements approval.

Skipping an optional extension does not remove the security, privacy, testing, or error-handling requirements already approved in tech-env.md. Property-based testing means testing automatically generated input combinations against rules that should always hold; the partial option limits its scope.

## Question 1: Supported destinations and language

The approved MVP is single-city and single-traveler, and evaluation uses 10 sample profiles across 3 destinations. The destinations and language coverage are not named.

Which coverage should the MVP promise? Include the names of the three evaluation destinations after your choice.

A) An English-language interface supporting only the three named destinations for this MVP.

B) An English-language interface accepting any single destination, with evaluation and demonstrated quality limited to the three named destinations.

X) Other (please describe after [Answer]: tag below)

[Answer]: X, An English-language interface accepting any single destination, with evaluation and demonstrated quality limited to the ten named destinations.

## Question 2: Preference intake and clarification length

Destination, dates, total activity budget/currency, and interests are required. Vague interests need follow-up, but the conversation length is open.

How should the chatbot decide when to stop clarifying and start generation?

A) Collect the required fields, allow at most three additional interest-clarification turns, then show a preference summary for confirmation. If required fields are still invalid or missing, request correction rather than generate.

B) Continue clarifying until the traveler explicitly confirms a preference summary, without a fixed clarification-turn cap; still require valid required fields.

X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 3: Past travel dates

The maximum remains five inclusive calendar days, and reversed dates are invalid. The inputs do not say whether historical travel dates can be entered.

Which date policy should apply to the product?

A) Accept only trips starting today or later in the destination local time zone. Historical dates may still appear in deterministic unit tests, not live itinerary generation.

B) Also allow historical trips for retrospective exploration, visibly labeled as historical and without implying current event availability.

X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 4: Prices in a different currency

The traveler chooses one currency (default USD), there is no conversion, and unknown prices are flagged and excluded from the budget calculation. A source may quote only a different currency.

How should an otherwise suitable activity with a price only in another currency be handled?

A) Allow it, label the cost in the chosen currency as unverified, flag the mismatch, and exclude it from the calculated total without claiming the whole itinerary fits the budget.

B) Omit activities with prices quoted only in a different currency. Continue allowing genuinely unknown prices under the already-approved unverified-price rule.

X) Other (please describe after [Answer]: tag below)

[Answer]: X, do a currency conversion to USD while noting that the conversion happened. Keep unknown prices flagged from budget calculation

## Question 5: Duration estimates

Each activity needs a duration; a duration not supplied by its source must be labeled as an estimate. The estimation rule is unspecified.

What should determine a missing duration?

A) Use a fixed 60-minute estimate for every activity whose source provides no duration.

B) Let the model estimate by activity type, constrained to 30–180 minutes; omit the activity if a plausible estimate cannot fit that range. Source-provided durations are not subject to this estimate range.

X) Other (please describe after [Answer]: tag below)

[Answer]: X, Let the model estimate by activity type, based on similar activities. Let the user know an estimate was made. Source-provided durations are not subject to this estimate range.

## Question 6: Unconfirmed event dates

Unknown opening hours are already allowed with an unverified label. A separate issue is a pop-up, class, or festival whose source does not establish that it occurs during the requested trip.

Should such time-limited events be scheduled?

A) No. Omit an event unless a retrieved source establishes an occurrence during the trip; show fewer results if necessary.

B) Yes, as explicitly tentative activities with availability labeled unverified and a direction to confirm with the organizer. Never override a source that shows an incompatible date.

X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 7: Attractions mentioned inside baseline results

The baseline is the up-to-10 results of the separate Tavily system search. A result can be a roundup article naming multiple attractions rather than a single attraction page. Name/URL comparison alone needs a defined source of attraction names.

What evidence from those baseline results may be used to identify attractions for overlap checks?

A) Use only the returned titles, URLs, and search snippets. Match names evidenced in those fields, and document that attractions not mentioned there may be missed.

B) Also use page content returned by the search provider, when available, to extract attraction names and their supporting evidence. Do not add browser scraping or let the model invent missing names.

X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 8: Unavailable baseline

The baseline search runs once for a new generation and revisions reuse its session cache. A failed or empty baseline cannot establish that an activity is absent from popular results.

What should a new generation do if it has no usable baseline results?

A) Stop generation with a clear explanation and a retry action. Do not claim local-discovery compliance or treat an empty baseline as proof that every activity is local.

B) Offer an explicitly unverified draft, flagging that the locality/overlap requirements could not be assessed. This would be an exception to the current locality guarantee and would need to be reflected in the requirements.

X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 9: Activity searches during revisions

Initial activity searches are limited to two per trip day, capped at ten, with five results each. Baseline caching is settled; whether an Update itinerary request receives a fresh activity-search allowance is not.

How should the activity-search allowance apply to a revision?

A) Each explicit update request gets its own allowance of up to two activity searches per trip day, capped at ten, while reusing the cached baseline and existing candidates when sufficient.

B) The initial generation and all its revisions share one allowance of up to two activity searches per trip day, capped at ten in total; once exhausted, revisions use existing candidates only.

X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 10: No suitable replacement

A thumbs-up locks an activity, unaffected activities/preferences must stay unchanged, and only thumbs-down activities may be replaced. A requested replacement may have no distinct candidate that fits the remaining time and budget.

What should happen to that thumbs-down activity when no valid replacement exists?

A) Keep the old activity visibly marked as disliked, explain that no replacement was found, and suggest broadening interests for a new itinerary; do not silently change preferences or other activities.

B) Remove the disliked activity, leave that time empty, and explain that fewer activities were found; keep every unaffected/locked activity and all preferences unchanged.

X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 11: Changing trip preferences after generation

The agreed revision behavior preserves all preferences and unaffected activities. Changing dates, destination, or budget is therefore different from replacing disliked activities.

How should a request to change trip preferences be handled?

A) Provide a New trip action that clears the old itinerary/session after confirmation and restarts intake. Chat requests to change preferences direct the user to that action.

B) Allow chat to propose starting a new trip with changed preferences, but require explicit confirmation before discarding the old itinerary and starting a fresh session and baseline.

X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 12: Presentation and supported browser experience

The inputs call for a local browser interface with chat, day-by-day activities, source links, ratings, and Update itinerary. Presentation and minimum accessibility/browser coverage remain open.

Which interface scope should be required for the MVP?

A) Desktop browser first: chat alongside day-grouped activity cards in Chrome and Safari, keyboard-operable controls, visible focus, readable contrast, text labels for ratings, and understandable progress/error messages. Mobile-specific layout testing is out of scope.

B) The same day-grouped cards, chat, and accessibility basics, with responsive desktop and phone layouts tested in Chrome and Safari. This adds mobile layout and testing work.

X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 13: Model and activity-search failure behavior

The approved input requires bounded requests/timeouts, clear errors, and no invented results. Numerical latency/memory targets remain deferred until Construction measurements, as already agreed. Baseline failure is covered separately in Question 8.

How should an ordinary model or activity-search timeout/service error be handled?

A) Stop the current attempt, show the affected service and a retry action, and preserve the last valid itinerary and user inputs. No automatic retry.

B) Retry once automatically within the existing request/search limits, showing progress; if it still fails, show a retry action and preserve the last valid itinerary and user inputs.

X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 14: KPI evaluation snapshot

Keep the approved targets and denominators: approval >=70% of rated activities; revision rate <30% of test itineraries needing more than two revisions; local-discovery >=70% and source coverage 100% of all recommended activities. Use ten profiles across three destinations, not live users. Multiple revisions can otherwise cause the same activity to be counted repeatedly.

Which snapshot should be used for activity-based KPIs in each round?

A) Use only the final itinerary per profile; retain the full revision count for that test itinerary. Count each final activity once and use its latest rating. Report generation failures separately; an empty denominator is N/A, never 100%.

B) Report initial and final itineraries separately, with no pooling across snapshots. Count each activity once per snapshot and retain full revision counts per test itinerary. Report failures separately and empty denominators as N/A.

X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 15: Shared-session and demonstration ownership

The assignment expects one shared workflow and identifies a team member to operate it. The README lists six members but does not assign that role. Model testing and service-account checks remain future work, not completed facts.

How will the team coordinate the remaining shared Inception sessions? Include the operator name(s), plus the planned demo-laptop owner if known.

A) One named operator runs the agent and maintains the shared repository while the whole team discusses answers and approvals.

B) Named operators rotate between shared sessions, with one active operator at a time and an explicit handoff using the current state and audit records.

X) Other (please describe after [Answer]: tag below)

[Answer]: X, Sophia is the designated operator, and the other group members join sessions over calls to make decisions.

## Question 16: Security Baseline
Should security extension rules be enforced for this project?

A) Yes — enforce all SECURITY rules as blocking constraints (recommended for production-grade applications)

B) No — skip all SECURITY rules (suitable for PoCs, prototypes, and experimental projects)

X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 17: Resiliency Baseline
Should the resiliency baseline be applied to this project?

**What this extension is.** Enabling it applies a set of **directional, design-time best practices** for building resilient systems, derived from the **AWS Well-Architected Framework (Reliability Pillar)** and resilience-review guidance. It steers requirements, design, and code toward fault tolerance, high availability, observability, and recoverability — covering 15 practice areas across business goals, change management, observability, high availability, disaster recovery, and continuous improvement.

**What this extension is NOT.** Enabling it does **not** make your workload production-ready, nor does it certify or guarantee any availability, RTO, or RPO target. It is a **starting point** that scaffolds good resiliency decisions early — it is not a substitute for a formal **AWS Well-Architected Review** of the built system.

Treat the output as a well-grounded **first draft of your resiliency posture** to build on and validate — not a finished, production-certified result.

A) Yes — apply the resiliency baseline as directional best practices and design-time guidance (recommended for business-critical workloads, as an informed starting point that you can validate and harden before go-live)

B) No — skip the resiliency baseline (suitable for PoCs, prototypes, and experimental projects where rapid iteration matters more than reliability)

X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 18: Property-Based Testing
Should property-based testing (PBT) rules be enforced for this project?

A) Yes — enforce all PBT rules as blocking constraints (recommended for projects with business logic, data transformations, serialization, or stateful components)

B) Partial — enforce PBT rules only for pure functions and serialization round-trips (suitable for projects with limited algorithmic complexity)

C) No — skip all PBT rules (suitable for simple CRUD applications, UI-only projects, or thin integration layers with no significant business logic)

X) Other (please describe after [Answer]: tag below)

[Answer]: B
