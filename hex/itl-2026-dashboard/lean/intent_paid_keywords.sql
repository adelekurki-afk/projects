-- Paid Google Ads search terms in the conference week. Not organic SEO / AEO
-- (Google Search Console is not in this warehouse).
SELECT
  search_term,
  SUM(impressions) AS impressions,
  SUM(clicks) AS clicks,
  ROUND(SUM(cost), 2) AS cost
FROM `n8n-telemetry.marts.fct_google_ads_search_term_daily`
WHERE event_date BETWEEN '2026-10-12' AND '2026-10-18'
GROUP BY search_term
ORDER BY impressions DESC
LIMIT 25
