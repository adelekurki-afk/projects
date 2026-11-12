SELECT
  DATE_TRUNC(event_date, WEEK(MONDAY)) AS week_start,
  COUNT(DISTINCT user_pseudo_id) AS n8n_users,
  COUNTIF(LOWER(IFNULL(geo_city,'')) = 'berlin') AS berlin_events
FROM `n8n-telemetry.intermediate.int_google_analytics__events_unnested`
WHERE hostname = 'n8n.io'
  AND event_date BETWEEN '2026-06-01' AND '2026-11-08'
GROUP BY week_start
ORDER BY week_start
