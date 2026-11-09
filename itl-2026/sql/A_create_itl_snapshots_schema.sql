-- ⚠️  PREREQUISITE: Run this SQL with a GCP account that has bigquery.datasets.create on n8n-telemetry.
--
-- The 'BQ - n8n' Hex connection is READ-ONLY and cannot create datasets.
-- Options:
--   1. Run directly in BigQuery Console (console.cloud.google.com/bigquery)
--      with a GCP admin account or any account with bigquery.datasets.create on n8n-telemetry.
--   2. Create a Hex data connection with a service account that has:
--        - bigquery.datasets.create on project n8n-telemetry
--        - bigquery.tables.create + bigquery.tables.updateData on the itl_2026_snapshots dataset
--   3. Run via bq CLI: bq mk --dataset --location=EU n8n-telemetry:itl_2026_snapshots
--
-- After creating the dataset, also grant BigQuery Data Editor to the service account
-- used by the 'BQ - n8n' Hex connection so cells B1-B4, K, and L can write to it.
-- ============================================================
CREATE SCHEMA IF NOT EXISTS `n8n-telemetry.itl_2026_snapshots`
OPTIONS (description = 'ITL 2026 event analytics: registrants and progression snapshots', location = 'EU')