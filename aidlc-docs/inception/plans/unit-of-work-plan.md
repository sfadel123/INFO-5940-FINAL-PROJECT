# Unit of Work Plan and Team Questions

Status: Units plan approved through UG1=A and UG2=A, recorded 2026-11-25T02:12:10Z. All three generated artifacts separately approved with "approve and finish inception ", recorded 2026-11-25T02:27:53Z. P1–P7/G1–G7 and Inception are complete; work stopped before Construction.

Please discuss both questions and fill each `[Answer]:` with your actual choice. For B in UG1, include names and module IDs; for requested changes or Other, include the concrete change. No answer is preselected. UG2=A approves this plan only after UG1 is complete and any conflicts are resolved. The generated unit documents will have a separate final review.

## 1. Scope and evidence

Keep one application unit, **U01 — Cultural Travel Planner**, containing the entire local product. The installed [Units rule](../../../.aidlc-rule-details/inception/units-generation.md) defines a monolith as one unit with logical modules. Nine modules do not mean nine deployments, services, Construction loops or teammate assignments.

Use the approved [design](../application-design/application-design.md), [components](../application-design/components.md), [methods](../application-design/component-methods.md), [services](../application-design/services.md), [dependency matrix](../application-design/component-dependency.md), [requirements](../requirements/requirements.md), [stories](../user-stories/stories.md), [personas](../user-stories/personas.md), [execution plan](execution-plan.md), and the existing-example reverse-engineering records. Preserve all 19 FRs, six NFRs, 17 stories and 59 acceptance scenarios. This stage groups that scope; it does not introduce new product features or change the approved providers, limits, budget, privacy or revision rules.

The workspace was routed through limited Brownfield analysis because a standalone teaching example exists. The product itself is new: preserve `examples/trip-validation/` and propose a separate application package. Application code remains outside aidlc-docs. Document organization follows the single-unit structure pattern in [code-generation.md](../../../.aidlc-rule-details/construction/code-generation.md); reading that structure reference does not start Construction.

## 2. Proposed module and code organization

Every path in this section is proposed future code under the repository root, not a file created by this plan. Keep component IDs C01–C09 as module identifiers to avoid a second competing catalog. Shared data definitions and the startup wiring are support code within U01, not new business modules.

| Module | Proposed code location | Responsibility and boundary |
| --- | --- | --- |
| C01 Desktop UI/API | `src/travel_planner/web/`, `src/travel_planner/templates/`, `src/travel_planner/static/` | Local FastAPI/Jinja2 interface, accessible chat/cards and typed commands; calls C03 |
| C02 Preferences | `src/travel_planner/preferences.py` | Pure required-field, date and budget validation; confirmation rules |
| C03 Trip coordinator | `src/travel_planner/coordinator.py` | Python-guided intake/generation/revision/new-trip/evaluation flow; coordinates other modules |
| C04 Model adapter | `src/travel_planner/adapters/model.py` | Planned Ollama/OpenAI-client boundary; bounded proposals only |
| C05 Search/evidence adapter | `src/travel_planner/adapters/search.py` | Tavily baseline/activity calls; evidence batches, no canonical state mutation |
| C06 Currency | `src/travel_planner/currency/` | Separate ECB acquisition and pure arithmetic so C07 cannot fetch rates |
| C07 Itinerary validation | `src/travel_planner/validation/` | Pure source/locality, schedule, budget, distinctness and revision-preservation checks |
| C08 Ephemeral sessions | `src/travel_planner/sessions.py` | Server-owned state, source registry, pinned caches, counters, versions and operation guards |
| C09 Team evaluation | `src/travel_planner/evaluation/` | Separate pure record projection/KPIs from link checks and ratings-file I/O |
| Shared support, within U01 | `src/travel_planner/contracts.py`, `src/travel_planner/config.py`, `src/travel_planner/main.py` | Shared typed objects, runtime configuration and app startup wiring; no duplicate business rules |
| Verification, within U01 | `tests/unit/`, `tests/api/`, `tests/integration/`, `tests/property/`, `tests/fixtures/` | Later tests and synthetic fixtures; PBT framework remains deferred |
| Nonsecret configuration | `config/` if a configuration file is needed | Keep secrets in runtime environment variables; do not add a second dependency manager or provider |

