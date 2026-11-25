# Component Methods and Interface Contracts

Status: Application Design artifacts approved by the team with "approve & continue", recorded 2026-11-25T02:02:35Z. Units Generation may begin. No implementation, integration, performance or test success is claimed.

These are proposed high-level interfaces generated under the approved plan. They are design notation, not implemented Python classes/routes. Detailed schemas, algorithms and tests belong to Construction Functional Design. Public fields/functions use snake_case, dates use ISO format, and money uses decimal values.

## Shared types and data ownership

| Type | Important content / invariant |
| --- | --- |
| CommandMeta | session_id, request_id, expected_version; applies after bootstrap; identifiers are opaque random values |
| PreferenceDraft | Incomplete intake fields and clarification count; never sufficient authorization to generate |
| ConfirmedPreferences | One destination/country/time zone, start/end dates, original total budget/currency, interests and confirmation version; immutable within the trip |
| EvidenceBatch / SourceRecord | Provider results with rank, title, URL and available text; server assigns source_id and session ownership on registration |
| Baseline | Successful separate query, up to ten ranked result records and evidence-backed attraction names/URLs/aliases; cached for the trip |
| EvidenceRef | Session-owned source_id plus supporting excerpt and claimed field/local criterion; source URL resolved by server |
| RateSnapshot | Source URL/date, EUR quotation basis, positive finite currency rates and normalized USD rates; pinned to the session; no model-supplied rates |
| CandidateActivity | Evidence-backed identity/name/location, interests explanation, event occurrence evidence if needed, duration with source/estimate label, known/unverified price/hours, locality evidence references |
| ScheduledActivity / Itinerary | Activity identity, destination-local date/start/end, duration, source references, uncertainty labels and price data; at most four distinct activities/day |
| RatingCommand | Current activity ID, thumbs_up or thumbs_down, optional allowed preset reason; no free-text feedback |
| ValidationContext | Immutable confirmed preferences, session source map, baseline, rates and prior accepted itinerary/ratings; pure validators receive this instead of accessing live state |
| ValidationReport | Structured constraint/evidence errors and warnings; a failed final validation cannot authorize a commit |
| ValidatedSnapshot | Accepted final itinerary with validation receipt, latest ratings, revision count and random itinerary ID; evaluation needs its resolved public links but no raw chat or full source text |
| SessionSnapshot / TripView | Internal canonical snapshot versus sanitized browser view; TripView omits secrets, raw source caches, internal traces and unrelated-session data |
| OperationResult | Current version, result category, safe message, optional TripView, warnings/shortfall counts and allowed retry/correction action |
| EvaluationRecord | Exactly itinerary_id, activity_count, revision_request_count, baseline_overlap_count, link_check_results and activity_ratings |
| RoundReport | Derived metrics and separate failure/round-completeness counts; no new persisted traveler/profile mapping |

The activity_ratings array is ordered with the final activities and contains a nullable vote plus optional preset reason; link_check_results follows the same ordering and contains load outcomes without source URLs. These nested values remain within the approved field groups. The file serializer receives only the allowlisted EvaluationRecord projection, not the full snapshot used for link checks. Ratings allow only too touristy, too expensive, wrong time, or not my interest. Replaced activities are excluded from the final arrays.

## Public interface inventory

| Endpoint | Request | Response / effect |
| --- | --- | --- |
| GET / | None | Local desktop page; application assets remain same-origin |
| POST /api/v1/sessions | Bootstrap request; no pre-existing session ID | New random session ID, initial version and empty TripView |
| POST /api/v1/chat | CommandMeta and message | Clarification, proposed preference summary, or result of an explicitly requested update; conversational text alone cannot silently change confirmed preferences |
| POST /api/v1/confirm-preferences | CommandMeta and displayed summary version | Confirms a valid unmodified summary; otherwise requests correction |
| POST /api/v1/generate | CommandMeta | Open request returns validated initial itinerary, honest partial/empty outcome, or safe failure; confirmed preferences required |
| POST /api/v1/feedback | CommandMeta and RatingCommand | Updated canonical rating/lock and version; no replacement call |
| POST /api/v1/update-itinerary | CommandMeta | Targeted replacement of disliked activities; no-op/no-replacement result when appropriate |
| POST /api/v1/confirm-new-trip | CommandMeta and pending new-trip proposal version | Invalidates old session and returns a fresh intake session only after explicit confirmation |
| POST /api/v1/evaluation/complete | CommandMeta for the final accepted snapshot | Team-triggered link checks, anonymous final record and metric contribution; no new account/dashboard |

The browser disables duplicate mutations while awaiting a response and shows readable waiting/retry/error text. No polling job/status endpoint is introduced. Chat may identify an update request, but C03 routes it to the same revision method/guards used by the button. A tentative new-trip suggestion does not reset anything.

Malformed or out-of-bounds inputs return HTTP 422; unknown/expired session references return a safe expired-session response, proposed HTTP 410; conflicting versions/in-flight mutations return 409. Provider failures/timeouts are distinguished from schema errors, proposed 502/504, with safe categories and existing view preserved. A missing budget conversion returns a typed blocked/correction outcome, never a successful budget-compliant itinerary. Exact error schemas are a Functional Design task; these meanings are fixed for this review.

## Method inventory

