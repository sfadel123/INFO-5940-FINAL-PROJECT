# Requirements Analysis Clarification Questions

Status: All answers received and validated. Requirements approved by the team; recorded 2026-11-24T21:03:33Z. Original questions and answers remain unchanged as historical evidence; requirements.md applies later clarifications.

Five follow-ups resolve missing details and the effects of your custom answers. Please fill each `[Answer]:` or send numbered answers labeled C1–C5 in chat. All options below are proposals, not recorded decisions. Requirements Analysis cannot be completed until these points are resolved. No later-stage approval is requested here.

## Question C1: Evaluation destinations and profile count

Original Q1 answer:

> X, An English-language interface accepting any single destination, with evaluation and demonstrated quality limited to the ten named destinations.

The prior input documents specify 10 sample profiles across 3 destinations. Your answer specifies 10 destinations but does not name them or specify whether the profile count changes. The English-language interface accepting any single destination is clear and will be carried forward.

Which evaluation set should the requirements use? Include the actual destination names after your choice.

A) Ten sample profiles across ten destinations, one profile per destination. List all ten destinations.

B) Keep ten sample profiles across three destinations; "ten named destinations" meant ten profiles. List the three destinations.

X) Other (state the total profile count, number of destinations, and destination names after [Answer]:)

[Answer]: B

## Question C2: Currency used for the budget and totals

Original Q4 answer:

> X, do a currency conversion to USD while noting that the conversion happened. Keep unknown prices flagged from budget calculation

This explicitly adds currency conversion. The prior inputs let the traveler choose a currency and prohibit conversion. Your new instruction to convert prices to USD will take precedence once the input/output behavior is clear. Unknown prices remain flagged and excluded from the calculated total.

How should the traveler enter a budget after this change?

A) Use USD only for the entered budget and all calculated totals. Convert verified prices from other currencies to USD and clearly label conversions.

B) Keep a traveler-selected budget currency, but convert both that budget and activity prices into USD for comparison and totals; show the original budget/currency and label conversions.

X) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question C3: Source of currency-conversion rates

Q4 adds conversion, but there is no approved exchange-rate source. The existing environment limits external services to the search provider and GitHub. The LLM must not invent an exchange rate.

Which rate-source approach should guide design? In either listed option, show the rate's source and date, label converted costs as estimates, and flag/exclude a price from the budget total if no valid rate is available. Provider selection, rate freshness thresholds, and rounding details will be documented during design; no paid account is assumed.

A) Add an exchange-rate service to the planned integrations. Choose the specific provider after reviewing access, supported currencies, limits, and cost during design. Rates must come from that service, not model memory.

B) Use a team-maintained local table of rates with an identified source and date. No additional online service is required; conversions work only for currencies included in the table.

X) Other (please describe the rate source and unavailable-rate behavior after [Answer]:)

[Answer]: X, get rates from the Wall Street Journal Currency Exchange Rates: https://www.wsj.com/market-data/currencies/exchangerates?eafs_enabled=false

## Question C4: Bounds for model-estimated durations

Original Q5 answer:

> X, Let the model estimate by activity type, based on similar activities. Let the user know an estimate was made. Source-provided durations are not subject to this estimate range.

The answer clearly requests activity-based estimates and visible estimate labels. It refers to "this estimate range" without stating a range. The earlier option B used 30–180 minutes.

Which bounds should apply when the source supplies no duration?

A) Keep the 30–180-minute range for model estimates based on similar activities; omit an activity if a plausible estimate cannot fit that range.

B) Use no fixed 30–180-minute range. Require a positive estimate that fits the remaining day, 9 AM–10 PM window, opening hours when known, and 30-minute buffers; omit activities that cannot fit.

X) Other (please state the desired range or rule after [Answer]:)

[Answer]: B

## Question C5: Full security extension versus the original local-app scope

You selected A in Q16, enabling the full Security Baseline. That selection remains active unless you change it here. Loading the selected rules revealed requirements beyond the existing technical document:

- SECURITY-01 requires encryption for persisted data stores, including the local ratings file, and protected transport for store access.
- SECURITY-03 requires structured application logging routed to a centralized log service.
- SECURITY-14 requires security-event alerts, a monitoring configuration, append-only or tamper-evident logs protected from application deletion, and a default minimum security-log retention of 90 days.
- Other enabled rules add requirements such as HTTP security headers and server-side access checks. Cloud-only infrastructure checks can be N/A when no such resources exist; applicable local requirements cannot be silently marked N/A just because this is a class demo.

The 90-day default concerns separate operational/security logs. It does not authorize keeping the traveler ratings file past the final demo. The current inputs do not specify these additional controls, permit only limited services, and say the app will persist only anonymous evaluation data.

How should these requirements be reconciled?

A) Keep the full Security Baseline enabled and expand the local-demo plan to satisfy its applicable controls: encrypted persisted stores, secure transport where required, a centralized logging component/service, and separate minimal operational/security logs with access protection, alerts, monitoring, and retention. Keep traveler data out of security logs and delete the separate ratings file after the final demo. Document the supporting components and validate the controls during Construction.

B) Revise Q16 to skip the optional Security Baseline extension. Keep every previously agreed project-specific security/privacy requirement, including secret handling, input/output validation, source-session checks, loopback binding, bounded tools, HTTPS for external services, safe errors, and ratings deletion.

X) Other (describe an explicit scoped override and which extension requirements it changes after [Answer]:)

[Answer]: B
