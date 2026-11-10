# In the Loop 2026 — Classic App

Continue editing Adele’s original Hex project in **Classic App** format: pinned markdown, HTML scoreboard, and Plotly tiles. Do not paste App.js. Do not switch back to Generative.

Open:

https://eu.hex.tech/n8n/hex/In-the-Loop-2026-Lead-Pipeline-Dashboard-034uXvUxSyRkGfmaNynnVx?projectView=app&view=app

## What the App should show

1. Title + **Conference visits** copy
2. **APP: Executive scoreboard** (HTML tiles: 1,269 / 391 / 878 / 39)
3. **Day visit KPIs** and **Partner vs Eco bars**
4. Staff, CAB overlay, speakers (overlays on the same door scans)
5. Salesforce funnel / pipeline / GA4 in their own sections (commercial, not physical headcount)

Physical visits stay Fliplet: Partner Day **391** (13 Oct) · Ecosystem Day **878** (14 Oct). 272 people visited both days, so they appear in both tiles. CAB **39** is an overlay, not extra headcount.

## If a new cell is missing from the App canvas

Hex cannot pin cells from the API. After a new scoreboard is added at the top of the notebook:

1. Stay on **App builder** (Classic).
2. **Add to app** (hexagon) on **APP: Executive scoreboard**, or **Outline → Reset layout → Use default layout**.
3. Remove `probe_` SQL tables from the App canvas if they appear (does not delete the notebook).
4. **Publish** when you want the `/app/.../latest` link. Workspace share is still **NONE** until you share it.

## Numbers

| Tile | Value | Source |
| --- | --- | --- |
| Registered | 1,269 | Fliplet Paid + Free, unique email |
| Partner Day visits | 391 | 13 Oct door scans |
| Ecosystem Day visits | 878 | 14 Oct door scans |
| CAB overlay | 39 | All redeemed |
| Staff tickets | 113 | Fliplet Ticket family = Staff |
| Programme speakers | 116 | Speakers tab |