Startup wiring may instantiate modules and supply dependencies, but request handling must still obey the approved calls: C01 to C03; C03 to C02/C04/C05/C06/C07/C08/C09; C07 to C06's pure arithmetic only. Shared contracts/configuration do not import service implementations. No internal network transport or separately released shared library is proposed. Exact helper-file splits and dependency-injection mechanics belong to later design/code planning.

U01 has no other application-unit dependencies: its unit-level matrix will have one row/column with no self-dependency. The separate internal-module matrix will preserve the approved acyclic graph. Ollama, Tavily, ECB and public source-link checks are external integration boundaries, not additional units of work. The anonymous ratings file is the approved local output, not a database service.

## 3. Story grouping and integration proposal

Keep the approved user-journey organization. The generated story map will assign each story exactly once to U01, with a primary coordinating/responsible module and all contributing modules. A primary module is a design responsibility, not a person's assignment. One unit does not mean one indivisible task or one person doing all the work.

| Approved journey | Stories to map to U01 | Main collaboration areas |
| --- | --- | --- |
| Confirm the trip | US-01, US-02 | UI, preference rules, coordinator, model interpretation and sessions |
| Discover and review | US-03, US-04, US-05, US-06, US-07 | Evidence/model adapters, currency, validation, coordinator and UI |
| Give feedback and revise | US-08, US-09, US-10 | UI, sessions, coordinator, evidence reuse and preservation validation |
| Start a different trip | US-11 | Confirmation, UI, coordinator and session reset |
| Recover and use the interface | US-12, US-13, US-14 | Bounded failures, session provenance and accessible UI |
| Evaluate the MVP | US-15, US-16, US-17 | Final-snapshot projection, link checks, metrics and cleanup |

For later implementation coordination, propose this dependency order within the single unit: establish shared contracts and pure rules; add isolated session/provider boundaries with fakes; integrate the coordinator and UI through the approved user journeys; connect final-snapshot evaluation and verify the complete flow. Add relevant checks with each part rather than waiting until the last part. This is a planning dependency order, not a Construction code-generation plan, sprint commitment or authorization to implement.

All six NFRs remain obligations of U01: NFR-01 local runtime/planned model, NFR-02 privacy/trust, NFR-03 maintainability/contracts, NFR-04 example/API/integration verification, NFR-05 partial PBT, and NFR-06 bounds/measured performance. The generated map will show their contributing modules and later verification locations. Keep DEF-01–03 resolved at design level and retain actual evaluation/rate verification later; preserve remaining detailed DEF-04 work and DEF-05–07 verification without inventing successful tests or provider access.

## 4. Assessment of every required question category

| Category | Applicability and evidence | Question or explicit reason for no new decision |
| --- | --- | --- |
| Story grouping | Applicable; S2=A already chooses journeys, all 17 stories belong to the one approved product | UG2 reviews the concrete unit/module mapping proposal; no repeat choice of story organization |
| Dependencies | Applicable; approved component-dependency.md fixes typed internal calls and provider boundaries | UG2 reviews translation into one unit and internal modules; separate inter-unit transport is N/A because there is only one unit |
| Team alignment | Applicable; README specifies equal contributions, frequent meetings and division of work; Sophia operates shared Inception sessions | UG1 decides whether unit records retain shared ownership or record named module owners now; the operator role does not imply technical ownership |
| Technical considerations | Applicable, already settled by NFR-01 and Application Design: one local deployment and shared runtime/resources | UG2 preserves those constraints; no separate deployment/scalability question because no component has an approved independent deployment requirement |
| Business domain | Applicable; personalized trip planning and its team evaluation support are one product, with the approved nine responsibility boundaries | UG2 reviews the boundary; no new bounded-context choice is needed and evaluation does not become a separate product/service |
| Code organization | The mandatory question category is for greenfield multi-unit projects, which this is not | No multi-unit deployment question. Nevertheless, section 2 supplies a concrete new-product code strategy for UG2 review; examples stay separate and unchanged |

## Question UG1 — Team ownership recorded in the unit documents

How should module ownership be recorded for later Construction?

