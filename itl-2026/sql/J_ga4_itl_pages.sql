-- ============================================================
-- ITL PAGE VIEWS: event-related pages + post-event content
-- Uses event_date (DATE) for filtering — event_timestamp not needed
-- ============================================================
SELECT
  CASE
    WHEN event_date BETWEEN '2026-10-05' AND '2026-10-11' THEN '1_Baseline'
    WHEN event_date BETWEEN '2026-10-12' AND '2026-10-18' THEN '2_Conference'
    WHEN event_date BETWEEN '2026-10-19' AND '2026-10-25' THEN '3_Post-Week'
  END AS period,
  REGEXP_REPLACE(page_location, r'\?.*$', '') AS page_path_clean,
  COUNT(DISTINCT user_pseudo_id)       AS unique_users,
  COUNT(*)                             AS total_views
FROM `n8n-telemetry.intermediate.int_google_analytics__events_unnested`
WHERE hostname = 'n8n.io'
  AND event_name = 'page_view'
  AND event_date BETWEEN '2026-10-05' AND '2026-10-25'
  AND (
    LOWER(page_location) LIKE '%in-the-loop%'
    OR LOWER(page_location) LIKE '%intheloop%'  -- pragma: allowlist secret
    OR LOWER(page_location) LIKE '%blog%2026%'
    OR LOWER(page_location) LIKE '%webinar%'
    OR LOWER(page_location) LIKE '%recap%'
    OR LOWER(page_location) LIKE '%itl%'
  )
GROUP BY 1, 2
HAVING period IS NOT NULL
ORDER BY 1, total_views DESC
