# In the Loop 2026 — Classic App

Continue editing Adele’s original Hex project in **Classic App** format: pinned markdown, HTML scoreboard, and Plotly tiles. Do not paste App.js. Do not switch back to Generative.

Open:

https://eu.hex.tech/n8n/hex/In-the-Loop-2026-Lead-Pipeline-Dashboard-034uXvUxSyRkGfmaNynnVx?projectView=app&view=app

## What the App should show

1. Title + **Conference visits** copy
2. **APP: Executive scoreboard** (conference tiles 1,269 / 426 / 916 / 39, then n8n website users for all / Europe / Germany)
3. **Day visit KPIs** and **Partner vs Eco bars**
4. Staff, CAB overlay, speakers (overlays on the same visit tiles)
5. Salesforce funnel / pipeline / GA4 in their own sections (commercial, not physical headcount)

Physical visits are people who **participated**: Fliplet door scans **union** Monday badge pickup **union** green YES on the CAB attendance sheet (`Incorrect no-show?` = YES). Partner Day **426** (391 door on 13 Oct + 35 non-staff badge desk on 12 Oct). Ecosystem Day **916** (878 door on 14 Oct + 38 of 40 green YES not already in the Eco door count). Staff 18 / 19 door scans sit inside. 324 people are in both day tiles. CAB **39** is an overlay, not extra headcount. Monday staff-only badge pickup (35) is not added.

Website tiles next to registration are GA4 page-view users on public n8n sites (**n8n.io, docs, community, blog, learn, plans**) for **1 Jun–9 Nov**. Europe is `geo_continent`, Germany is `geo_country`. **app.n8n.cloud** product usage is excluded. Digital section also has weekly n8n.io trends and YouTube/LinkedIn arrivals on n8n.io. There is no YouTube Analytics or LinkedIn Campaign Manager in the warehouse.

## If a new cell is missing from the App canvas

Hex cannot pin cells from the API. After a new scoreboard is added at the top of the notebook:

1. Stay on **App builder** (Classic).
2. **Add to app** (hexagon) on **APP: Executive scoreboard**, or **Outline → Reset layout → Use default layout**.
3. Remove `probe_` SQL tables from the App canvas if they appear (does not delete the notebook).
4. **Publish** when you want the `/app/.../latest` link. Workspace share is still **NONE** until you share it.

## Numbers

| Tile | Value | Source |
| --- | --- | --- |
| Registered | 1,269 | All participants · Paid + Free unique email |
| Partner Day visits | 426 | 391 door scans on 13 Oct + 35 badge pickup on 12 Oct |
| Ecosystem Day visits | 916 | 878 door scans on 14 Oct + 38 green YES |
| CAB overlay | 39 | All redeemed |
| Staff tickets | 113 | Fliplet Ticket family = Staff |
| Programme speakers | 116 | Speakers tab |
| Website users | 3.8M | GA4 users on public n8n sites, Jun–Nov |
| Europe users | 1.0M | `geo_continent` = Europe |
| Germany users | 219k | `geo_country` = Germany |