A) Shared team ownership, with specific work divided in team meetings as described in README. Do not assign permanent module owners now. Sophia remains the shared-session operator, not the assumed owner of every module. (Recommended; preserves the current collaboration plan.)

B) Record named module owners now. After the answer tag, list the actual teammate name(s) for each C01–C09 module; shared ownership is allowed if explicitly named. Team review and equal contribution still apply.

X) Other (describe the ownership arrangement after the answer tag).

[Answer]: A

## Question UG2 — Approve this concrete unit plan

With the ownership choice in UG1, is this plan ready for generation of the three unit documents?

A) Approve U01, the nine-module mapping, proposed folder layout, dependency/story treatment, verification obligations and checklist below. Generate the three documents, then present them for separate final approval. This does not authorize Construction.

B) Request changes before generation. Describe the specific unit/module, folder, dependency, story-mapping or plan change after the answer tag.

X) Other (describe the requested approach after the answer tag).

[Answer]: A

## 5. Execution checklist

- [x] P1. Record the actual Application Design approval; mark its G10 and stage complete.
- [x] P2. Load the approved requirements/stories/design, existing-example context, Units/common rules and current extension configuration.
- [x] P3. Evaluate all six question categories; prepare the concrete one-unit proposal and context-relevant questions.
- [x] P4. Validate this plan, save it with blank answer tags, preserve a verbatim issued snapshot in audit.md, and present the plan and updated records.
- [x] P5. Receive and append both actual team answers and any accompanying approval/change request with actual recording timestamps.
- [x] P6. Analyze completeness, ambiguities and conflicts; obtain and record targeted follow-ups only if needed.
- [x] P7. Record explicit approval of the resolved plan before generation. UG2=A can provide this approval when the other answer is complete and consistent.
- [x] G1. Read the complete approved plan and relevant context before executing its next uncompleted generation step.
- [x] G2. Generate `aidlc-docs/inception/application-design/unit-of-work.md` with U01 scope, module responsibilities, code organization, actual ownership decision and later-work boundary.
- [x] G3. Generate `aidlc-docs/inception/application-design/unit-of-work-dependency.md` with the one-unit matrix, internal-module matrix, external boundaries and dependency/integration order.
- [x] G4. Generate `aidlc-docs/inception/application-design/unit-of-work-story-map.md` mapping all US-01–US-17 exactly once to U01, primary/contributing modules, FR/NFR coverage and later verification obligations.
- [x] G5. Validate boundaries and acyclic calls; confirm all 17 stories, 19 FRs, six NFRs and seven DEF dispositions are covered, with no invented owner, answer, approval or implementation result.
- [x] G6. Validate Markdown/links and any diagrams with text alternatives; check preservation of examples/answers/product scope; update checkboxes, state and audit; present all three generated documents and records for final approval.
- [x] G7. Receive and record actual Units Generation approval, mark this stage and Inception complete, and STOP before Construction. If changes are requested, revise and present again rather than claim approval.

## 6. Extension compliance and preservation

Security Baseline and Resiliency Baseline are N/A because the team disabled them (C5=B and Q17=B); their full rules are not reloaded/enforced. Project-specific protections remain requirements. Partial PBT remains limited to pure functions and serialization round-trips.

| Rule | Current planning status | Reason and later obligation |
| --- | --- | --- |
| PBT-01 | N/A | Advisory; detailed property identification is later Functional Design |
| PBT-02 | N/A | No serialization implementation/tests now; U01 contracts and pure record projection retain later round-trip checks |
| PBT-03 | N/A | No pure-function implementation/tests now; preferences, currency, validation and pure evaluation retain invariant checks |
| PBT-04 | N/A | Advisory; request idempotency still needs later functional/example checks |
| PBT-05 | N/A | Advisory; no oracle implementation created |
| PBT-06 | N/A | Advisory; do not expand partial mode into mandatory stateful/live-model PBT |
| PBT-07 | N/A | Domain generators are later test work; planned test utilities remain shared within U01 |
| PBT-08 | N/A | Shrinking, failure seeds and CI integration are later Construction obligations |
| PBT-09 | N/A | Framework selection remains DEF-05 for later NFR/design; no dependency is installed |
| PBT-10 | N/A | Advisory; all 59 story scenarios and complementary example-test obligations remain |

