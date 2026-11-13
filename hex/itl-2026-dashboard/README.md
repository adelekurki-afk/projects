# In the Loop 2026

Stay on the existing Hex Classic App. Do not use the seven-cell scratch project.

**App:** https://eu.hex.tech/n8n/hex/In-the-Loop-2026-Lead-Pipeline-Dashboard-034uXvUxSyRkGfmaNynnVx?projectView=app&view=app

**Notebook:** https://eu.hex.tech/n8n/hex/In-the-Loop-2026-Lead-Pipeline-Dashboard-034uXvUxSyRkGfmaNynnVx/draft/logic

The Classic App has three tabs. The four views sit on those tabs — they are not four extra tabs (the API cannot add one):

| App tab | View |
| --- | --- |
| **Overview** | Summary at the top, **Funnel** under it. SFDC lead progression is already in **APP: Funnel Chart** |
| **Participation** | **Attendance**. Pin per-survey cells (**Ecosystem Day**, **Partner Day**, **Session feedback**) here |
| **Intent** | Website / YouTube / paid search |

After SQL/CODE edits, **Run all** then refresh the App. Markdown updates without Run all. Do not Reset layout — that dumps every SQL probe onto the canvas.

## Summary

Same shape as Paid Some LinkedIn: a Result paragraph, then Hex-native charts and tables (Plotly with transparent paper so dark mode stays readable — no custom HTML). Fliplet visits 426 / 916 / 1,018, staff 113, speakers 116, CAB 39, attendance 87% Partner / 76% Eco of tickets. Salesforce funnel is live from BigQuery (`salesforce_bq` CampaignMember / Opportunity). Sourced vs influenced. New Business vs Expansion (no Partner-typed opps).

## Attendance

`APP: Participation` is self-contained Plotly (no SQL names from later in the notebook). App runs top-to-bottom; a forward reference was red-erroring that cell.

Locked Fliplet headcount, then Salesforce Attended mix (region, segment, seniority — a different clock). Fliplet door scans 391 / 878. Zone game scans. n8n sales meetings sheet 23 people. Fliplet booked meetings 1,076. Per-survey cells at the bottom of the notebook: Ecosystem recommend 9.1/10 (n=43, NPS 72), Partner overall 9.1/10 (n=20 after dropping 3 Fillout tests), session score 4.8/5 (n=62). Hex API cannot pin them — Add to app. No named session-scan column.

## Funnel

Salesforce **lead progression** is Lead/Contact status on ITL Free+Paid (1,102 → 314 New → 269 Working → 177 Qualified). It is written into **APP: Funnel Chart** and the Funnel Result already on Overview — Hex cannot pin the extra SQL cells. Event people 1,119 → 837 stays as the second funnel on that same chart. AI SDR vs humans, opportunity stages, sourced vs influenced stay as they were.

## Intent

Weekly n8n.io users with conference week 12–18 Oct highlighted: worldwide, then Europe and Germany as separate lines. YouTube views (from 1 Jul) and videos published. Acquired instances by `deployment_type`. Paid Google Ads search terms that week (organic SEO / AEO is not in the warehouse). No Common Room table for social posts.

Physical visits are Fliplet. Salesforce registered is not 1,269. Salesforce Attended is not 426 / 916.

See `VIEW_SPEC.md` for source and status of each ask.
