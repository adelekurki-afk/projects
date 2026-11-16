-- ITL Free+Paid people: Lead → meeting booked → opportunity → pipeline opportunity → closed.
-- Meeting = CampaignMember Status = Meeting Booked on 701cj00001MqzF9AAJ.
-- Opportunity = NB/Expansion created on/after 12 Oct 2026, not duplicate/disqualified.
-- Pipeline opportunity = int_opportunities.is_pipeline_opportunity (Value Workshop and later).
-- Closed = is_won.
WITH registered AS (
  SELECT
    LOWER(TRIM(email)) AS email,
    ANY_VALUE(NULLIF(account_id, '')) AS account_id
  FROM `n8n-telemetry.marts.fct_campaign_member_pipeline`
  WHERE campaign_id = '701cj0000157ynMAAQ'
    AND member_status IN ('Free', 'Paid')
    AND email IS NOT NULL
  GROUP BY 1
),
meeting AS (
  SELECT DISTINCT LOWER(TRIM(email)) AS email
  FROM `n8n-telemetry.marts.fct_campaign_member_pipeline`
  WHERE campaign_id = '701cj00001MqzF9AAJ'
    AND member_status = 'Meeting Booked'
    AND email IS NOT NULL
),
opps AS (
  SELECT
    salesforce_account_id AS account_id,
    LOGICAL_OR(is_pipeline_opportunity) AS is_pipeline_opportunity,
    LOGICAL_OR(is_won) AS is_won
  FROM `n8n-telemetry.intermediate.int_opportunities`
  WHERE opportunity_type IN ('New Business', 'Expansion')
    AND DATE(created_at) >= '2026-10-12'
    AND IFNULL(is_duplicate, FALSE) = FALSE
    AND IFNULL(is_disqualified, FALSE) = FALSE
  GROUP BY 1
),
joined AS (
  SELECT
    r.email,
    m.email IS NOT NULL AS had_meeting,
    o.account_id IS NOT NULL AS has_opp,
    IFNULL(o.is_pipeline_opportunity, FALSE) AS has_pipeline_opp,
    IFNULL(o.is_won, FALSE) AS is_won
  FROM registered r
  LEFT JOIN meeting m ON m.email = r.email
  LEFT JOIN opps o ON o.account_id = r.account_id
)
SELECT n, stage, value AS people, ROUND(100.0 * value / MAX(value) OVER (), 1) AS pct_of_lead
FROM (
  SELECT 1 AS n, 'Lead' AS stage, COUNT(*) AS value FROM joined
  UNION ALL
  SELECT 2, 'Meeting booked', COUNTIF(had_meeting) FROM joined
  UNION ALL
  SELECT 3, 'Opportunity', COUNTIF(has_opp) FROM joined
  UNION ALL
  SELECT 4, 'Pipeline opportunity', COUNTIF(has_pipeline_opp) FROM joined
  UNION ALL
  SELECT 5, 'Closed', COUNTIF(is_won) FROM joined
)
ORDER BY n
