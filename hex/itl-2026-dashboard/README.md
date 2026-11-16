# In the Loop 2026

Stay on the existing Hex Classic App. Do not use the seven-cell scratch project.

**App:** https://eu.hex.tech/n8n/hex/In-the-Loop-2026-Lead-Pipeline-Dashboard-034uXvUxSyRkGfmaNynnVx?projectView=app&view=app

**Notebook:** https://eu.hex.tech/n8n/hex/In-the-Loop-2026-Lead-Pipeline-Dashboard-034uXvUxSyRkGfmaNynnVx/draft/logic

**Visuals first.** Each Plotly CODE cell is one figure (`APP: Ticket sales …` and `APP: Chart · …`). Classic App only shows the first `display()`. Filter Outline to **Chart** and drag those cells onto a tab. SQL / `Table ·` cells stay available if you want to restyle a native table.

| App tab | Pin these from Outline (Chart) |
| --- | --- |
| **Overview** | Event people funnel, Pipeline mix, SFDC Lead vs Contact, SFDC by sales segment, SFDC by region |
| **Participation** | Attendance KPIs, How visits are built, Who came which days, Floor scans, Role mix, Staff by crew, Speakers by day |
| **Registration** | **APP: Ticket sales daily / mix / vs goal** (already on the tab) |
| **Funnel** | **Lead to closed**, Event people funnel, SFDC Lead vs Contact, SFDC by sales segment / region |
| **Intent** | Website visitors and product users (worldwide + Europe/Germany), YouTube views, Paid search |
| **Feedback** | Eco recommend, Eco operations, Partner Day overall, Session scores |

After SQL/CODE edits, **Run all** then refresh the App. Markdown updates without Run all. Do not Reset layout — that dumps every SQL probe onto the canvas.

## Summary

Same shape as Paid Some LinkedIn: a Result paragraph, then Hex-native charts and tables (Plotly with transparent paper so dark mode stays readable — no custom HTML). Fliplet visits 426 / 916 / 1,018, staff 113, speakers 116, CAB 39, attendance 87% Partner / 76% Eco of tickets. Salesforce funnel is live from BigQuery (`salesforce_bq` CampaignMember / Opportunity). Sourced vs influenced. New Business vs Expansion (no Partner-typed opps).

## Attendance

`APP: Participation` is self-contained Plotly (no SQL names from later in the notebook). App runs top-to-bottom; a forward reference was red-erroring that cell.

Locked Fliplet headcount, then Salesforce Attended mix (region, segment, seniority — a different clock). Fliplet door scans 391 / 878. Zone game scans. n8n sales meetings sheet 23 people. Fliplet booked meetings 1,076. Per-survey cells at the bottom of the notebook: Ecosystem recommend 9.1/10 (n=43, NPS 72), Partner overall 9.1/10 (n=20 after dropping 3 Fillout tests), session score 4.8/5 (n=62). Hex API cannot pin them — Add to app. No named session-scan column.

## Funnel

Salesforce **lead reached** is Lead/Contact status on ITL Free+Paid (1,102 people; 314 New, 269 Working, 177 Qualified), plus the same statuses by sales segment and region as **two charts**, not one combined figure. It is written into **APP: Funnel Chart** on Overview. Ticket sales (Paid + Free) lives on the **Registration** tab: 1,151 registrations / 1,043 unique people vs an 850 unique-people goal. Event people 1,119 → 837 stays as the CampaignMember funnel on Overview. AI SDR vs humans, opportunity stages, sourced vs influenced stay as they were.

## Intent

Website visitors are GA4 distinct `user_pseudo_id` on n8n.io. Product users are weekly UI-active people in `computed.activity_users` (`has_ui_events`). Conference week 12–18 Oct is highlighted. Worldwide is its own chart; Europe and Germany share one chart per metric. YouTube views (from 1 Jul) and videos published. Acquired instances by `deployment_type`. Paid Google Ads search terms that week (organic SEO / AEO is not in the warehouse).

Physical visits are Fliplet. Salesforce registered is not 1,269. Salesforce Attended is not 426 / 916.

See `VIEW_SPEC.md` for source and status of each ask.
