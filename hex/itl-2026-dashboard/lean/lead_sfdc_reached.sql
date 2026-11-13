-- Ever reached each Salesforce status. Pin as APP: SFDC lead reached.
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
reached AS (
  SELECT email, sfdc_status FROM lead_reached
  UNION DISTINCT
  SELECT email, sfdc_status FROM contact_reached
),
itl_people AS (
  SELECT COUNT(DISTINCT email) AS itl_people FROM itl WHERE email IS NOT NULL
)
SELECT
  CASE r.sfdc_status
    WHEN 'Suspect' THEN 1
    WHEN 'New' THEN 2
    WHEN 'Working' THEN 3
    WHEN 'Qualified' THEN 4
    WHEN 'Nurturing' THEN 5
    WHEN 'Unqualified' THEN 6
    ELSE 9
  END AS stage_n,
  r.sfdc_status,
  COUNT(DISTINCT r.email) AS people_ever_reached,
  p.itl_people,
  ROUND(100.0 * COUNT(DISTINCT r.email) / p.itl_people, 1) AS pct_of_itl
FROM reached r
CROSS JOIN itl_people p
GROUP BY 1, 2, p.itl_people
ORDER BY stage_n, people_ever_reached DESC
