-- Ever reached each Salesforce status, plus sales segment and region on the same rows.
-- STRING counts so the App SQL pin is not an empty INT tile.
-- Visuals live on APP: Funnel Chart (first figure = segment + region).
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
person AS (
  SELECT email, sfdc_status, 'lead' AS src FROM lead_reached
  UNION ALL
  SELECT email, sfdc_status, 'contact' FROM contact_reached
),
combo AS (
  SELECT i.email, i.segment, i.region, r.sfdc_status, r.src
  FROM itl i
  JOIN person r ON r.email = i.email
  WHERE r.sfdc_status IN ('Suspect', 'New', 'Working', 'Qualified', 'Nurturing', 'Unqualified')
),
base AS (
  SELECT
    sfdc_status,
    COUNT(DISTINCT email) AS people,
    COUNT(DISTINCT IF(src = 'lead', email, NULL)) AS as_lead,
    COUNT(DISTINCT IF(src = 'contact', email, NULL)) AS as_contact
  FROM combo
  GROUP BY 1
),
seg AS (
  SELECT * FROM (
    SELECT sfdc_status, segment AS k, COUNT(DISTINCT email) AS n
    FROM combo
    GROUP BY 1, 2
  ) PIVOT (SUM(n) FOR k IN ('ENT' AS ENT, 'MM' AS MM, 'SMB' AS SMB, 'Unknown' AS Unknown_seg))
),
reg AS (
  SELECT * FROM (
    SELECT sfdc_status, region AS k, COUNT(DISTINCT email) AS n
    FROM combo
    GROUP BY 1, 2
  ) PIVOT (
    SUM(n) FOR k IN (
      'DACH' AS DACH,
      'North EMEA' AS North_EMEA,
      'South EMEA' AS South_EMEA,
      'US' AS US,
      'Other' AS Other
    )
  )
),
itl_people AS (
  SELECT COUNT(DISTINCT email) AS itl_people FROM itl
)
SELECT
  b.sfdc_status,
  REPEAT(CHR(9608), CAST(GREATEST(1, ROUND(b.people / 35)) AS INT64)) AS reached,
  CAST(b.people AS STRING) AS people_ever_reached,
  CAST(b.as_lead AS STRING) AS as_lead,
  CAST(b.as_contact AS STRING) AS as_contact,
  CAST(IFNULL(s.ENT, 0) AS STRING) AS ENT,
  CAST(IFNULL(s.MM, 0) AS STRING) AS MM,
  CAST(IFNULL(s.SMB, 0) AS STRING) AS SMB,
  CAST(IFNULL(r.DACH, 0) AS STRING) AS DACH,
  CAST(IFNULL(r.North_EMEA, 0) AS STRING) AS North_EMEA,
  CAST(IFNULL(r.South_EMEA, 0) AS STRING) AS South_EMEA,
  CAST(IFNULL(r.US, 0) AS STRING) AS US,
  CAST(IFNULL(r.Other, 0) AS STRING) AS Other,
  CAST(ROUND(100.0 * b.people / p.itl_people, 1) AS STRING) AS pct_of_itl,
  CASE b.sfdc_status
    WHEN 'Suspect' THEN 1
    WHEN 'New' THEN 2
    WHEN 'Working' THEN 3
    WHEN 'Qualified' THEN 4
    WHEN 'Nurturing' THEN 5
    WHEN 'Unqualified' THEN 6
    ELSE 9
  END AS stage_n
FROM base b
LEFT JOIN seg s ON s.sfdc_status = b.sfdc_status
LEFT JOIN reg r ON r.sfdc_status = b.sfdc_status
CROSS JOIN itl_people p
ORDER BY stage_n
