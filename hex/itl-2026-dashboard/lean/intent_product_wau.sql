-- Weekly product WAU: UI-active people (not website visitors, not MCP-only).
-- activity_users grain is (user_id, day); dim_users is unique on user_id today.
SELECT
  DATE_TRUNC(DATE(a.day), WEEK(MONDAY)) AS week_start,
  COUNT(DISTINCT a.user_id) AS wau,
  COUNT(DISTINCT IF(
    LOWER(IFNULL(u.product_region, '')) IN ('europe', 'emea')
    AND LOWER(IFNULL(u.product_country, '')) != 'russia',
    a.user_id,
    NULL
  )) AS europe_wau,
  COUNT(DISTINCT IF(LOWER(IFNULL(u.product_country, '')) = 'germany', a.user_id, NULL)) AS germany_wau
FROM `n8n-telemetry.computed.activity_users` a
LEFT JOIN `n8n-telemetry.marts.dim_users` u
  ON a.user_id = u.user_id
WHERE a.has_ui_events = TRUE
  AND a.day >= TIMESTAMP('2026-06-01')
  AND a.day < TIMESTAMP('2026-11-09')
GROUP BY 1
ORDER BY 1