No applicable extension blocker. This is a planning applicability assessment, not completed testing. Preserve existing examples, all actual answer text and the root input-document content. Make status-only approval updates in existing workflow records where needed. Append to audit.md; never replace its existing history. No ratings file, new code, runtime tests, dependency installation, commit or push is part of this stage.

## 7. Approval and stop boundary

**Unit of work plan complete. Review the plan in aidlc-docs/inception/plans/unit-of-work-plan.md. Ready to proceed to generation?** Record the answer in UG2, after answering UG1.

The installed Units rules require explicit plan approval before generation. After the generated unit documents receive their separate approval, follow the user's stop instruction: end Inception before Construction. The generic rule template's suggestion to continue to Construction is overridden by that explicit boundary. Do not begin Functional Design, NFR stages, code generation or implementation tests.

## Received answers and plan approval

Recorded 2026-11-25T02:12:10Z: UG1=A retains shared team ownership and work assignment in meetings; UG2=A approves this concrete plan for generation. Both original answer lines remain unchanged, including whitespace. The full received file is preserved in audit.md. No ambiguity or follow-up is necessary. The earlier proposal/question wording is retained as issued context. Only the three planned unit documents will be generated; their final approval and the Inception stop remain separate.

## Generated artifacts and final review checkpoint

At the review recorded 2026-11-25T02:21:55Z, P1–P7 and G1–G6 were complete and G7 awaited actual final approval. That approval has now been received and G7 is complete. UG1/UG2 still contain the exact received A answers; their question/proposal wording is retained as historical context.

| Generated artifact | Review content |
| --- | --- |
| [unit-of-work.md](../application-design/unit-of-work.md) | U01 definition, nine modules, shared ownership, approved code organization and later-work boundary |
| [unit-of-work-dependency.md](../application-design/unit-of-work-dependency.md) | One-unit matrix, approved acyclic nine-module matrix, handoffs, provider/storage boundaries and future integration order |
| [unit-of-work-story-map.md](../application-design/unit-of-work-story-map.md) | All 17 stories assigned once, 59 existing scenarios, primary/contributing modules, 19 FRs/six NFRs and seven DEF dispositions |

Changes this interaction: created only the three unit artifacts; recorded actual answers/plan approval and advanced this checklist; updated [execution plan](execution-plan.md), [startup checkpoint](startup-plan.md), [state](../../aidlc-state.md) and appended [audit](../../audit.md). No root input, existing requirement/story/design, example or actual-answer content was changed. Primary-module assignments are generated design detail within the approved plan, ready for this review, not invented named team assignments.

Validation passed: 41 protected files unchanged; audit's original byte prefix unchanged; full received plan snapshot and raw answers preserved; all planned code locations represented; Markdown tables/fences/local links checked; unique story/requirement/NFR/DEF coverage checked; module matrix identical to the approved design and acyclic. New documents use tables/text and introduce no new diagrams. Existing execution-plan Mermaid receives status-label updates only with structural checks; no graphical render claimed. git diff --check passed. No application tests, live provider calls, source/test/config directories, dependency installation, ratings file, commit or push.

Extension review: Security/Resiliency disabled and skipped. PBT-01–PBT-10 are individually N/A at this documentation stage, with rationale and later obligations in unit-of-work.md; no applicable blocker.

Final decision received: "approve and finish inception ", recorded 2026-11-25T02:27:53Z. This separately approves the generated package and completes G7. UG2's earlier approval covered the plan. Work has stopped before Construction.

## Inception completion recorded

- Actual final user input: "approve and finish inception "
- Actual UTC recording timestamp: 2026-11-25T02:27:53Z.
- All three unit artifacts explicitly approved; P1–P7/G1–G7 are complete.
- All seven Inception stages are complete, with approvals recorded where required.
- [State](../../aidlc-state.md), [execution plan](execution-plan.md), [startup checkpoint](startup-plan.md) and [audit](../../audit.md) record the completed boundary. Artifact content/answers are preserved; only approval/status records change in this interaction.
- Construction and Operations remain unstarted. No implementation, tests, new commit, push or submission performed by this completion.
