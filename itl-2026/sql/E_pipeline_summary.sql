-- ============================================================
-- PIPELINE: OPPORTUNITIES LINKED TO ITL REGISTRANT ACCOUNTS
-- Filters: IsDeleted=FALSE, Stage not in (Closed Duplicate, Disqualified)
--          Type in (New Business, Expansion)
-- NOTE: Product_Interest__c filter NOT applied — confirm before filtering to Enterprise.
-- Currency: Amount_EUR__c used for EUR column; ARR fields in SFDC reporting currency.
-- ============================================================
WITH registrants AS (
  SELECT email, segment, is_partner
  FROM `n8n-telemetry.itl_2026_snapshots.registrants`
),
email_lead AS (
  SELECT LOWER(r.email) AS email_lc, l.IsConverted, l.ConvertedAccountId AS account_id
  FROM registrants r
  INNER JOIN `n8n-telemetry.salesforce_bq.Lead` l
    ON LOWER(r.email) = LOWER(l.Email) AND l.IsDeleted = FALSE AND l.IsConverted = TRUE
),
email_contact AS (
  SELECT LOWER(r.email) AS email_lc, c.AccountId AS account_id
  FROM registrants r
  INNER JOIN `n8n-telemetry.salesforce_bq.Contact` c
    ON LOWER(r.email) = LOWER(c.Email) AND c.IsDeleted = FALSE
),
email_account AS (
  SELECT email_lc, account_id FROM email_lead
  UNION DISTINCT
  SELECT email_lc, account_id FROM email_contact
  WHERE account_id IS NOT NULL
),
domain_account AS (
  SELECT LOWER(r.email) AS email_lc, a.Id AS account_id
  FROM registrants r
  LEFT JOIN email_account ea ON LOWER(r.email) = ea.email_lc
  INNER JOIN `n8n-telemetry.salesforce_bq.Account` a
    ON ea.account_id IS NULL
   AND LOWER(SPLIT(r.email, '@')[SAFE_OFFSET(1)]) =
       LOWER(REGEXP_REPLACE(REGEXP_REPLACE(COALESCE(a.Website,''), r'^https?://(www\.)?',''), r'/.*$',''))
   AND a.IsDeleted = FALSE
),
all_accounts AS (
  SELECT account_id FROM email_account WHERE account_id IS NOT NULL
  UNION DISTINCT
  SELECT account_id FROM domain_account
),
opps AS (
  SELECT
    o.Id               AS opportunity_id,
    o.Name             AS opportunity_name,
    a.Name             AS account_name,
    o.StageName        AS stage,
    o.Type             AS opp_type,
    o.ForecastCategoryName AS forecast_category,
    o.CloseDate,
    o.CurrencyIsoCode,
    o.Amount_EUR__c    AS amount_eur,
    o.Current_Customer_ARR__c,
    o.New_Business_ARR__c,
    o.Expansion_ARR__c,
    o.Renewal_ARR__c,
    o.C_C_Amount__c,
    o.Net_New_ARR__c,
    o.Customer_ARR_After__c,
    o.CreatedDate
  FROM all_accounts aa
  INNER JOIN `n8n-telemetry.salesforce_bq.Opportunity` o ON aa.account_id = o.AccountId
  INNER JOIN `n8n-telemetry.salesforce_bq.Account` a ON o.AccountId = a.Id
  WHERE o.IsDeleted = FALSE
    AND o.StageName NOT IN ('Closed Duplicate', 'Disqualified')
    AND o.Type IN ('New Business', 'Expansion')
)

SELECT
  opp_type,
  stage,
  COUNT(*)                        AS opp_count,
  SUM(amount_eur)                 AS total_amount_eur,
  SUM(New_Business_ARR__c)        AS new_business_arr,
  SUM(Expansion_ARR__c)           AS expansion_arr,
  SUM(Net_New_ARR__c)             AS net_new_arr,
  SUM(Renewal_ARR__c)             AS renewal_arr,
  SUM(C_C_Amount__c)              AS cc_amount,
  SUM(Customer_ARR_After__c)      AS arr_after,
  SUM(Current_Customer_ARR__c)    AS arr_before
FROM opps
GROUP BY opp_type, stage
ORDER BY opp_type, stage