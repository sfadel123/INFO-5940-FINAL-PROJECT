# Remaining Requirements Clarifications

Status: All answers received and validated. Requirements approved by the team; recorded 2026-11-24T21:03:33Z. Original questions and answers remain unchanged as historical evidence; requirements.md applies later clarifications.

Please fill each `[Answer]:` or send D1–D2 answers in chat. No choices below are selected on your behalf.

## Question D1: Names of the three evaluation destinations

C1=B confirms ten sample traveler profiles across three destinations. The three names requested in C1 were not supplied. The app still accepts any single destination; this choice only specifies the evaluation sample.

How should the evaluation destinations be recorded?

A) Name the three destinations now. Include all three city names and their countries after your answer.

B) Explicitly defer selection of the three evaluation destinations to Application Design and proceed with the fixed ten-profile/three-destination evaluation scope. Record this as an unresolved fixture-selection task, not as a completed selection.

X) Other (please describe after [Answer]: tag below)

[Answer]:  B

## Question D2: How the application obtains WSJ rates

C3 names this source: [Wall Street Journal Currency Exchange Rates](https://www.wsj.com/market-data/currencies/exchangerates?eafs_enabled=false). The source choice is recorded and will be preserved.

A read-only web check returned the page heading and loading text without rate values. Automated access is therefore unverified; this does not establish that your browser cannot display the rates or that access requires payment. The existing MVP excludes browser scraping, and no paid service or account is assumed.

Which approach should the MVP use to obtain rates from the selected WSJ source?

A) A team member reads WSJ through their legitimate access and maintains a local rate table. Store the source URL and rate date with the table. The app uses those recorded rates and labels conversions as estimates; this adds no live rate-retrieval integration.

B) Plan automated retrieval from WSJ. Confirm a supported, accessible method during Application Design, without bypassing access restrictions or adding browser scraping. If no suitable method can be verified, return the integration decision to the team before implementation rather than substituting another source or inventing rates.

X) Other (please describe the intended retrieval method after [Answer]:)

[Answer]: B

## Rules retained for either rate approach

- Keep the selected WSJ source, record the source and rate date, and label conversions as estimates.
- Do not invent rates or obtain them from model memory.
- A price without a valid conversion remains flagged as unverified and excluded from the calculated activity total; never count it as a verified zero-cost activity or guarantee the full total is within budget.
- Preserve the user's original budget/currency and show USD conversions, per C2=B.
- Rate freshness thresholds, rounding, and detailed unavailable-budget-conversion behavior will be specified and reviewed during Application Design; no working integration or current rate value is asserted here.
