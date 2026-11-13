-- Current Salesforce Lead/Contact status for ITL Free+Paid. Pin as APP: Salesforce lead statuses.
WITH itl AS (
  SELECT
    LOWER(TRIM(email)) AS email,
    member_status AS ticket,
    person_type,
    is_converted,
    COALESCE(NULLIF(TRIM(lead_status), ''), '(blank)') AS sfdc_status
  FROM `n8n-telemetry.marts.fct_campaign_member_pipeline`
  WHERE campaign_id = '701cj0000157ynMAAQ'
    AND member_status IN ('Free', 'Paid')
)
SELECT
  CASE sfdc_status
    WHEN 'Suspect' THEN 1
    WHEN 'New' THEN 2
    WHEN 'Working' THEN 3
    WHEN 'Qualified' THEN 4
    WHEN 'Nurturing' THEN 5
    WHEN 'Unqualified' THEN 6
    ELSE 9
  END AS stage_n,
  sfdc_status,
  COUNT(*) AS members,
  COUNT(DISTINCT email) AS people,
  COUNTIF(ticket = 'Free') AS free_tickets,
  COUNTIF(ticket = 'Paid') AS paid_tickets,
  COUNTIF(person_type = 'lead') AS still_lead,
  COUNTIF(person_type = 'contact' OR is_converted IS TRUE) AS converted_contact,
  ROUND(100.0 * COUNT(DISTINCT email) / SUM(COUNT(DISTINCT email)) OVER(), 1) AS pct_of_itl
FROM itl
GROUP BY 1, 2
ORDER BY stage_n, people DESC
