-- ============================================================
-- SNAPSHOT HISTORY: progression chart data
-- Compare matched/opp/won counts across snapshot dates
-- ============================================================
SELECT
  snapshot_date,
  COUNT(*)                                   AS total_registrants,
  COUNTIF(match_type != 'unmatched')         AS sfdc_matched,
  COUNTIF(opp_count > 0)                     AS has_opportunity,
  COUNTIF(closed_won_count > 0)              AS has_closed_won,
  SUM(total_net_new_arr)                     AS total_pipeline_arr,
  SUM(won_net_new_arr)                       AS total_won_arr
FROM `n8n-telemetry.itl_2026_snapshots.progression_snapshots`
GROUP BY snapshot_date
ORDER BY snapshot_date