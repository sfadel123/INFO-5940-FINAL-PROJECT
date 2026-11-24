# Vision Document

## Executive Summary

Our project is an agent that personalizes travelers itineraries based on their specific interests. The LLM agent will ask users their destination, dates, budget, and key areas of interest. From these inputs, the agent will create a personalized itinerary that gives the traveler local and harder to find activities that they may not have found otherwise. It addresses the desire travelers have to truly explore the place they are visiting, without relying on popular and TikTok recommendations and without the time spent doing deep research themselves or the money spent on a travel agent. With these agents, users are expected to be more excited about their travel plans and gain access to local activities that fit with their interests.

## Business Context

Oftentimes when traveling, users rely on a few key places for recommendations: google, social media, or a travel agent. More recently, however, users have started to rely on LLMs to provide them with recommendations of where to eat or what to do when they are traveling. We have found that these recommendations are very similar, bringing tourists to the same overcrowded places or telling them to engage in activities that may not be what they want to spend their vacation doing. Our agent plans to address the pain point these travelers face by giving customized recommendations and building a catered itinerary based on budget, travel dates, and user preferences.

We are aiming at targeting individuals in their 20s and 30s. These are travelers who are already accustomed to LLMs, likely utilize social media in their travel preparation, and do not have the money to afford a travel agent. They are young and adventurous, hoping to immerse themselves in the local culture without solely going to places coined “tourist attractions.” Ultimately, we aim for this tool to be helpful for any traveler, regardless of age.

| User | Description | Primary Need |
| --- | --- | --- |
| Recent Graduates | Individuals who are traveling and want to explore local activities on a budget | Local recommendations that fit within a certain budget |
| Individuals Exploring Hobbies | Individuals who have been exploring activities like pottery and painting and want to continue these pursuits on vacation | Catered recommendations based on interests |
| Pop-Up Enthusiasts | Individuals who love exploring pop-ups | These individuals need recommendations tailored to their interests and their time traveling in that location |
| Abroad Students | Living in a new place for the first time, want to go beyond basic tourist attractions | Want recommendations catered to preferences and interests to explore a new city. Wants drop-in activities that help them meet locals, like a run club meetup or a cooking class |

### Success measurement

KPIs are measured during team evaluation rounds, not with live users. Each round uses 10 sample traveler profiles across 3 destinations. For each itinerary, log only anonymous data: a random itinerary ID, number of activities, number of revision requests, number of baseline overlaps, link-check results, and activity ratings.

| KPI | Definition and denominator | Target |
| --- | --- | --- |
| Activity approval rate | Thumbs-up ratings divided by rated activities | At least 70% |
| Revision rate | Test itineraries needing more than two revision requests divided by test itineraries | Under 30% |
| Local-discovery rate | Recommended activities absent from the baseline and meeting the local criteria below, divided by all recommended activities | At least 70% |
| Source coverage | Recommended activities whose source link loads in an automated check, divided by all recommended activities | 100% |

The team will review these KPIs after each round of testing and use them to adjust prompts, search queries, and ranking rules. A short satisfaction questionnaire after the trip is a future addition.

## Full Scope Vision

The goal of this agent is to provide individuals with more personalized travel recommendations based on interests, budget, and destination. Long term, the product would add saved profiles that learn from ratings and past trips, an optional personality quiz (for example, introvert or extrovert, spontaneous or structured), social media sources, booking, and calendar export.

## MVP Features in Scope

Our MVP will focus on providing individuals with a customized itinerary for their travels.

