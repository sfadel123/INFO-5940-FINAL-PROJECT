# Application Services and Orchestration

Status: Application Design artifacts approved by the team with "approve & continue", recorded 2026-11-25T02:02:35Z. Units Generation may begin. No implementation, integration, performance or test success is claimed.

## Service boundary

C03 supplies application services through ordinary internal function calls inside the one local FastAPI application. Provider adapters are replaceable boundaries for tests; no separate microservice, message broker, background job API or orchestration framework is introduced. C01 keeps the HTTP request open and shows a waiting indicator under AD2=A.

See [components](components.md), [method contracts](component-methods.md), and [dependencies](component-dependency.md). The consolidated [design](application-design.md) records numerical bounds, currency rules, fixtures and requirement traceability.

## S01 — Intake and confirmation

1. Bootstrap a random session. C08 owns the draft and version; the browser keeps a display copy.
2. C03 asks C04 to interpret the bounded chat input. C02 validates required fields and destination-local dates; incomplete/invalid data produces correction requests, not invented preferences.
3. Once required fields are present, ask at most three additional interest-clarification turns. Required corrections remain necessary even after that cap.
4. Show destination/country/time zone, dates, original budget/currency and interests as a valid summary. Accept explicit confirmation of that version before generation.
5. Ambiguous place/time-zone proposals require correction. Membership in the IANA time-zone catalog validates an identifier, not the correctness of a city-to-zone mapping; the summary makes that mapping visible and fixture mappings are explicitly documented.

## S02 — Initial generation

1. Acquire a C08 operation lease and confirmed preference snapshot. Check request replay/version and remaining deadline/call bounds. Unconfirmed or malformed requests never invoke discovery.
2. Prepare the trip's rate snapshot. USD has an identity conversion. A missing required budget conversion blocks the operation under AD5=A, preserving inputs and any prior accepted result; provide retry or confirmed correction. Do not consume activity searches merely to work around a missing budget conversion.
3. Obtain the separate baseline only if this trip lacks a successful usable baseline. Query `top things to do in [destination]` with up to ten results; register sources and evidence-backed baseline entries. Empty/unusable baseline stops this attempt, with a user retry action. No automatic baseline retry loop.
4. C04 proposes relevant activity queries. C03 validates query purpose and reserves C08 activity-search slots before each dispatch through C05. Reuse available candidates when adequate. Each activity request has at most five results; attempts, including a permitted retry, count toward the cumulative trip allowance.
5. Register returned evidence under server-created source IDs. C04 interprets bounded evidence and proposes candidates and a schedule. Provider/model material cannot grant tool permissions or alter confirmed preferences.
6. C07 verifies all final constraints against the canonical ValidationContext. Unsuitable candidates may be omitted before final validation; an invalid submitted itinerary/source reference cannot be accepted. Return fewer or zero activities with the actual count and interest-broadening suggestion rather than fabricate fillers.
7. Commit only the validated itinerary and its derived labels/totals. Preserve unverified-price/hour warnings and duration-estimate labels. Return a sanitized view and new state version; keep successful caches and consumed quota even if a later step fails.

One successful rate acquisition and one successful baseline belong to the trip, not to each activity or chat message. A failed acquisition may be retried through the explicit retry flow; a successful cache is not discarded merely because a subsequent model step fails.

## S03 — Feedback and targeted revision

Feedback validates the current activity ID and preset reason, then updates its latest vote. Thumbs up locks; thumbs down marks without replacement. Choosing a new explicit vote updates that activity's latest rating; a revision can target only activities currently marked thumbs down. A neutral activity is unaffected.

An explicit Update itinerary action or unambiguous chat update request uses the same revision service:

1. Acquire the operation lease and immutable snapshot. If there are no disliked activities, return a no-change message without search/model work; the revision request count records a valid explicit update request once, not each network replay or automatic retry.
2. Reuse the pinned rates and cached baseline. Check rate freshness and required budget availability before changing anything. Do not silently refresh prices for unaffected activities. A stale snapshot blocks the update and directs the user to retry if the condition can resolve, or explicitly confirm a new trip for new rates/preferences.
3. Freeze confirmed preferences and every locked/neutral activity, including scheduled fields and cost labels. Provide disliked targets and the fixed context to the model.
4. Prefer cached candidates. Additional activity searches require remaining cumulative allowance; exhaustion means use existing evidence only. Do not rerun the baseline or reset quota.
5. Validate replacements for distinctness, sources/locality, remaining schedule slots and total comparable budget. C07 also compares the submitted fixed portion with the original snapshot; changed fixed fields fail validation.
6. Commit valid replacements together. If no replacement fits a target, retain that original activity visibly disliked and explain the shortfall. If the operation itself fails, preserve the entire last accepted itinerary and inputs. Suggest broader interests only through a new trip, not a hidden preference edit.

