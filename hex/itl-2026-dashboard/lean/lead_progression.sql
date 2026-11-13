-- SFDC lead progression for ITL 2026 Free+Paid. Pin as APP: Lead progression.
-- Cumulative ever-reached: ITL people → New (handed to sales) → Working → Qualified.
WITH itl AS (
  SELECT
    cm.LeadId AS lead_id,
    cm.ContactId AS contact_id,
    LOWER(TRIM(COALESCE(cm.Email, l.Email, c.Email))) AS email
  FROM `n8n-telemetry.salesforce_bq.CampaignMember` cm
  LEFT JOIN `n8n-telemetry.salesforce_bq.Lead` l
    ON l.Id = cm.LeadId AND l.IsDeleted = FALSE
  LEFT JOIN `n8n-telemetry.salesforce_bq.Contact` c
    ON c.Id = cm.ContactId AND c.IsDeleted = FALSE
  WHERE cm.IsDeleted = FALSE
    AND cm.CampaignId = '701cj0000157ynMAAQ'
    AND cm.Status IN ('Free', 'Paid')
),
lead_reached AS (
  SELECT i.email, h.NewValue AS sfdc_status
  FROM itl i
  JOIN `n8n-telemetry.salesforce_bq.LeadHistory` h
    ON h.LeadId = i.lead_id AND h.IsDeleted = FALSE
  WHERE i.lead_id IS NOT NULL AND h.Field = 'Status' AND h.NewValue IS NOT NULL
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
  WHERE i.contact_id IS NOT NULL AND h.Field IN ('Status__c', 'Status') AND h.NewValue IS NOT NULL
  UNION DISTINCT
  SELECT i.email, c.Status__c
  FROM itl i
  JOIN `n8n-telemetry.salesforce_bq.Contact` c
    ON c.Id = i.contact_id AND c.IsDeleted = FALSE
  WHERE i.contact_id IS NOT NULL AND c.Status__c IS NOT NULL
),
reached AS (
  SELECT email, sfdc_status FROM lead_reached
  UNION DISTINCT
  SELECT email, sfdc_status FROM contact_reached
),
p AS (
  SELECT COUNT(DISTINCT email) AS itl_people FROM itl WHERE email IS NOT NULL
),
a AS (
  SELECT
    COUNT(DISTINCT IF(sfdc_status = 'New', email, NULL)) AS ever_new,
    COUNT(DISTINCT IF(sfdc_status = 'Working', email, NULL)) AS ever_working,
    COUNT(DISTINCT IF(sfdc_status = 'Qualified', email, NULL)) AS ever_qualified
  FROM reached
)
SELECT stage_n, sfdc_status, people, pct_of_itl
FROM (
  SELECT 1 AS stage_n, 'ITL Free+Paid' AS sfdc_status, p.itl_people AS people, 100.0 AS pct_of_itl FROM p
  UNION ALL
  SELECT 2, 'New — handed to sales', a.ever_new, ROUND(100.0 * a.ever_new / p.itl_people, 1) FROM a CROSS JOIN p
  UNION ALL
  SELECT 3, 'Working', a.ever_working, ROUND(100.0 * a.ever_working / p.itl_people, 1) FROM a CROSS JOIN p
  UNION ALL
  SELECT 4, 'Qualified', a.ever_qualified, ROUND(100.0 * a.ever_qualified / p.itl_people, 1) FROM a CROSS JOIN p
)
ORDER BY stage_n
