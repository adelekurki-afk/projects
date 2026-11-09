-- ============================================================
-- GA4 WEBSITE TRAFFIC: 3-week comparison on n8n.io
-- event_timestamp is TIMESTAMP type; event_date is DATE type
-- Baseline:    2026-10-05 to 2026-10-11
-- Conference:  2026-10-12 to 2026-10-18 (ITL week)
-- Post-week:   2026-10-19 to 2026-10-25
-- NOTE: city column not available in this table — Berlin traffic
--       requires a different GA4 export (see assumptions).
-- ============================================================
SELECT
  CASE
    WHEN event_date BETWEEN '2026-10-05' AND '2026-10-11' THEN '1_Baseline (Oct 5-11)'
    WHEN event_date BETWEEN '2026-10-12' AND '2026-10-18' THEN '2_Conference (Oct 12-18)'
    WHEN event_date BETWEEN '2026-10-19' AND '2026-10-25' THEN '3_Post-Week (Oct 19-25)'
  END AS period,
  COUNT(DISTINCT user_pseudo_id)       AS unique_users,
  COUNTIF(event_name = 'page_view')    AS page_views,
  COUNTIF(event_name = 'session_start') AS sessions,
  COUNT(*)                              AS total_events
FROM `n8n-telemetry.intermediate.int_google_analytics__events_unnested`
WHERE hostname = 'n8n.io'
  AND event_date BETWEEN '2026-10-05' AND '2026-10-25'
GROUP BY 1
HAVING period IS NOT NULL
ORDER BY 1
