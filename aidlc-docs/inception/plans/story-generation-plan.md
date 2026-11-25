# Story Generation Plan

Status: Complete and approved. The team approved generated stories/personas with its message recorded 2026-11-25T01:09:54Z. G1–G8 are complete; Workflow Planning is next.

Requirements Analysis was approved with `Approved `, recorded 2026-11-24T21:03:33Z. That approval starts this planning stage; it does not approve the choices proposed below.

## How to respond

Discuss S1–S3 together and put a letter after each `[Answer]:` tag. Choose X and describe your preference if the listed options do not fit. Leave the rest of the plan intact. Tell the assistant when all three are answered; numbered answers in chat can also be transcribed verbatim. The assistant will record the actual answers, check for ambiguity, and present the resolved plan for approval before generating stories and personas.

The original options below remain as issued; the actual answers are preserved. S2=A and S3=A are selected. S1 is a custom persona list refined by SC1 to three travelers: Recent Graduate, Abroad Student, and Cultural Explorer; Team Evaluator remains separate. The approved product requirements remain fixed unless an explicit scope change is reviewed. No evaluation-city names, currency-rate access method, or other deferred design decision is requested here.

## Question S1: How many distinct traveler personas?

The vision already names four audiences. A persona is a short description of a user's goals, frustrations, and needs; it is not an account type. Which representation would be most useful for your team?

A) Keep four distinct traveler personas: Recent Graduate, Hobby Explorer, Pop-Up Enthusiast, and Abroad Student. Also document the Team Evaluator as a separate project role for the existing evaluation requirements. This preserves every audience from the vision. (Recommended)

B) Consolidate into two traveler personas: Budget-Conscious Cultural Explorer (recent-graduate and abroad-student motivations) and Interest-Led Experience Seeker (hobby and pop-up motivations). Also document the same Team Evaluator role. This is shorter; retain each original audience's distinct needs within the combined profiles.

X) Other (describe the persona grouping and treatment of team evaluation after [Answer]:)

[Answer]:  Keep four distinct traveler personas: Recent Graduate, Abroad Student, cultural explorer, Fiancees . Also document the Team Evaluator as a separate project role for the existing evaluation requirements. This preserves every audience from the vision. (Recommended)

Neither option adds accounts, an administrator interface, or live-user analytics. Personas will be illustrative archetypes based on the approved vision, not claims of user interviews or demographic research. Do not invent biographical facts or choose the ten evaluation fixtures at this stage.

## Question S2: How should the stories be organized?

A story describes one useful outcome for a user. The same approved requirements will be covered with every option; the choice changes how the document is organized.

A) User journey: group by the steps a traveler takes, from confirming preferences to reviewing and revising an itinerary; put team evaluation in a separate final section. This makes the overall flow easy to review. (Recommended)

B) Feature: group by capabilities such as preference intake, local discovery, schedule/budget presentation, feedback, and evaluation. This makes feature coverage easy to scan.

C) Persona: group stories by their primary persona, with shared stories written once and referenced by the other personas. This emphasizes each audience's needs.

D) Domain: group by business areas such as trip preferences, activity evidence, itinerary feasibility, and evaluation. This highlights rules that belong together.

E) Epic: use broad user goals as headings, each containing small stories with acceptance criteria. This emphasizes the hierarchy from goals to detailed outcomes; epics themselves are not treated as testable stories.

X) Other (describe the grouping; for a hybrid, state the primary grouping and where the secondary grouping applies after [Answer]:)

[Answer]:  A

## Question S3: How should acceptance criteria be written?

Acceptance criteria state what must be true for a story to be satisfied. Both options cover the successful path, relevant boundaries, and failure cases, using the same approved rules.

A) Given / When / Then scenarios: describe the starting situation, the action, and the expected result. For example: Given a six-day trip, when the traveler requests generation, then the app asks for dates within the five-day limit. (Recommended)

B) A numbered checklist of observable outcomes, grouped into successful, boundary, and failure cases where relevant. For example: Reject a six-day trip and request dates within the five-day limit.

X) Other (describe the acceptance-criteria format after [Answer]:)

[Answer]: A

## Recorded choices and approval scope — 2026-11-25T00:50:51Z (historical)

- S1 is a custom text answer, not a literal selection of option A: Recent Graduate, Abroad Student, cultural explorer, Fiancees, and the Team Evaluator role. Preserve the actual text above; do not rewrite it as an A/X response.
- S2=A selects user-journey organization, with team evaluation in its own section.
- S3=A selects Given / When / Then criteria.
- The team said exactly “Ok, user stories approval is done”. Record this approval for the current story-planning work; it is not approval of stories/personas that have not been generated.
- SC1 in [story-planning-clarification-questions.md](story-planning-clarification-questions.md) distinguishes an engaged individual within the approved MVP from a request for couple planning. Do not infer a traveler-count or budget change.
- The Cultural Explorer label fits the approved local-cultural-discovery purpose. Existing hobby/event capabilities remain required, even though their former persona labels are not in the new list. Reconcile affected persona wording in the vision/requirements after SC1 is resolved, preserving original answers in the audit.
- Approval already received for the current approach is retained. A clarification within existing scope will satisfy the question gate; material scope changes require review of the changed requirements/plan. Generated artifacts will have their own approval gate.

