-- People funnel. Pin as APP: Lead progression. Depends on lead_funnel.
SELECT
  stage,
  count AS people,
  pct_of_registered
FROM lead_funnel
