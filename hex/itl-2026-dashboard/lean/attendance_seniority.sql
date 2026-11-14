-- Salesforce Attended members by title seniority. Not Fliplet 426 / 916.
WITH people_raw AS (
  SELECT
    CASE
      WHEN cm.CampaignId = '701cj00001LbE7XAAV' THEN 'Partner Day'
      WHEN cm.CampaignId = '701cj00001LbEQvAAN' THEN 'Ecosystem Day'
    END AS day_name,
    LOWER(TRIM(COALESCE(c.Email, l.Email))) AS email,
    COALESCE(c.Title, l.Title, l.Seniority__c) AS title_raw
  FROM `n8n-telemetry.salesforce_bq.CampaignMember` cm
  LEFT JOIN `n8n-telemetry.salesforce_bq.Lead` l
    ON l.Id = cm.LeadId AND l.IsDeleted = FALSE
  LEFT JOIN `n8n-telemetry.salesforce_bq.Contact` c
    ON c.Id = cm.ContactId AND c.IsDeleted = FALSE
  WHERE cm.IsDeleted = FALSE
    AND cm.CampaignId IN ('701cj00001LbE7XAAV', '701cj00001LbEQvAAN')
    AND cm.Status = 'Attended'
),
people AS (
  SELECT day_name, email, ANY_VALUE(title_raw) AS title_raw
  FROM people_raw
  WHERE day_name IS NOT NULL
    AND email IS NOT NULL
    AND email != ''
  GROUP BY day_name, email
)
SELECT
  day_name,
  CASE
    WHEN REGEXP_CONTAINS(LOWER(COALESCE(title_raw,'')), r'\b(ceo|cfo|cto|coo|cmo|ciso|chief|founder|co-founder|president|owner|managing director)\b') THEN 'Exec / founder'
    WHEN REGEXP_CONTAINS(LOWER(COALESCE(title_raw,'')), r'\b(svp|evp|vp\b|vice president)\b') THEN 'VP'
    WHEN REGEXP_CONTAINS(LOWER(COALESCE(title_raw,'')), r'\b(director|head of|principal)\b') THEN 'Director / head of'
    WHEN REGEXP_CONTAINS(LOWER(COALESCE(title_raw,'')), r'\b(manager|teamlead|team lead|lead\b)\b') THEN 'Manager / lead'
    WHEN REGEXP_CONTAINS(LOWER(COALESCE(title_raw,'')), r'\b(partner|consultant|advisor|ambassador)\b') THEN 'Partner / consultant'
    WHEN REGEXP_CONTAINS(LOWER(COALESCE(title_raw,'')), r'\b(engineer|developer|architect|analyst|scientist|specialist|admin|qa)\b') THEN 'IC / practitioner'
    WHEN title_raw IS NULL OR TRIM(title_raw) = '' THEN 'Unknown title'
    ELSE 'Other'
  END AS seniority,
  COUNT(*) AS people
FROM people
GROUP BY 1, 2
ORDER BY day_name, people DESC
