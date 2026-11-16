# ITL 2026 app — four views on the existing Hex project

Stay on [In the Loop 2026 — Lead & Pipeline Dashboard](https://eu.hex.tech/n8n/hex/In-the-Loop-2026-Lead-Pipeline-Dashboard-034uXvUxSyRkGfmaNynnVx?projectView=app&view=app). Do not use the seven-cell scratch project.

Plotly CODE cells only show their first `display()`, so every visual is its own `APP: Chart ·` or ticket cell. Tabs: **Overview**, **Participation**, **Funnel**, **Intent**, **Feedback**, **Registration**. SQL / `Table ·` cells stay in Outline if you want to restyle a native table. No custom HTML (it vanishes in dark mode). Do not Reset layout.

## Summary

| Ask | Source | Status |
| --- | --- | --- |
| Participants per day | Fliplet visits (426 / 916) | Locked |
| Staff / speakers / CAB | Tickets 113, speakers 116, CAB 39 | Locked overlays |
| Attendance % | Came / tickets: 426/487 Partner, 916/1,205 Eco | Locked |
| Full funnel | Salesforce `lead_funnel` (`salesforce_bq.CampaignMember` + Opportunity) | Live from BQ; App Funnel chart is a 13 Nov snapshot so it does not NameError. Pin **APP: Event people funnel** if you still want 1,119 → 837 |
| SFDC lead reached | LeadHistory + ContactHistory `Status__c` + current `Lead.Status` / `Contact.Status__c` on ITL Free+Paid | Overview Funnel markdown tables + **APP: Funnel Chart** (segment chart and region chart as separate figures) + **APP: SFDC lead reached** SQL (wide STRING columns ENT/MM/SMB/DACH/…) |
| Ticket sales | In The Loop Registrations · Pacing (Detailed). Paid + Free, Expired/Cancelled excluded | Registration tab. **APP: Ticket sales daily / mix / vs goal** are Plotly visuals (bars+line, stacked area, branded table). Last real day 2026-10-10: 1,151 registrations, 1,043 unique people |
| Campaign / lead statuses | `CampaignMember.Status` on ITL/Eco/Partner/Meetings; current SFDC status from `fct_campaign_member_pipeline` | Pin **APP: Campaign member statuses** and **APP: Salesforce lead statuses** |
| Sourced vs influenced | `itl_sourced_influenced_opps` | Live |
| Expansion / partner / net new / closed | `pipeline_arr` + sourced list Type | Live |

## Attendance

| Ask | Source | Status |
| --- | --- | --- |
| People per day | Fliplet 426 / 916 | Locked |
| Region per day | Salesforce Account/Lead on Attended members | SQL |
| Sales segment per day | Salesforce `Sales_Segment__c` | SQL |
| Seniority | Title buckets on Salesforce Attended | SQL |
| Sessions | Fliplet Scans, User Game Scans, Session Feedback | Door scans 391/878; no named session-scan column |
| Meetings | [In The Loop_sales meetings](https://docs.google.com/spreadsheets/d/1IqHpjJ0mkhT9rxvMIa6fAdzC-5pzr2zLYi7uA3CSAgI) | 23 people on the sheet |
| Feedback | [shared Fliplet workbook](https://docs.google.com/spreadsheets/d/1ZGiFP8wgcpaFESOY7WuDSgwGdztCTivzmwdWK87JsrU) tabs Ecosystem Day Feedback Survey, Partner Day Feedback Survey, Session Feedback | Eco recommend 9.1/10 (n=43, NPS 72). Partner overall 9.1/10 (n=20; 3 Fillout tests dropped; 8.8/n=23 included tests). Session score 4.8/5 (n=62). Pin **APP: Ecosystem / Partner / Session** cells. |

## Funnel

| Ask | Source | Status |
| --- | --- | --- |
| Leads by category | CampaignMember Free/Paid + attendance groups | SQL |
| AI SDR vs humans | `fct_opportunities.first_meeting_source` (AI Handoff = Freddy) | SQL |
| Contacts per opportunity stage | ITL sourced+influenced joined to StageName | SQL |
| Closed won | Same list, Closed Won | SQL |
| Opportunity lists | `itl_sourced_influenced_opps` | Already in the project |

## Intent

| Ask | Source | Status |
| --- | --- | --- |
| Website overall, ITL week highlighted | GA4 n8n.io weekly users | SQL |
| Germany + Europe charts | GA4 geo on n8n.io | SQL |
| YouTube views + creations | `fct_youtube_video_daily_stats`, `dim_youtube_video` | SQL |
| Instance creations by type | `computed.instances` `deployment_type` × `acquired_at` | SQL |
| SEO / AEO keywords that week | Organic GSC / AEO **not in warehouse**. Paid Google Ads search terms exist | Paid terms only |
