-- ============================================================
-- K: Create progression_snapshots table
-- Run once (Cell A must have created the schema first).
-- Partitioned by snapshot_date for efficient 90-120 day ROI queries.
-- Safe to re-run (IF NOT EXISTS).
-- ============================================================
CREATE TABLE IF NOT EXISTS `n8n-telemetry.itl_2026_snapshots.progression_snapshots` (
  snapshot_date     DATE      NOT NULL OPTIONS(description='Date this snapshot was taken'),
  email             STRING    NOT NULL OPTIONS(description='Registrant email'),
  name              STRING,
  company           STRING,
  segment           STRING    OPTIONS(description='ENT/MM/SMB/Unknown'),
  is_partner        BOOL,
  day1              BOOL      OPTIONS(description='Partner Day registrant'),
  day2              BOOL      OPTIONS(description='Ecosystem Day registrant'),
  match_type        STRING    OPTIONS(description='contact | converted_lead | open_lead | domain_match | unmatched'),
  sfdc_lead_id      STRING,
  sfdc_contact_id   STRING,
  sfdc_account_id   STRING,
  opp_count         INT64,
  closed_won_count  INT64,
  total_net_new_arr FLOAT64   OPTIONS(description='Sum Net_New_ARR__c across matched opps'),
  won_net_new_arr   FLOAT64   OPTIONS(description='Net_New_ARR__c on Closed Won opps only'),
  created_at        TIMESTAMP NOT NULL
)
PARTITION BY snapshot_date
OPTIONS (
  description = 'Daily ITL 2026 registrant progression. Track from 2026-10-12 to ~2027-02-09 (120-day ROI window). One row per email per snapshot_date.'
)
