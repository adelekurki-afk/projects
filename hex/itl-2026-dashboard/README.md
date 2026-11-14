# In the Loop 2026

Stay on the existing Hex Classic App. Do not use the seven-cell scratch project.

**App:** https://eu.hex.tech/n8n/hex/In-the-Loop-2026-Lead-Pipeline-Dashboard-034uXvUxSyRkGfmaNynnVx?projectView=app&view=app

**Notebook:** https://eu.hex.tech/n8n/hex/In-the-Loop-2026-Lead-Pipeline-Dashboard-034uXvUxSyRkGfmaNynnVx/draft/logic

Dashboard tables live in **CODE cells labeled `Table · …` at the top of the notebook**. The App Outline **Table** filter only lists Hex **Table display** cells (Add cell → Table). SQL queries, notebook sections, and Python cells do not show there, and the API cannot create Table display cells.

Run the `Table ·` cells, then **Add cell → Table** and pick the dataframe (`visits`, `pipeline_summary`, `role_mix`, …). Those Table cells appear in Outline. Drag onto a tab, then use the chart icon to restyle as a bar, line, or stacked area. The three Registration cards are Charts — search `Table ·` with the type filter cleared if you want the Python cells themselves.

| App tab | Pin these from Outline (`Table ·`) |
| --- | --- |
| **Overview** | Visits, Pipeline summary, Opportunities |
| **Participation** | Role mix, Attendance by region, Also on site, Staff by crew, Speakers by day |
| **Registration** | Ticket sales daily / mix / vs goal (already pinned) |
| **Funnel** | SFDC lead reached, Event people funnel, Sourced vs influenced |
| **Intent** | Weekly n8n.io users, YouTube views, Paid search terms |
| **Feedback** | Eco programme parts, Eco operations, Eco who answered, Partner tracks, Session ratings |

After SQL/CODE edits, **Run all** then refresh the App. Markdown updates without Run all. Do not Reset layout — that dumps every SQL probe onto the canvas.

## Summary

Same shape as Paid Some LinkedIn: a Result paragraph, then Hex-native charts and tables (Plotly with transparent paper so dark mode stays readable — no custom HTML). Fliplet visits 426 / 916 / 1,018, staff 113, speakers 116, CAB 39, attendance 87% Partner / 76% Eco of tickets. Salesforce funnel is live from BigQuery (`salesforce_bq` CampaignMember / Opportunity). Sourced vs influenced. New Business vs Expansion (no Partner-typed opps).

## Attendance

`APP: Participation` is self-contained Plotly (no SQL names from later in the notebook). App runs top-to-bottom; a forward reference was red-erroring that cell.

Locked Fliplet headcount, then Salesforce Attended mix (region, segment, seniority — a different clock). Fliplet door scans 391 / 878. Zone game scans. n8n sales meetings sheet 23 people. Fliplet booked meetings 1,076. Per-survey cells at the bottom of the notebook: Ecosystem recommend 9.1/10 (n=43, NPS 72), Partner overall 9.1/10 (n=20 after dropping 3 Fillout tests), session score 4.8/5 (n=62). Hex API cannot pin them — Add to app. No named session-scan column.

## Funnel

Salesforce **lead reached** is Lead/Contact status on ITL Free+Paid (1,102 people; 314 New, 269 Working, 177 Qualified), plus the same statuses by sales segment and region as **two charts**, not one combined figure. It is written into **APP: Funnel Chart** on Overview. Ticket sales (Paid + Free) lives on the **Registration** tab: 1,151 registrations / 1,043 unique people vs an 850 unique-people goal. Event people 1,119 → 837 stays as the CampaignMember funnel on Overview. AI SDR vs humans, opportunity stages, sourced vs influenced stay as they were.

## Intent

Weekly n8n.io users with conference week 12–18 Oct highlighted: worldwide, then Europe and Germany as separate lines. YouTube views (from 1 Jul) and videos published. Acquired instances by `deployment_type`. Paid Google Ads search terms that week (organic SEO / AEO is not in the warehouse). No Common Room table for social posts.

Physical visits are Fliplet. Salesforce registered is not 1,269. Salesforce Attended is not 426 / 916.

See `VIEW_SPEC.md` for source and status of each ask.
