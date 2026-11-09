# ITL 2026 — Hex Dashboard SQL

SQL cells for the [ITL 2026 Hex dashboard](https://eu.hex.tech/n8n/hex/ITL-2026-Lead-Progression-Pipeline-Partner-Day-034uYCCFgBFrgyIxbmjAdB/draft/logic).

**Project ID:** `01a1bfe8-d19e-735f-8c30-ff695862715d`  
**BQ dataset:** `n8n-telemetry.itl_2026_snapshots`  
**BQ connection:** `BQ - n8n` (id `019ce681-e9fb-7002-ad50-b766bf65c6cf`)

## Run order

The cells must be run in alphabetical order on first use:

| Cell | File | Purpose | Run once? |
|------|------|---------|-----------|
| A | `A_create_itl_snapshots_schema.sql` | CREATE SCHEMA `n8n-telemetry.itl_2026_snapshots` | Yes |
| B1 | `B1_create_registrant_table_rows_1_320.sql` | CREATE TABLE + load rows 1–320 | Yes (re-run to refresh) |
| B2 | `B2_insert_registrant_rows_321_640.sql` | INSERT rows 321–640 | Yes (after B1) |
| B3 | `B3_insert_registrant_rows_641_960.sql` | INSERT rows 641–960 | Yes (after B2) |
| B4 | `B4_insert_registrant_rows_961_1279.sql` | INSERT rows 961–1279 | Yes (after B3) |
| C | `C_lead_funnel.sql` | Lead progression funnel | Live |
| D | `D_match_detail.sql` | Per-registrant SFDC match detail | Live |
| E | `E_pipeline_summary.sql` | Pipeline by type/stage with ARR | Live |
| F | `F_pipeline_detail.sql` | One row per opportunity | Live |
| G | `G_partner_day_detail.sql` | Partner Day breakdown by segment | Live |
| H | `H_partner_day_summary.sql` | Partner Day top-level summary | Live |
| I | `I_ga4_traffic_comparison.sql` | GA4 traffic: baseline, conference, post-week | Live |
| J | `J_ga4_itl_pages.sql` | ITL-related page views | Live |
| K | `K_create_snapshot_table.sql` | CREATE TABLE progression_snapshots (schema) | Yes |
| L | `L_insert_daily_snapshot.sql` | INSERT today's snapshot (idempotent) | Daily |
| M | `M_snapshot_history.sql` | Read snapshot progression history | Live |

## Data loading

### ⚠️ BQ write access required

The `BQ - n8n` Hex connection is **read-only**. Cells A, B1–B4, K, and L (DDL + DML) must be run from a context that has write access to `n8n-telemetry.itl_2026_snapshots`. Options:

1. **BigQuery Console**: Open `console.cloud.google.com/bigquery`, copy-paste each SQL file, run in order A → B1 → B2 → B3 → B4 → K.
2. **bq CLI**: `bq mk --dataset --location=EU n8n-telemetry:itl_2026_snapshots`, then `bq query --use_legacy_sql=false < B1_create_registrant_table_rows_1_320.sql`, etc.
3. **New writable Hex connection**: Create a connection with a service account that has `roles/bigquery.dataEditor` on the `itl_2026_snapshots` dataset. Then use that connection for cells A, B1–B4, K, L.

After creating the dataset, grant `roles/bigquery.dataViewer` (or `dataEditor`) on `itl_2026_snapshots` to the service account used by `BQ - n8n` so analysis cells C–J, M can read the data.

After running cell **B1** (which uses `CREATE OR REPLACE TABLE`), cells B2–B4 must run in order. If you want to re-load all data from scratch, re-run B1 first (it drops and recreates the table), then B2, B3, B4.

The registrant data comes from the n8n metrics webhook (authenticated). It reflects the state on **2026-11-09**: 1,279 registrants (Paid + Free tickets, test accounts excluded).

## Assumptions

1. **Product_Interest__c filter NOT applied.** The pipeline includes all Opportunity types (New Business, Expansion) regardless of product interest. Add `AND o.Product_Interest__c LIKE '%Enterprise%'` to restrict to Enterprise — confirm scope before enabling.

2. **Currency.** `Amount_EUR__c` (FLOAT64) is used for the EUR column; this is an SFDC-calculated EUR conversion of the opportunity amount. ARR fields (`New_Business_ARR__c`, `Expansion_ARR__c`, `Net_New_ARR__c`, etc.) are in the SFDC org currency (EUR for n8n) and not separately converted.

3. **Domain fallback.** Registrants with no email match in Lead or Contact are matched to Accounts by normalizing `Account.Website` (strip `https://`, `www.`, path) against the registrant's email domain. This is a heuristic and may produce false positives for large shared domains (e.g., gmail.com is excluded naturally because no Account has that website).

4. **Opportunity date range.** No date filter on opportunities — all open/closed opps linked to registrant accounts are included, regardless of creation date. This shows total account pipeline value, not event-attributed pipeline. To scope to event-attributed opps, add `AND o.CreatedDate >= '2026-10-12'`.

5. **GA4 city column.** The `int_google_analytics__events_unnested` table does not have a `city` column. Berlin traffic analysis requires a different GA4 export (raw `events_*` tables with the geo nested field). Flagged as a placeholder in the dashboard.

6. **LinkedIn activity and livestream views.** No connector available. These are marked as placeholders. Required exports: LinkedIn Page Analytics CSV + livestream platform metrics.

7. **Snapshot idempotency.** Cell L (insert snapshot) checks for `CURRENT_DATE()` in the existing snapshots and skips if already present. Schedule it via Hex's project schedule for daily runs.

## Partner Day definition

- **Partner invitee**: registrant whose `best_ticket` contains "partner" (case-insensitive) → `is_partner = TRUE`
- **Partner Day only**: `is_partner AND day1 AND NOT day2`
- **Both days**: `is_partner AND day1 AND day2`
- **Ecosystem only**: `NOT is_partner AND day2`

Counts (from webhook, 2026-11-09):
- Partner only: 63
- Both days: 229
- Ecosystem only: 984 (non-partner day2)
- Total partner invitees: 292
