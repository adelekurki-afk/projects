-- CampaignMember.Status on ITL 2026 campaigns. Pin as APP: Campaign member statuses.
SELECT
  c.Name AS campaign,
  cm.Status AS member_status,
  COUNT(*) AS members,
  COUNT(DISTINCT LOWER(TRIM(COALESCE(cm.Email, l.Email, ct.Email)))) AS unique_emails
FROM `n8n-telemetry.salesforce_bq.CampaignMember` cm
JOIN `n8n-telemetry.salesforce_bq.Campaign` c
  ON c.Id = cm.CampaignId AND c.IsDeleted = FALSE
LEFT JOIN `n8n-telemetry.salesforce_bq.Lead` l
  ON l.Id = cm.LeadId AND l.IsDeleted = FALSE
LEFT JOIN `n8n-telemetry.salesforce_bq.Contact` ct
  ON ct.Id = cm.ContactId AND ct.IsDeleted = FALSE
WHERE cm.IsDeleted = FALSE
  AND cm.CampaignId IN (
    '701cj0000157ynMAAQ',  -- ITL 2026 main
    '701cj00001LbEQvAAN',  -- Ecosystem Day
    '701cj00001LbE7XAAV',  -- Partner Day
    '701cj00001MqzF9AAJ'   -- Meetings booked
  )
GROUP BY 1, 2
ORDER BY campaign, members DESC
