# ITL 2026 (In the Loop) — Registrant Enrichment

## Overview

Fliplet export (13 tabs) → enriched registrant CSV with cross-tab joins → BigQuery + Hex dashboard.

**Hex dashboard:** https://eu.hex.tech/n8n/hex/In-the-Loop-2026-Lead-Pipeline-Dashboard-034uXvUxSyRkGfmaNynnVx/draft/logic

---

## Files

| File | Description |
|------|-------------|
| `itl_2026_registrants_enriched.csv` | Full 1,269-row enriched dataset (all Fliplet tabs joined) |
| `itl_2026_full_bq_query.sql` | Full 1,269-row compact inline BigQuery SQL (use this to load data inline in Hex/BQ) |

---

## Data Model

### Fliplet Cross-Tab Joins

The raw Fliplet export has 13 tabs. Key linkage:
- `Purchases.User Unique ID` = `Scans.UserID` = `Session Feedback.UserID` = `Booked Meetings.BookedByID`

### Enriched Columns

| Column | Description |
|--------|-------------|
| `email` | Registrant email (from Purchases tab) |
| `name` | Full name |
| `company` | Company name |
| `country` | Country |
| `ticket_type` | Early Bird / General / Partner Day + Ecosystem Day / etc. |
| `partner_type` | Ambassador / Strategic Partner / Node Partner / Expert Partner |
| `day1` | Attended Partner Day (Day 1) = True/False |
| `day2` | Attended Ecosystem Day (Day 2) = True/False |
| `has_badge_scan` | Scanned badge at any session = True/False |
| `booked_meeting_count` | Number of Booked Meetings |
| `has_lead_note` | Has event lead note = True/False |
| `is_exhibitor` | Is listed as exhibitor = True/False |
| `fliplet_uid` | Fliplet User Unique ID (for cross-reference) |

### Key Stats (from 1,269 registrants)
- Badge scanned (physically attended): 981 (77%)
- Booked meetings: 480 with ≥1 meeting
- Lead notes captured: 47
- Partner Day attendees: ~160+

---

## Loading into BigQuery

To run SFDC enrichment against the full 1,269-row dataset:

```bash
# Load enriched CSV into BigQuery (EU region)
bq load \
  --location=EU \
  --source_format=CSV \
  --skip_leading_rows=1 \
  --schema=email:STRING,name:STRING,company:STRING,country:STRING,ticket_type:STRING,partner_type:STRING,day1:BOOLEAN,day2:BOOLEAN,has_badge_scan:BOOLEAN,booked_meeting_count:INTEGER,has_lead_note:BOOLEAN,is_exhibitor:BOOLEAN,fliplet_uid:STRING \
  n8n-telemetry:itl_2026_snapshots.registrants \
  ./itl_2026_registrants_enriched.csv
```

Then update the Hex dashboard cells to query:
```sql
SELECT * FROM `n8n-telemetry.itl_2026_snapshots.registrants`
```

---

## Hex Dashboard Cells

| Cell Name | Cell ID | Purpose |
|-----------|---------|---------|
| `registrants` | `01a1bfdf-7e47-7033-854d-a9b4b95334d4` | 250-row sample of registrant data |
| `sfdc_account_enrichment` | `01a1c073-4619-72fc-8f83-6730f947eb2c` | Segment breakdown: ENT/MM/SMB/Unknown |
| `lead_funnel` | `01a1bfe3-9664-7625-8434-3eb44d19d6d7` | 5-stage funnel: registered → attended → SFDC match → opp → closed won |

---

## SFDC Match Strategy

1. **Email match to Lead** (`salesforce_bq.Lead.Email`)
2. **Email match to Contact** (`salesforce_bq.Contact.Email`) → Account
3. **Domain fallback** (`salesforce_bq.Account.Website_Domain__c`) for corporate emails

Domain exclusions: `gmail.com`, `yahoo.com`, `hotmail.com`, `outlook.com` and other free email providers.

---

## Results (from 70-row sub-sample)

### Segment Breakdown
| Segment | Count | Attended | Booked Mtgs | SFDC Accounts |
|---------|-------|----------|-------------|---------------|
| Unknown | 40 (55.6%) | 93% | 21 | 1 |
| ENT | 15 (20.8%) | 93% | 10 | 7 |
| MM | 12 (16.7%) | 92% | 6 | 10 |
| SMB | 5 (6.9%) | 100% | 3 | 0 |

### Lead Funnel (71-row sample)
| Stage | Count | % of Registered |
|-------|-------|-----------------|
| Registered | 71 | 100% |
| Physically Attended | 66 | 93% |
| Matched in SFDC | 15 | 21% |
| Account with Opp (≥ Oct 12) | 0 | 0% |
| Closed Won | 0 | 0% |

> **Note:** The 0 for opps/closed won is expected in this small sample biased toward partner/ecosystem attendees.
> With the full 1,269 row dataset loaded into BQ, re-run the cells for accurate pipeline attribution.
