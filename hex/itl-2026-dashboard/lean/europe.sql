SELECT
  geo_country AS country,
  COUNT(DISTINCT user_pseudo_id) AS users,
  COUNT(*) AS page_views
FROM `n8n-telemetry.intermediate.int_google_analytics__events_unnested`
WHERE event_date BETWEEN '2026-06-01' AND '2026-11-09'
  AND event_name = 'page_view'
  AND LOWER(IFNULL(geo_continent, '')) = 'europe'
  AND LOWER(IFNULL(geo_country, '')) != 'russia'
  AND hostname IN (
    'n8n.io',
    'docs.n8n.io',
    'community.n8n.io',
    'blog.n8n.io',
    'learn.n8n.io',
    'plans.n8n.io'
  )
GROUP BY geo_country
ORDER BY users DESC
LIMIT 8
