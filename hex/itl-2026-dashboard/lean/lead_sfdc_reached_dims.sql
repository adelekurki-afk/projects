-- SFDC lead reached by sales segment and region. ITL Free+Paid.
-- Segment = fct_campaign_member_pipeline.market_segment (ENT/MM/SMB).
-- Region = Salesforce sub-region (DACH, North EMEA, South EMEA, US rolled up).
-- Unique people ever in each status; not stacked (same person can hit several statuses).
WITH itl AS (
  SELECT
    LOWER(TRIM(p.email)) AS email,
    ANY_VALUE(p.lead_id) AS lead_id,
    ANY_VALUE(p.contact_id) AS contact_id,
    ANY_VALUE(COALESCE(NULLIF(TRIM(p.market_segment), ''), 'Unknown')) AS segment,
    ANY_VALUE(
      CASE
        WHEN p.sub_region IN ('US', 'US W', 'US E', 'US Cent') THEN 'US'
        WHEN NULLIF(TRIM(p.sub_region), '') IS NULL THEN 'Unknown'
        ELSE TRIM(p.sub_region)
      END
    ) AS region
  FROM `n8n-telemetry.marts.fct_campaign_member_pipeline` p
  WHERE p.campaign_id = '701cj0000157ynMAAQ'
    AND p.member_status IN ('Free', 'Paid')
    AND p.email IS NOT NULL
  GROUP BY 1
),
lead_reached AS (
  SELECT i.email, h.NewValue AS sfdc_status
  FROM itl i
  JOIN `n8n-telemetry.salesforce_bq.LeadHistory` h
    ON h.LeadId = i.lead_id AND h.IsDeleted = FALSE
  WHERE i.lead_id IS NOT NULL
    AND h.Field = 'Status'
    AND h.NewValue IS NOT NULL
  UNION DISTINCT
  SELECT i.email, l.Status
  FROM itl i
  JOIN `n8n-telemetry.salesforce_bq.Lead` l
    ON l.Id = i.lead_id AND l.IsDeleted = FALSE
  WHERE i.lead_id IS NOT NULL AND l.Status IS NOT NULL
),
contact_reached AS (
  SELECT i.email, h.NewValue AS sfdc_status
  FROM itl i
  JOIN `n8n-telemetry.salesforce_bq.ContactHistory` h
    ON h.ContactId = i.contact_id AND h.IsDeleted = FALSE
  WHERE i.contact_id IS NOT NULL
    AND h.Field IN ('Status__c', 'Status')
    AND h.NewValue IS NOT NULL
  UNION DISTINCT
  SELECT i.email, c.Status__c
  FROM itl i
  JOIN `n8n-telemetry.salesforce_bq.Contact` c
    ON c.Id = i.contact_id AND c.IsDeleted = FALSE
  WHERE i.contact_id IS NOT NULL AND c.Status__c IS NOT NULL
),
combined AS (
  SELECT i.email, i.segment, i.region, r.sfdc_status
  FROM itl i
  JOIN lead_reached r ON r.email = i.email
  UNION DISTINCT
  SELECT i.email, i.segment, i.region, r.sfdc_status
  FROM itl i
  JOIN contact_reached r ON r.email = i.email
),
long AS (
  SELECT 'segment' AS dim, segment AS dim_value, sfdc_status, email FROM combined
  UNION ALL
  SELECT 'region', region, sfdc_status, email FROM combined
)
SELECT
  dim,
  dim_value,
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
  COUNT(DISTINCT email) AS people
FROM long
WHERE sfdc_status IN ('Suspect', 'New', 'Working', 'Qualified', 'Nurturing', 'Unqualified')
GROUP BY 1, 2, 3, 4
ORDER BY dim, stage_n, people DESC
