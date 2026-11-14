-- ITL 2026 Pipeline: fully SFDC CampaignMember-driven
-- Uses Opportunity.Amount (NB_ARR and EXP_ARR fields are null in this org; Amount is the deal value)
-- Registrant accounts sourced from ITL main campaign Lead (ConvertedAccountId) + Contact.AccountId
-- Meeting flag: account also in 'Meetings Booked' campaign

WITH

registrant_accounts AS (
  SELECT DISTINCT COALESCE(l.ConvertedAccountId, l.Matched_Account__c) AS account_id
  FROM `n8n-telemetry.salesforce_bq.CampaignMember` cm
  JOIN `n8n-telemetry.salesforce_bq.Lead` l ON l.Id = cm.LeadId AND l.IsDeleted = FALSE
  WHERE cm.IsDeleted = FALSE AND cm.CampaignId = '701cj0000157ynMAAQ'
    AND cm.Status IN ('Free','Paid') AND cm.LeadId IS NOT NULL
    AND COALESCE(l.ConvertedAccountId, l.Matched_Account__c) IS NOT NULL

  UNION DISTINCT

  SELECT DISTINCT c.AccountId AS account_id
  FROM `n8n-telemetry.salesforce_bq.CampaignMember` cm
  JOIN `n8n-telemetry.salesforce_bq.Contact` c ON c.Id = cm.ContactId AND c.IsDeleted = FALSE
  WHERE cm.IsDeleted = FALSE AND cm.CampaignId = '701cj0000157ynMAAQ'
    AND cm.Status IN ('Free','Paid') AND cm.ContactId IS NOT NULL
    AND c.AccountId IS NOT NULL
),

meeting_accounts AS (
  SELECT DISTINCT
    COALESCE(l.ConvertedAccountId, l.Matched_Account__c, c.AccountId) AS account_id
  FROM `n8n-telemetry.salesforce_bq.CampaignMember` cm
  LEFT JOIN `n8n-telemetry.salesforce_bq.Lead` l ON l.Id = cm.LeadId AND l.IsDeleted = FALSE
  LEFT JOIN `n8n-telemetry.salesforce_bq.Contact` c ON c.Id = cm.ContactId AND c.IsDeleted = FALSE
  WHERE cm.IsDeleted = FALSE AND cm.CampaignId = '701cj00001MqzF9AAJ'
    AND cm.Status = 'Meeting Booked'
    AND COALESCE(l.ConvertedAccountId, l.Matched_Account__c, c.AccountId) IS NOT NULL
),

opps AS (
  SELECT
    o.Id          AS opp_id,
    o.AccountId,
    o.Name        AS opp_name,
    o.StageName,
    o.Type,
    o.CloseDate,
    COALESCE(a.Name,'Unknown') AS account_name,
    COALESCE(a.Sales_Segment__c,'Unknown') AS segment,
    COALESCE(o.Amount, 0)  AS amount,
    ma.account_id IS NOT NULL AS from_meeting
  FROM `n8n-telemetry.salesforce_bq.Opportunity` o
  JOIN registrant_accounts ra ON ra.account_id = o.AccountId
  LEFT JOIN `n8n-telemetry.salesforce_bq.Account` a ON a.Id = o.AccountId AND a.IsDeleted = FALSE
  LEFT JOIN meeting_accounts ma ON ma.account_id = o.AccountId
  WHERE o.IsDeleted = FALSE
    AND o.StageName NOT IN ('Closed Duplicate','Disqualified')
    AND o.Type IN ('New Business','Expansion')
    AND DATE(o.CreatedDate) >= '2026-10-12'
)

SELECT
  Type                                                                     AS opp_type,
  segment,
  COUNT(DISTINCT opp_id)                                                   AS opp_count,
  COUNT(DISTINCT AccountId)                                                AS account_count,
  COUNTIF(from_meeting)                                                    AS opps_from_meetings,
  ROUND(SUM(amount), 0)                                                    AS total_amount,
  COUNTIF(StageName IN ('Closed Won','Closed Won Approved'))               AS closed_won_count,
  ROUND(SUM(CASE WHEN StageName IN ('Closed Won','Closed Won Approved')
                 THEN amount ELSE 0 END), 0)                               AS closed_won_amount,
  COUNTIF(StageName NOT IN ('Closed Won','Closed Won Approved'))           AS open_opp_count,
  ROUND(SUM(CASE WHEN StageName NOT IN ('Closed Won','Closed Won Approved')
                 THEN amount ELSE 0 END), 0)                               AS open_pipeline_amount
FROM opps
GROUP BY 1, 2
ORDER BY total_amount DESC