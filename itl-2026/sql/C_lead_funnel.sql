-- ============================================================
-- LEAD PROGRESSION FUNNEL
-- Registered → Matched in SFDC → Has Opportunity → Closed Won
-- Attribution: event registrants from ITL 2026 (2026-10-12 to 2026-10-18)
-- ============================================================
WITH registrants AS (
  SELECT email, name, company, sfdc_account, segment, is_partner, day1, day2
  FROM `n8n-telemetry.itl_2026_snapshots.registrants`
),

-- 1. Email → Lead
email_lead AS (
  SELECT r.email,
    l.Id        AS lead_id,
    l.IsConverted,
    l.ConvertedAccountId,
    l.ConvertedContactId
  FROM registrants r
  INNER JOIN `n8n-telemetry.salesforce_bq.Lead` l
    ON LOWER(r.email) = LOWER(l.Email)
   AND l.IsDeleted = FALSE
),

-- 2. Email → Contact
email_contact AS (
  SELECT r.email,
    c.Id        AS contact_id,
    c.AccountId AS contact_account_id
  FROM registrants r
  INNER JOIN `n8n-telemetry.salesforce_bq.Contact` c
    ON LOWER(r.email) = LOWER(c.Email)
   AND c.IsDeleted = FALSE
),

-- 3. Merge email matches; keep best account: contact > converted lead
email_match AS (
  SELECT
    COALESCE(el.email, ec.email) AS email,
    el.lead_id,
    el.IsConverted            AS lead_is_converted,
    el.ConvertedAccountId     AS lead_account_id,
    ec.contact_id,
    ec.contact_account_id,
    COALESCE(
      ec.contact_account_id,
      CASE WHEN el.IsConverted THEN el.ConvertedAccountId END
    ) AS account_id_from_email
  FROM email_lead el
  FULL OUTER JOIN email_contact ec ON LOWER(el.email) = LOWER(ec.email)
),

-- 4. Attach email-match results to every registrant
rw AS (
  SELECT
    r.email, r.segment, r.is_partner,
    em.lead_id,
    em.lead_is_converted,
    em.contact_id,
    em.contact_account_id,
    em.account_id_from_email
  FROM registrants r
  LEFT JOIN email_match em ON LOWER(r.email) = LOWER(em.email)
),

-- 5. Domain fallback: unmatched email → Account.Website
domain_fallback AS (
  SELECT rw.*,
    a.Id AS domain_account_id
  FROM rw
  LEFT JOIN `n8n-telemetry.salesforce_bq.Account` a
    ON rw.account_id_from_email IS NULL
   AND rw.contact_id IS NULL
   AND rw.lead_id IS NULL
   AND LOWER(SPLIT(rw.email, '@')[SAFE_OFFSET(1)]) =
       LOWER(REGEXP_REPLACE(
         REGEXP_REPLACE(COALESCE(a.Website, ''), r'^https?://(www\.)?', ''),
         r'/.*$', ''))
   AND a.IsDeleted = FALSE
),

-- 6. Resolve final account ID and match type
resolved AS (
  SELECT *,
    COALESCE(account_id_from_email, domain_account_id) AS final_account_id,
    CASE
      WHEN contact_id IS NOT NULL THEN 'contact'
      WHEN lead_id    IS NOT NULL AND lead_is_converted THEN 'converted_lead'
      WHEN lead_id    IS NOT NULL THEN 'open_lead'
      WHEN domain_account_id IS NOT NULL THEN 'domain'
      ELSE 'unmatched'
    END AS match_type
  FROM domain_fallback
),

-- 7. Opportunity roll-up per registrant
opp_rollup AS (
  SELECT
    r.email,
    r.match_type,
    COUNT(DISTINCT o.Id)                                    AS opp_count,
    COUNT(DISTINCT CASE WHEN o.StageName = 'Closed Won'
                         THEN o.Id END)                     AS closed_won_count,
    SUM(o.Net_New_ARR__c)                                   AS total_net_new_arr,
    SUM(CASE WHEN o.StageName = 'Closed Won'
              THEN o.Net_New_ARR__c END)                    AS won_net_new_arr
  FROM resolved r
  LEFT JOIN `n8n-telemetry.salesforce_bq.Opportunity` o
    ON r.final_account_id = o.AccountId
   AND o.IsDeleted = FALSE
   AND o.StageName NOT IN ('Closed Duplicate', 'Disqualified')
   AND o.Type IN ('New Business', 'Expansion')
  GROUP BY r.email, r.match_type
)

-- Funnel summary
SELECT
  1          AS sort_order,
  'Registered'      AS stage,
  COUNT(*)          AS registrant_count,
  NULL              AS total_net_new_arr_eur
FROM opp_rollup
UNION ALL
SELECT 2, 'Matched in SFDC',
  COUNTIF(match_type != 'unmatched'), NULL
FROM opp_rollup
UNION ALL
SELECT 3, 'Has Open Opportunity',
  COUNTIF(opp_count > 0), SUM(CASE WHEN opp_count > 0 THEN total_net_new_arr END)
FROM opp_rollup
UNION ALL
SELECT 4, 'Closed Won',
  COUNTIF(closed_won_count > 0), SUM(won_net_new_arr)
FROM opp_rollup
ORDER BY sort_order