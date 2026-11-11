# In the Loop 2026 — Classic App

Continue editing Adele’s original Hex project in **Classic App** format: pinned markdown, HTML scoreboard, and Plotly tiles. Do not paste App.js. Do not switch back to Generative.

Open:

https://eu.hex.tech/n8n/hex/In-the-Loop-2026-Lead-Pipeline-Dashboard-034uXvUxSyRkGfmaNynnVx?projectView=app&view=app

## What the App should show

Keep **APP: Executive scoreboard** as the App. It is one HTML dashboard:

1. **Overview** — conference visits (1,269 / 426 / 916 / 1,018), Salesforce conversion (1,118 → 835 → 20 → 57 → 6), opportunities (€2.42M / 27 opps)
2. **Participation** — both-day overlap, staff / speakers / CAB overlays
3. **Site intent** — n8n websites Germany & Europe, conference-week Berlin / CTA / trials
4. **Partner Day** — how 426 is built vs Ecosystem Day 916

If other blocks are still on the canvas, hover them → **⋯ → Remove from App**. Do **not** Reset layout (that dumps SQL tables). Do not pin `ga4_web_*` SQL cells.

Physical visits are people who **participated**: Fliplet door scans **union** Monday badge pickup **union** green YES on the CAB attendance sheet (`Incorrect no-show?` = YES). Partner Day **426** (391 door on 13 Oct + 35 non-staff badge desk on 12 Oct). Ecosystem Day **916** (878 door on 14 Oct + 38 of 40 green YES not already in the Eco door count). Staff 18 / 19 door scans sit inside. 324 people are in both day tiles. CAB **39** is an overlay, not extra headcount. Monday staff-only badge pickup (35) is not added.

Salesforce registered **1,118** is not Fliplet **1,269**. Salesforce Attended **835** is not 426 / 916.

Website tiles are GA4 page-view users on public n8n sites (**n8n.io, docs, community, blog, learn, plans**) for **1 Jun–9 Nov**. Europe is `geo_continent`, Germany is `geo_country`. **app.n8n.cloud** product usage is excluded. There is no YouTube Analytics or LinkedIn Campaign Manager in the warehouse.

**Publish** when you want the `/app/.../latest` link.

## Numbers

| Tile | Value | Source |
| --- | --- | --- |
| Registered | 1,269 | All participants · Paid + Free unique email |
| Partner Day visits | 426 | 391 door scans on 13 Oct + 35 badge pickup on 12 Oct |
| Ecosystem Day visits | 916 | 878 door scans on 14 Oct + 38 green YES |
| Unique people | 1,018 | 426 + 916 − 324 both days |
| CAB overlay | 39 | All redeemed |
| Staff tickets | 113 | Fliplet Ticket family = Staff |
| Programme speakers | 116 | Speakers tab |
| Salesforce registered | 1,118 | CampaignMember Free/Paid |
| Pipeline | €2.42M | NB + Expansion from 12 Oct |
| Website users | 3.8M | GA4 users on public n8n sites, Jun–Nov |
| Europe users | 1.0M | `geo_continent` = Europe |
| Germany users | 219k | `geo_country` = Germany |