## S04 — Confirmed new trip

Chat may stage a changed preference proposal but cannot mutate the active trip. Display the proposed change and require explicit confirmation before discarding the old session. After confirmation, C08 clears the old session and creates a fresh intake session with its own random identifier, source registry, baseline, rate snapshot and activity quota. Validate and confirm the new preference summary before generating. Decline/no confirmation preserves all old state.

## S05 — Failure, concurrency and session lifecycle

| Condition | Required service behavior |
| --- | --- |
| Ordinary model/activity-search timeout or service error | One automatic retry at most, subject to the same remaining call/time/search limits; then safe retry action |
| Invalid/truncated model structure or unowned source ID | Reject the proposal; no unbounded repair loop or invented source |
| Failed/empty baseline | Stop initial generation and offer explicit retry; no false local classification |
| Missing/stale required budget rate | Block generation/revision under AD5=A; no silent source/currency substitution |
| Unknown activity price/conversion | Flag unverified, exclude from verified subtotal, retain honest uncertainty; never treat as verified zero |
| Duplicate request ID with identical payload | Return the retained receipt/result; do not repeat work, write a second record, or increment counts |
| Same request ID with different payload / stale version | Conflict response; do not apply ambiguous mutations |
| Another mutation in progress | Reject conflict safely; one mutation per session; UI prevents repeat clicks |
| Expired/restart-stale session or source ID | Reject and explain a fresh flow is required; browser data cannot restore authority |
| Operation exception or deadline expiry | Release the mutation guard; keep accepted state, consumed counters and successful caches |

C08 expires an inactive session after two hours, excluding an active operation, and clears all memory on server restart. Browser reload starts a fresh flow; no persistent browser storage or automatic recovery is promised. Cleanup releases evidence, cached rates, receipts and trip data together. Service responses/logs contain safe categories and request IDs rather than credentials or raw profiles.

## S06 — Team evaluation and cleanup

Use the ten approved synthetic profiles across New York City, London and Paris. Each evaluation completion captures the final accepted itinerary and latest votes after actual team-requested revisions, not intermediate/replaced activities. Explicit completion invokes bounded link checks and projects the six allowed field groups into ratings.jsonl. There is no live-user telemetry, account or evaluator dashboard.

Use one final record per random itinerary ID. If the team explicitly completes evaluation again after a later permitted revision/rating, replace that itinerary's prior final record rather than pooling old and new activity snapshots. Replayed completion requests do not duplicate work. No profile/destination mapping is persisted.

Calculate approval from rated final activities, revision rate from evaluated test itineraries, and locality/source coverage from all final recommended activities. A validated non-baseline activity has locality evidence, allowing local count to be derived from total activities minus baseline overlaps. Show failures separately and N/A for empty denominators. Report attempted profiles and final-itinerary count so a round with fewer than ten evaluated itineraries is visibly incomplete; failed generation is not fabricated into a successful zero-activity itinerary. A valid empty itinerary after a usable baseline is a distinct outcome. If all ten profiles fail to generate, report an incomplete round and N/A metrics, not a zero revision rate or successful evaluation.

This denominator interpretation and the concrete record-writing contract are design details presented for review, not additional claimed team answers. Detailed failure-report serialization and file-update mechanics belong to Functional Design; no extra persistent profile fields are authorized.

The ratings file is already locally ignored by Git, is never committed, and is deleted by the team after the final demo. These are future controls; this stage creates no ratings file and performs no deletion.

## Extension and verification boundary

Disabled Security/Resiliency extensions remain skipped; project-specific privacy, bounded calls and safe errors still apply. Later tests must cover the documented guards, pure invariants and serialization under partial PBT. Provider access, model behavior, browser flows, freshness/rounding edge cases and file operations require Construction evidence; none is reported as passing here.