- **Conversational Preference Intake:** The chatbot will ask the individual a series of questions in conversation to understand their travel preferences, with follow-up questions when an answer is vague (for example, asking whether "art" means museums or hands-on classes). These include the destination, time of travel, budget, and preferred areas of activities. Maximum trip length is 5 days, for one traveler.
- **Budget:** One total activity budget covers the whole trip for one traveler, including activity tickets and fees only. Flights, lodging, meals, and local transport are excluded. The user chooses one currency, default USD; no currency conversion is performed. Unknown prices are labeled "unverified," flagged to the user, and excluded from the budget calculation. An itinerary with unknown prices does not establish that the full trip's activity cost fits the budget.
- **Recommendations:** The LLM agent gathers activities from the internet that fit the user's preferences, accounting for event times and activity reviews. Up to 2 activity searches per trip day are allowed, capped at 10 activity searches per generation, with up to 5 results each. The baseline is a separate system Tavily search for "top things to do in [destination]," run once per itinerary generation and returning up to 10 results. It does not count toward the activity-search limit. The baseline is cached in the session so revisions reuse it; the five-results-per-search and ten-searches-per-generation limits apply only to activity searches. At most one activity per itinerary may match that baseline. All other activities must qualify as local: absent from the baseline and either independent (not a chain), a time-limited event (pop-up, class, festival), or found through a local source (local news, city or venue event listings, community organizations). The model must cite its evidence; Python checks baseline overlap by name and URL. Each item includes one sentence explaining how it matches the user's stated interests.
- **Daily Itinerary Generation:** Target 2 to 4 distinct activities per day. If too few suitable, distinct activities are found, show fewer, tell the user how many were found, suggest broadening their interests, and never invent activities. Each activity shows its time, location, estimated duration, estimated cost (or "unverified"), source link, and explanation of interest fit.
- **Scheduling Feasibility:** All times use the destination's local time zone. Each activity has an estimated duration, labeled as an estimate if the source does not give one. Activities must not overlap and must have a 30-minute buffer between them. Schedule activities between 9:00 AM and 10:00 PM and within opening hours when known; otherwise label hours "unverified." Route optimization remains out of scope.
- **Feedback and Revisions:** Users give a thumbs up or down plus an optional preset reason: "too touristy," "too expensive," "wrong time," or "not my interest." There is no free-text feedback. A thumbs-down marks an activity without replacing it immediately. When the user clicks "Update itinerary" or asks in chat, the agent replaces only thumbs-down activities. A thumbs-up locks an activity. Unaffected activities and all preferences stay unchanged.
- **Source Provenance and Privacy:** Retrieved sources are held in server memory, tied to a random session ID, and cleared on server restart. The browser sends that session ID with each request. The backend rejects any source ID in a submitted itinerary or revision that does not belong to that session. Anonymous evaluation data and ratings are stored in `ratings.jsonl`, listed in `.gitignore`, never committed, and deleted after the final demo.

### Planned model

The planned model is Qwen3 4B (`qwen3:4b` via Ollama), called with the OpenAI Python client through Ollama's OpenAI-compatible API. Model suitability, tool calling, and performance will be tested during Construction. Qwen3 8B (`qwen3:8b`) is the fallback on a laptop with more memory.

## MVP Features Out of Scope

- **Direct Bookings:** Users will not be able to book activities directly through the website as there are risks with payment information and an inability to coordinate with other websites.
- **Calendar Integration:** The itinerary will not be able to be directly exported to the calendar of the individual traveler.
- **Route Optimization:** The agent will not be able to give the best way of transport to each activity.
- Also out of scope: user accounts and saved profiles (only anonymous evaluation data and ratings are kept for KPI tracking), scraping TikTok or other social media, the personality quiz, and multi-city or group trips.

## Open Questions

- Is Qwen3 4B reliable enough at tool calling on an 8 GB laptop, or will the planned Qwen3 8B fallback be needed? What are Tavily's free-tier limits? What KPI targets are realistic for the MVP?
- How many questions should the chatbot ask, and how detailed should they be, to generate recommendations without being too time consuming?
- How do we evaluate whether the recommendations are sufficiently personalized, relevant, and feasible beyond the agreed KPI protocol?
- How should the itinerary be presented within the agreed scheduling and feedback constraints?

## Future scope

- How can we gather recommendations from social media so we have more versatility in response beyond web search? Social-media scraping remains outside the MVP.
