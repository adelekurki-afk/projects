-- People who attended each day, by Salesforce region and sales segment.
-- Day = Partner / Eco CampaignMember Status = Attended (not Fliplet door scans).
WITH people AS (
  SELECT
    CASE
      WHEN cm.CampaignId = '701cj00001LbE7XAAV' THEN 'Partner Day'
      WHEN cm.CampaignId = '701cj00001LbEQvAAN' THEN 'Ecosystem Day'
    END AS day_name,
    LOWER(TRIM(COALESCE(c.Email, l.Email))) AS email,
    COALESCE(a.Region__c, 'Unknown') AS region,
    COALESCE(a.Sales_Segment__c, 'Unknown') AS segment
  FROM `n8n-telemetry.salesforce_bq.CampaignMember` cm
  LEFT JOIN `n8n-telemetry.salesforce_bq.Lead` l
    ON l.Id = cm.LeadId AND l.IsDeleted = FALSE
  LEFT JOIN `n8n-telemetry.salesforce_bq.Contact` c
    ON c.Id = cm.ContactId AND c.IsDeleted = FALSE
  LEFT JOIN `n8n-telemetry.salesforce_bq.Account` a
    ON a.Id = COALESCE(c.AccountId, l.ConvertedAccountId, l.Matched_Account__c)
    AND a.IsDeleted = FALSE
  WHERE cm.IsDeleted = FALSE
    AND cm.CampaignId IN ('701cj00001LbE7XAAV', '701cj00001LbEQvAAN')
    AND cm.Status = 'Attended'
    AND LOWER(TRIM(COALESCE(c.Email, l.Email))) IS NOT NULL
)
SELECT
  day_name,
  region,
  segment,
  COUNT(DISTINCT email) AS people
FROM people
WHERE day_name IS NOT NULL
GROUP BY 1, 2, 3
ORDER BY day_name, people DESC
