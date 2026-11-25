# Requirements Review: Input Document Changes

Status: Approved with the Requirements Analysis review package; exact response "Approved " recorded 2026-11-24T21:03:33Z. These edits reconcile actual team answers with the original input wording. Original answers are preserved in question files and audit snapshots. No example code, AGENTS.md, rule files, or .gitignore was changed.

## Changes by file and decision

### README.md

- C1/D1/Q14: preserve ten profiles/three destinations, record city deferral and final-only KPI snapshot.
- C2/C3/D2: describe selected-currency budget, USD conversion, WSJ source, and conditional automated retrieval.
- Q15: name Sophia and shared-call decision process while retaining general meeting commitments.

### vision.md

- C1/D1/Q14: evaluation scope, city deferral, final-only measurement and failure reporting.
- Q1/Q2/Q3: English/any-single-destination intake, date validation, clarification cap and confirmation.
- Q4/C2/C3/D2: supersede no-conversion rule with USD comparison and conditional WSJ integration.
- C2/D2: distinguish unknown/unconvertible prices from zero and maintain honest totals.
- Q9: share search allowance across generation/revisions.
- Q7/Q8/Q9: provider content, failed-baseline behavior and shared cap.
- Q6: omit events without evidence of occurrence during trip.
- Q5/C4: activity-based estimates without fixed range, schedule constraints retained.
- Q10/Q11: retain disliked activity on no replacement and confirm new-trip changes.
- Q12/Q13: desktop accessibility and bounded retry behavior.
- Replace answered open questions with actual recorded design/Construction deferrals; keep approval status explicit.

### tech-env.md

- C3/D2: add planned conditional WSJ rate integration.
- C3/D2: reconcile external-service boundary and preserve access feasibility gate.
- C2/C3/D2: add currency responsibility within the existing modular application.
- Q2: bound clarification and confirm valid preferences.
- Q9/Q13: cumulative activity-search allowance.
- Q8/Q13: specify retry and prior-state behavior.
- Q1/Q3: geography, language, inclusive dates and past-trip restriction.
- C2: remove no-conversion prohibition and specify original/converted display.
- C2/D2: explicit rate uncertainty and agreed design details.
- Q5/C4: duration estimation rule.
- Q6: event occurrence validation.
- Q7/Q8: evidence enrichment and fail-closed baseline behavior.
- Q10/Q11: preserve rejected item on failed replacement and confirm new-trip reset.
- Clarify account exclusion without contradicting existing source-session authorization.
- C5/Q17: record extension opt-outs without dropping project security.
- C1/D1/Q14: evaluation city deferral and final-only metric rules.
- Q18 and currency scope: add partial-PBT obligations and mocked rate testing without implementing tests.
- Q12: document desktop/browser/accessibility scope.
- Update input review tense and distinguish answers from pending requirements approval.

## New requirements artifact

requirements.md records 19 functional and 6 non-functional requirements, acceptance criteria, source traceability, the team-approved scope changes, seven explicit design/verification follow-through items, and extension applicability. Evaluation-city selection and automated WSJ feasibility are explicitly deferred by D1/D2; neither is claimed completed. The separate requirements approval was recorded 2026-11-24T21:03:33Z.

## Preservation and validation

- All original Q/C/D answer text is unchanged.
- The three Python blocks in tech-env.md are identical to their pre-edit contents and still match the example files.
- Existing source and test files are unchanged; tests were not run.
- No dependency installed, rate scraped, paid service activated, commit created, or push performed.
- Markdown fence/table structure, Python code-block syntax, requirement IDs, and answer counts were checked.
