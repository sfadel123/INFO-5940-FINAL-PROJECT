# Application Design — External Access Review

Original research recorded: 2026-11-25T01:26:42Z. Subsequent team decision: AD4=A approved at 2026-11-25T01:32:46Z, selecting ECB instead of WSJ. Research findings below predate that decision; no app integration, credential use or paid request is claimed.

## WSJ decision returned to the team (DEF-02)

The [selected WSJ page](https://www.wsj.com/market-data/currencies/exchangerates?eafs_enabled=false) returned loading text without rate values. The retrieved representation was cached; this is not a live browser or API test.

Official-domain searches and an attempted read of the [Dow Jones developer site](https://developer.dowjones.com/) did not establish a supported method accessible to this team. The developer site was unavailable through the reading tool. This limited investigation does not prove that no WSJ API or licensed access exists. No team credentials/access entitlement were supplied or assumed. Third-party scraper listings were not treated as official support and were not used.

Conclusion: automated WSJ retrieval remains unverified, so do not represent DEF-02 as successfully integrated or resolved. Return the decision through AD4, as required by the earlier D2 answer. A team-supplied official method would need documentation and access verification before implementation. No browser scraping, access bypass, invented rates or silent source substitution.

## Alternative researched and subsequently selected

The [European Central Bank reference-rate page](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html) publishes dated EUR-based reference rates, including USD and GBP, and links XML/CSV downloads. It says updates normally occur on working days and the rates are for information, not transactions.

Inference for this project: that published format is a plausible source for labeled travel-cost estimates, subject to team approval and Construction verification. It does not turn the planner into a booking/payment service. The linked XML request was rejected by the web-reading tool as an unsupported text/xml content type; no successful XML ingestion or production integration is claimed. No current numerical rates are copied into the plan or fixture budgets.

AD4 offers an explicit source change, a team-prepared WSJ table with changed fetching behavior, or evidence of usable official WSJ access. All options retain source/date labels, honest uncertainty and the existing prohibition on invented rates. Selecting one may require updates to README, vision, tech-env, requirements, and affected stories; those files are unchanged in this planning turn.

## Tavily documentation check (DEF-07, partial evidence)

The [official Search API documentation](https://docs.tavily.com/documentation/api-reference/endpoint/search) describes an authenticated search endpoint with explicit result-count parameters and source title/URL/content fields. Raw content is optional. This supports designing separate requests for the baseline and activity searches; it does not establish this team's account, allowance, pricing, raw-content availability or end-to-end results.

Use Python-owned search limits and explicit parameters in the proposed adapter. Do not assume provider defaults enforce product quotas. No Tavily API was called and no account/credits were inspected. Account availability, applicable limits/costs, dependencies and live behavior remain DEF-07 checks before integration.

## Review boundary

The [design plan](application-design-plan.md) now contains all six actual A answers and explicit plan approval. AD4 chooses ECB; AD3/AD5/AD6 settle fixtures and policy/defaults. Earlier proposal wording above records what was offered before selection. Current source documents are reconciled with these choices, and the generated Application Design awaits its own approval. DEF-05/06 and remaining DEF-07 work stay assigned to later design/Construction. Inception still stops after Units Generation approval.

## Follow-up explanation: effort, caching and Asia

The user asked whether another source could be scraped, whether repeated ECB downloads are expensive, and whether Asian trips work. No new source choice was made by that question. The design retains the approved structured download and trip snapshot reuse; it does not scrape a site or download for every activity/chat message. Currency coverage is separate from geographic destination coverage. Unsupported activity conversions stay unverified; an unconvertible budget pauses generation/revision under AD5=A. The official ECB table was re-read for the explanation; no live app benchmark or ingestion success was claimed.
