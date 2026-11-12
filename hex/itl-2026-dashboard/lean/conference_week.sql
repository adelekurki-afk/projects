-- GA4: n8n.io traffic and signup-proxy signals by week (Baseline / Conference / Post).
-- No 'sign_up' event exists; using the following as signup proxies:
--   click_get_started_buttons: CTA clicks on n8n.io (closest to intent)
--   selfhost_signal: self-host deployment signals
--   selfhost_business_plan_start_free_trial_: trial starts
--   sales_lead_form_thankyou: completed sales form submissions
-- geo_city is well-populated (~93% of events) and reliable for Berlin filter.

WITH

base AS (
  SELECT
    event_date,
    event_name,
    geo_city,
    geo_country,
    user_pseudo_id,
    ga_session_id,
    CASE
      WHEN event_date BETWEEN '2026-10-05' AND '2026-10-11' THEN 'Baseline (5-11 Oct)'
      WHEN event_date BETWEEN '2026-10-12' AND '2026-10-18' THEN 'Conference (12-18 Oct)'
      WHEN event_date BETWEEN '2026-10-19' AND '2026-10-25' THEN 'Post-week (19-25 Oct)'
    END AS week_label
  FROM `n8n-telemetry.intermediate.int_google_analytics__events_unnested`
  WHERE hostname = 'n8n.io'
    AND event_date BETWEEN '2026-10-05' AND '2026-10-25'
)

SELECT
  week_label,
  COUNT(*)                                                     AS total_events,
  COUNT(DISTINCT user_pseudo_id)                               AS unique_users,
  COUNT(DISTINCT ga_session_id)                                AS sessions,
  -- Signup proxy signals
  COUNTIF(event_name = 'click_get_started_buttons')           AS cta_clicks,
  COUNTIF(event_name = 'selfhost_signal')                     AS selfhost_signals,
  COUNTIF(event_name = 'selfhost_business_plan_start_free_trial_') AS trial_starts,
  COUNTIF(event_name = 'sales_lead_form_thankyou')            AS sales_form_completions,
  -- Berlin & Germany
  COUNTIF(LOWER(geo_city) = 'berlin')                         AS berlin_events,
  COUNTIF(LOWER(geo_country) = 'germany')                     AS germany_events
FROM base
WHERE week_label IS NOT NULL
GROUP BY week_label
ORDER BY
  CASE week_label
    WHEN 'Baseline (5-11 Oct)'       THEN 1
    WHEN 'Conference (12-18 Oct)'    THEN 2
    WHEN 'Post-week (19-25 Oct)'     THEN 3
  END