| Component | Signature / contract | Purpose and important outcomes |
| --- | --- | --- |
| C01 | render_view(view: TripView) -> HTML | Accessible escaped chat/cards; visible uncertainty, count, focus and rating labels |
| C01 | dispatch(command: TypedCommand) -> OperationResult | Validate public envelope and map the coordinator result to HTTP/UI; never accept browser state as authority |
| C02 | validate_preferences(draft: PreferenceDraft, destination_today: date) -> PreferenceValidation | Required-field corrections or typed valid preferences; 1–5 inclusive days and future/live start rule |
| C02 | confirm_preferences(draft: PreferenceDraft, summary_version: int) -> ConfirmedPreferences | Accept only the actual valid summary the traveler confirmed |
| C03 | start_session() -> SessionSnapshot | Bootstrap C08 state and return the random identifier and initial version; no prior session required |
| C03 | handle_chat(meta: CommandMeta, message: str) -> OperationResult | Bounded intake/clarification or an explicit action routed through its own guards |
| C03 | generate(meta: CommandMeta) -> OperationResult | Coordinate a new generation with existing confirmed preferences, caches, quotas and validation |
| C03 | rate(meta: CommandMeta, rating: RatingCommand) -> OperationResult | Change latest rating/lock only; unchanged activity content |
| C03 | revise(meta: CommandMeta) -> OperationResult | Replace thumbs-down targets only; preserve fixed context; retain unmatched disliked activities |
| C03 | confirm_new_trip(meta: CommandMeta, proposal_version: int) -> SessionSnapshot | Reset only the confirmed proposal; return a fresh session for valid intake |
| C03 | complete_evaluation(meta: CommandMeta) -> EvaluationResult | Guard the final snapshot and coordinate C09 exactly once for the requested completion |
| C04 | interpret_intake(context: IntakeContext) -> IntakeProposal | Extract/clarify without inventing required fields or exceeding optional interest turns |
| C04 | propose_queries(preferences: ConfirmedPreferences, allowance: int) -> QueryProposal | Return permitted search-query proposals; Python chooses count and execution |
| C04 | interpret_evidence(batch: EvidenceBatch, context: ModelContext) -> EvidenceProposal | Identify evidenced baseline entities/candidates; retain source references and uncertainty |
| C04 | propose_itinerary(context: DraftContext) -> ItineraryProposal | Draft sourced schedule or replacements; no direct mutation, URL authority, or tool execution |
| C05 | search_baseline(query: str, permit: SearchPermit) -> EvidenceBatch | Separate system query, max ten results, no hidden retries/crawl |
| C05 | search_activities(query: str, permit: SearchPermit) -> EvidenceBatch | Max five results; every dispatched attempt consumes a reserved activity-search slot |
| C06 | acquire_rates(deadline: Deadline) -> RateAvailability | Fetch the official documented ECB daily data; bounded retrieval/parse, source date/direction validation, typed missing/stale/error result |
| C06 | convert_to_usd(money: Money, snapshot: RateSnapshot) -> ConversionResult | Pure conversion preserving originals; USD identity; unsupported amounts remain explicitly unavailable |
| C06 | summarize_costs(items: ActivityPrices, budget: Money, snapshot: RateSnapshot) -> CostSummary | Unrounded comparisons, rounded display, verified subtotal and missing-price flags; missing budget blocks work |
| C07 | validate_initial(proposal: ItineraryProposal, context: ValidationContext) -> ValidationReport | Grounding, locality, distinctness, schedule, prices/budget and item limits |
| C07 | validate_revision(proposal: ItineraryProposal, context: ValidationContext) -> ValidationReport | All initial constraints plus unchanged preferences/locked/neutral activities |
| C07 | compare_baseline(identity: ActivityIdentity, baseline: Baseline) -> MatchResult | Python name/URL matching yields match, clear non-match or ambiguous; ambiguous cannot claim local status |
| C08 | create_session() -> SessionSnapshot | Allocate isolated empty in-memory state and a random session ID |
| C08 | begin_operation(meta: CommandMeta) -> OperationLease | Validate session/version; replay completed request or reserve one mutation; reject reused request ID with different payload |
| C08 | reserve_search(lease: OperationLease, kind: SearchKind) -> SearchPermit | Reserve baseline attempt or increment cumulative activity allowance before external dispatch |
| C08 | register_sources(lease: OperationLease, batch: EvidenceBatch) -> SourceRegistryView | Assign server IDs/ownership and retain evidence for this session |
| C08 | commit_result(lease: OperationLease, result: ValidatedResult) -> SessionSnapshot | Atomically replace only approved state fields and increment version; release lease and record request receipt |
| C08 | finish_failure(lease: OperationLease, error: SafeError) -> SessionSnapshot | Preserve accepted itinerary/preferences; keep consumed calls/caches, update receipt/version as appropriate and release lease |
| C08 | reset_or_expire(session_id: str, reason: ResetReason) -> None | Clear canonical state/evidence on confirmed reset, restart or idle expiry |
| C09 | check_links(final: ValidatedSnapshot, policy: LinkCheckPolicy) -> LinkCheckResults | Bounded public HTTP/HTTPS checks; failed/blocked/unsafe links do not count as loaded |
| C09 | create_record(final: ValidatedSnapshot, checks: LinkCheckResults) -> EvaluationRecord | Pure projection to the six allowed field groups using latest final-activity ratings |
| C09 | write_final_record(record: EvaluationRecord) -> RecordReceipt | Explicit completion upserts one final record per itinerary ID; no pooled obsolete snapshot or raw profile write |
| C09 | calculate_kpis(records: EvaluationRecords, failures: FailureSummary) -> RoundReport | Agreed denominators, N/A for empty denominators, failures and incomplete rounds visible |
| C09 | delete_ratings_after_demo(path: RatingsPath) -> CleanupResult | Future team-invoked deletion of the local ratings file; not executed in Inception |

Auxiliary types such as Deadline, SearchPermit, OperationLease and MatchResult are internal contract names. Their detailed representations and race/error algorithms are deferred to Functional Design. A permit cannot be supplied by the model/browser. Core validators and currency arithmetic must stay testable independently of provider clients and storage.
