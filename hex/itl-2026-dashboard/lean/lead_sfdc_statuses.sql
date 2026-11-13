-- Salesforce lead/contact status for ITL 2026 Free+Paid members. Pin as APP: Salesforce lead statuses.
SELECT
  COALESCE(NULLIF(TRIM(cm.Contact_or_Lead_Status__c), ''), '(blank)') AS lead_status,
  cm.Status AS ticket,
  COUNT(*) AS members,
  COUNT(DISTINCT LOWER(TRIM(COALESCE(cm.Email, l.Email, ct.Email)))) AS unique_emails
FROM `n8n-telemetry.salesforce_bq.CampaignMember` cm
LEFT JOIN `n8n-telemetry.salesforce_bq.Lead` l
  ON l.Id = cm.LeadId AND l.IsDeleted = FALSE
LEFT JOIN `n8n-telemetry.salesforce_bq.Contact` ct
  ON ct.Id = cm.ContactId AND ct.IsDeleted = FALSE
WHERE cm.IsDeleted = FALSE
  AND cm.CampaignId = '701cj0000157ynMAAQ'
  AND cm.Status IN ('Free', 'Paid')
GROUP BY 1, 2
ORDER BY members DESC