## Resolved choices — 2026-11-25T00:56:16Z

- SC1 says exactly: `  OK, scratch the fiancees as a person and use three `. This removes Fiancees and leaves the other three traveler personas from S1: Recent Graduate, Abroad Student, and Cultural Explorer.
- Team Evaluator remains the separate project role already requested in S1; it is not a fourth traveler persona or an account type.
- S2=A and S3=A remain selected: user-journey organization and Given / When / Then criteria.
- The existing approval statement “Ok, user stories approval is done” is carried forward. This clarification removes the ambiguity within the approved single-traveler scope; no repeated plan approval is needed.
- The vision audience table and requirements audience paragraph are reconciled with the actual decision. All product behavior and seven design deferrals remain unchanged.
- Generate the agreed artifacts now, then pause for approval of the generated stories/personas before Workflow Planning.

## Approved story-writing method

Use Standard depth. Each story will have a stable US identifier, a concise title, the relevant persona IDs, an `As a ... I want ... so that ...` narrative, references to approved FR/NFR IDs, Given / When / Then acceptance criteria, and any known dependency or explicit design deferral.

Keep each story centered on one observable user goal. Split a goal when it contains independently useful outcomes; keep boundary and failure cases with their related goal unless they form a separate user outcome. Do not force a one-to-one mapping between stories and requirements, prescribe a story count, or repeat the same story under several personas.

Apply INVEST:

- Independent: express a separately understandable and verifiable outcome; state unavoidable dependencies instead of hiding them.
- Negotiable: leave implementation choices to design while preserving approved product constraints.
- Valuable: explain the benefit to a traveler or the existing team-evaluation role.
- Estimable: provide enough context and criteria for later estimation; do not invent effort estimates here.
- Small: split broad goals into focused outcomes.
- Testable: use observable results and explicit limits, not claims such as fast, accurate, or intuitive without criteria.

For each persona, document the source audience, goals, current difficulties, relevant constraints, success signals, and mapped story IDs. Use descriptive role names; illustrative motivations must be distinguishable from researched facts. The Team Evaluator represents the six-member team's existing evaluation work, not a new product account or dashboard.

## Comparison of organization approaches

| Approach | Benefit for this project | Trade-off |
| --- | --- | --- |
| User journey | Shows intake, review, feedback, revision, and new-trip flow in order | Shared constraints must be linked across steps |
| Feature | Makes capability coverage easy to scan | End-to-end journeys need cross-references |
| Persona | Highlights distinct motivations already in the vision | Shared behavior must be referenced to avoid duplication |
| Domain | Keeps related rules such as scheduling and evidence together | Less immediately recognizable as a traveler journey |
| Epic | Connects broad goals to small stories | Can become too broad unless each child story has a clear outcome |

A hybrid is possible through S2=X, but needs explicit grouping rules before approval. Organization does not set implementation priority, sprint order, or component boundaries.

## Coverage to preserve in every organization

This table is a coverage guide, not generated stories or a selected grouping.

| User outcome or obligation | Approved sources | Cases that must remain visible |
| --- | --- | --- |
| Confirm a valid trip and interests | FR-01/02 | One traveler/city, one to five inclusive days, no past live start, up to three additional clarification turns, valid-summary confirmation |
| Discover relevant local activities | FR-03/04/05 | Shared activity-search limit, separate cached baseline, at most one overlap, cited local evidence, interest fit |
| Understand source provenance | FR-06/16; NFR-02 | Session-owned sources, cross-session/stale rejection, server restart, no model-invented links |
| Review a feasible daily plan | FR-07/08/09 | Two-to-four target, honest shortfalls, confirmed event dates, local time, positive durations, opening hours, 30-minute buffers, 9 AM–10 PM |
| Understand activity costs | FR-10/11 | Original budget/currency, USD comparison, dated/source-labeled estimates, unknown costs excluded and flagged, conditional WSJ access |
| Mark and replace disliked activities | FR-12/13 | Preset-only feedback, no immediate replacement, thumbs-up locks, preserve unaffected activities/preferences, keep disliked item if no substitute |
| Change preferences deliberately | FR-14 | Confirm new trip before replacing old state; fresh session/baseline and allowance |
| Recover from service failures | FR-04/15; NFR-06 | One bounded retry for model/activity search, no usable baseline stops new generation, preserve last valid state |
| Use the desktop interface | FR-17 | English, Chrome/Safari, chat and day cards, keyboard/focus/contrast/text labels, progress/errors |
| Evaluate and remove anonymous records | FR-18/19 | Ten profiles/three deferred cities, final-only activity KPIs/latest ratings, full revision count, allowlisted records, link checks, N/A denominators, deletion after demo |
| Carry technical quality constraints forward | NFR-01 through NFR-06 | Local planned stack/model, privacy, maintainability, example tests/coverage, partial PBT, measured performance; trace in a cross-cutting section without inventing user-facing features |

