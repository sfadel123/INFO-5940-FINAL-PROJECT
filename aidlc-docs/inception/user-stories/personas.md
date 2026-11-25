# Traveler Personas and Team Evaluation Role

Status: Approved by the team; approval recorded 2026-11-25T01:09:54Z in audit.md. Three traveler personas plus one separate project role, following S1 as refined by SC1.

## Basis and limits

These are illustrative planning archetypes grounded in the vision and the team's actual persona choices, not results of user interviews. No names, ages, incomes, relationship details, evaluation-city selections, or real-user claims are invented. The target audience remains travelers interested in local cultural experiences; age is not an eligibility rule.

SC1 removes the proposed Fiancees persona. The final traveler set is Recent Graduate, Abroad Student, and Cultural Explorer. The Team Evaluator is an existing project responsibility, not a traveler persona, account type, or new administrator interface. The former hobby and pop-up motivations remain within the supported cultural-discovery use cases.

Sources: [vision](../../../vision.md), [approved requirements](../requirements/requirements.md), [story plan and S1–S3](../plans/story-generation-plan.md), and [SC1 clarification](../plans/story-planning-clarification-questions.md).

## P01 — Recent Graduate

**Source audience:** Recent Graduates in the vision, retained in S1/SC1.

**Goal:** Find cultural activities that fit personal interests and a limited total activity budget without spending excessive time researching generic tourist lists.

**Current difficulties:** Recommendation lists can favor well-promoted attractions. An apparent low-cost itinerary can hide unknown ticket prices, currency mismatches, or additional expenses that the activity budget does not cover.

**Relevant needs:** Enter a budget in a chosen currency, see the original budget alongside USD comparisons, understand unverified prices, review source links, and replace disliked activities without losing satisfactory choices. Keep the distinction between an activity subtotal and the cost of the whole vacation visible.

**Illustrative scenario:** The traveler describes interests and a short trip, reviews the proposed day cards and verified activity subtotal, then marks one expensive-looking option as disliked and explicitly requests an update. This is a planning scenario, not a selected evaluation fixture or evidence that the product works.

**Constraints:** One traveler, one city, one to five inclusive days. The budget covers activity tickets/fees only. Unknown costs are not free; incomplete prices or conversions cannot prove full budget compliance.

**Success signals for later review:** The itinerary reflects stated interests, exposes cost uncertainty, respects the comparable budget, and preserves accepted activities and preferences during a targeted revision.

## P02 — Abroad Student

**Source audience:** Abroad Students in the vision, retained in S1/SC1.

**Goal:** Explore a new city through interest-matched local activities, including drop-in experiences that may offer opportunities to meet locals.

**Current difficulties:** Familiar tourist lists provide little help finding less-promoted experiences. A class or meetup can appear relevant but have no confirmed occurrence during the requested dates; a crowded schedule can make otherwise useful suggestions impractical.

**Relevant needs:** Clarify interests in conversation, receive evidenced local recommendations, distinguish confirmed event dates from unknown opening hours, and see destination-local schedules with duration estimates and buffers. Meeting people is a motivation, not a guaranteed outcome or a social-network feature.

**Illustrative scenario:** The student plans a short outing or one-to-five-day set of activities in the city, looks for a drop-in cultural activity, and checks the source and schedule before deciding whether it fits. Living abroad does not expand the product's five-day planning window.

**Constraints:** Future/live travel-date rules, one traveler's budget and preferences, and the same source, schedule, and search limits as every other traveler. No saved account or persistent student profile.

**Success signals for later review:** Recommendations go beyond the baseline tourist list, evidence supports event dates, and the traveler can distinguish feasible plans from unverified details without assumed availability.

## P03 — Cultural Explorer

**Source audience:** The team's custom S1 label, retained by SC1; grounded in the vision's local-culture, hobby, and pop-up discovery goals.

**Goal:** Discover experiences that connect personal interests with the destination's local culture, including hands-on activities and time-limited events when supported by evidence.

**Current difficulties:** Broad interests can lead to generic recommendations. An activity being absent from a popular list does not by itself show that it is local or suitable, and a claimed pop-up may not occur during the trip.

**Relevant needs:** Explain interests in natural language, receive a concise reason for each match, inspect cited evidence of local relevance, and give preset feedback such as too touristy or not my interest. Prefer an honest short list to invented or repeated recommendations.

**Illustrative scenario:** The traveler clarifies an interest such as pottery or painting, reviews the sources and relevance explanations, marks one mismatch, and requests a replacement while keeping the rest of the plan.

**Constraints:** At most one baseline overlap per itinerary; every other activity needs evidence of an approved local criterion. Time-limited events require a source-supported occurrence during the trip. Search limits and scheduling/budget checks remain unchanged.

**Success signals for later review:** Activities have defensible local evidence, reflect the clarified interest, explain their relevance, and remain distinct and feasible after a revision.

## R01 — Team Evaluator (project role)

**Source:** Existing team-evaluation requirements FR-18/19, retained explicitly in S1. This role is not counted among the three traveler personas.

**Goal:** Evaluate the MVP consistently while retaining only the agreed anonymous records and an honest account of failures and uncertainty.

**Current difficulties:** Revisions can duplicate activity counts, unrated activities can distort approval calculations, and storing raw traveler details can exceed the privacy agreement. A source link loading does not prove the activity information is accurate.

**Relevant needs:** Run the agreed ten profiles across three destinations, use final itineraries and latest ratings for activity metrics, preserve total revision-request counts, check source-link loading, report failures and empty denominators correctly, and remove ratings after the final demo.

**Constraints:** AD3 selects New York City, London and Paris with ten synthetic fixtures distributed 4/3/3, documented in [Application Design](../application-design/application-design.md). No live-user telemetry, new dashboard/account, free-text feedback, stored raw conversations, or expanded ratings fields. Only the existing anonymous field allowlist may be persisted in ratings.jsonl; the file stays out of Git.

**Success signals for later review:** Metrics are reproducible from the permitted records and applicable final in-memory validation context, the agreed denominators are used, failures are visible, and no successful model/service evaluation is claimed without evidence.

## Shared traveler boundaries

All three traveler personas use the same English desktop flow in Chrome and Safari with keyboard access and clear text labels. Preferences are confirmed before generation. A thumbs-down marks only; an explicit update replaces disliked activities, while a thumbs-up locks an activity. Changed preferences require a confirmed new trip. No booking, group planning, route optimization, saved accounts, social-media scraping, or mobile-specific testing is introduced by these personas.

Persona emphasis does not restrict who can use a capability. The Team Evaluator can exercise the same traveler flow through sample profiles without becoming an additional product account.

## Persona-to-story mapping

All three traveler personas can use US-01 through US-14. The emphasis below explains their different motivations; it is not an access restriction or a reason to duplicate shared stories.

| Persona / role | Particularly relevant stories | Value emphasized |
| --- | --- | --- |
| P01 Recent Graduate | US-01, US-05, US-07, US-09, US-10 | Valid preferences, understandable activity costs, honest shortfalls, and controlled replacements |
| P02 Abroad Student | US-02, US-03, US-06, US-11, US-13 | Local exploration, confirmed event dates, feasible schedules, and deliberate session changes |
| P03 Cultural Explorer | US-02, US-03, US-04, US-06, US-08, US-09 | Interest clarification, cited local evidence, relevant events, and preserving useful choices |
| R01 Team Evaluator | US-15, US-16, US-17 | Anonymous evaluation, correct final-itinerary metrics, and ratings cleanup |


See [stories.md](stories.md) for the complete story index, acceptance criteria, requirement traceability, and explicit design dependencies.