All seven DEF items in requirements.md remain tracked. Persona illustrations and story scenarios must not be presented as selected evaluation cities/fixtures. Rate access, freshness/rounding/failure details, model feasibility, PBT framework selection, and other deferred choices remain assigned to their approved later stages.

## Required outputs and review

After the plan is approved, create `aidlc-docs/inception/user-stories/personas.md` and `aidlc-docs/inception/user-stories/stories.md`. Include the persona-to-story mapping and a requirement-to-story/constraint coverage matrix in those documents. Technical obligations that have no direct user story still appear in the cross-cutting matrix with an explanation; none is silently dropped.

The stage review will present both artifacts, the completed generation checklist, audit.md, and aidlc-state.md. Generated stories/personas require a separate explicit approval before Workflow Planning. The overall workflow stops after Units Generation approval, before Construction.

## Execution checklist — Part 1: Planning

- [x] Record the actual Requirements Analysis approval and update its stage/plan status.
- [x] Load the stage/common rules, approved requirements and answers, vision, prior reverse-engineering context, and assignment.
- [x] Assess the value of User Stories and document the decision in user-stories-assessment.md.
- [x] Evaluate all eight question categories and carry forward settled product decisions.
- [x] Propose a story-writing method, compare five breakdown approaches, and prepare S1–S3 with blank answers.
- [x] Validate the plan/questions, preserve prior work, update audit/state, and present the plan.
- [x] Receive and record all three answers exactly; complete plan snapshot recorded 2026-11-25T00:50:51Z.
- [x] Analyze all three answers: S2/S3 clear; S1 introduces a persona whose traveler-count implications need clarification.
- [x] Create SC1 in a separate clarification file; preserve every original answer.
- [x] Receive and validate SC1; remove Fiancees, retain three traveler personas plus the Team Evaluator role; recorded 2026-11-25T00:56:16Z.
- [x] Update the method with S2=A and S3=A and record the team’s existing approval statement.
- [x] Finalize persona grouping and reconcile vision/requirements audience wording from S1/SC1; no change to approved product behavior.
- [x] Record the team’s approval statement for the current story-planning work at 2026-11-25T00:50:51Z; SC1 is now resolved within the existing product scope.

## Execution checklist — Part 2: Generation (after plan approval only)

- [x] G1: Read the entire approved plan and relevant requirements; confirm the approval record and next incomplete step.
- [x] G2: Generate personas.md using the selected grouping, grounded goals/constraints, and stable persona IDs; add final story mappings in G5.
- [x] G3: Generate stories.md in the selected organization using the proposed small-outcome method, stable US IDs, persona references, user-value narratives, and FR/NFR references.
- [x] G4: Include acceptance criteria for every story in the selected format; cover successful paths, relevant boundary/failure cases, exact limits, and preserved state.
- [x] G5: Map every persona to relevant stories and every FR/NFR to stories or explicit cross-cutting obligations; retain all DEF dependencies.
- [x] G6: Review INVEST, duplicated/conflicting criteria, scope boundaries, all coverage rows, extension applicability, and Markdown/link validity; resolve findings.
- [x] G7: Update all completed generation checkboxes and state, append the exact stage review prompt to audit.md, and present stories.md/personas.md and records for approval.
- [x] G8: Receive and record explicit approval of generated stories/personas; only then mark the User Stories stage complete and transition to Workflow Planning.

Mark each step complete in the interaction that completes it. No Part 2 step is authorized by a blank answer or by the prior requirements approval alone.

## Extension status and sources

Security and Resiliency extensions are disabled; project-specific security/privacy and failure rules stay in acceptance coverage. Partial PBT remains enabled. Its implementation/test checks are N/A for this planning artifact; NFR-05 and DEF-05 remain requirements for later applicable stages. The [assessment](user-stories-assessment.md) records the per-rule rationale; there is no blocking extension finding at this stage.

Sources: [approved requirements](../requirements/requirements.md), [vision](../../../vision.md), [technical environment](../../../tech-env.md), [User Stories rule](../../../.aidlc-rule-details/inception/user-stories.md), the attached milestone, and the actual [audit](../../audit.md) and [state](../../aidlc-state.md).
