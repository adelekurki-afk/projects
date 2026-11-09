-- ============================================================
-- INSERT TODAY'S SNAPSHOT (idempotent — skips if date exists)
-- Schedule this cell or the full project to run daily.
-- ============================================================
INSERT INTO `n8n-telemetry.itl_2026_snapshots.progression_snapshots`
WITH registrants AS (
  SELECT email, name, company, segment, is_partner, day1, day2
  FROM `n8n-telemetry.itl_2026_snapshots.registrants`
),
email_lead AS (
  SELECT LOWER(r.email) AS email_lc,
    l.Id AS lead_id, l.IsConverted, l.ConvertedAccountId
  FROM registrants r
  INNER JOIN `n8n-telemetry.salesforce_bq.Lead` l
    ON LOWER(r.email) = LOWER(l.Email) AND l.IsDeleted = FALSE
),
email_contact AS (
  SELECT LOWER(r.email) AS email_lc,
    c.Id AS contact_id, c.AccountId AS contact_account_id
  FROM registrants r
  INNER JOIN `n8n-telemetry.salesforce_bq.Contact` c
    ON LOWER(r.email) = LOWER(c.Email) AND c.IsDeleted = FALSE
),
email_match AS (
  SELECT COALESCE(el.email_lc, ec.email_lc) AS email_lc,
    el.lead_id, el.IsConverted AS lead_is_converted, el.ConvertedAccountId,
    ec.contact_id, ec.contact_account_id,
    COALESCE(ec.contact_account_id, CASE WHEN el.IsConverted THEN el.ConvertedAccountId END) AS account_id
  FROM email_lead el
  FULL OUTER JOIN email_contact ec ON el.email_lc = ec.email_lc
),
rw AS (
  SELECT r.*, em.lead_id, em.lead_is_converted, em.contact_id,
    em.contact_account_id, em.account_id AS account_id_from_email
  FROM registrants r
  LEFT JOIN email_match em ON LOWER(r.email) = em.email_lc
),
domain_fallback AS (
  SELECT rw.*, a.Id AS domain_account_id
  FROM rw
  LEFT JOIN `n8n-telemetry.salesforce_bq.Account` a
    ON rw.account_id_from_email IS NULL AND rw.contact_id IS NULL AND rw.lead_id IS NULL
   AND LOWER(SPLIT(rw.email,'@')[SAFE_OFFSET(1)]) =
       LOWER(REGEXP_REPLACE(REGEXP_REPLACE(COALESCE(a.Website,''), r'^https?://(www\.)?',''), r'/.*$',''))
   AND a.IsDeleted = FALSE
),
resolved AS (
  SELECT *,
    COALESCE(account_id_from_email, domain_account_id) AS final_account_id,
    CASE
      WHEN contact_id IS NOT NULL THEN 'contact'
      WHEN lead_id IS NOT NULL AND lead_is_converted THEN 'converted_lead'
      WHEN lead_id IS NOT NULL THEN 'open_lead'
      WHEN domain_account_id IS NOT NULL THEN 'domain_match'
      ELSE 'unmatched'
    END AS match_type
  FROM domain_fallback
),
opp_rollup AS (
  SELECT
    r.email, r.name, r.company, r.segment, r.is_partner, r.day1, r.day2,
    r.match_type, r.lead_id AS sfdc_lead_id, r.contact_id AS sfdc_contact_id,
    r.final_account_id AS sfdc_account_id,
    COUNT(DISTINCT o.Id) AS opp_count,
    COUNT(DISTINCT CASE WHEN o.StageName='Closed Won' THEN o.Id END) AS closed_won_count,
    SUM(o.Net_New_ARR__c) AS total_net_new_arr,
    SUM(CASE WHEN o.StageName='Closed Won' THEN o.Net_New_ARR__c END) AS won_net_new_arr
  FROM resolved r
  LEFT JOIN `n8n-telemetry.salesforce_bq.Opportunity` o
    ON r.final_account_id = o.AccountId
   AND o.IsDeleted = FALSE
   AND o.StageName NOT IN ('Closed Duplicate','Disqualified')
   AND o.Type IN ('New Business','Expansion')
  GROUP BY
    r.email, r.name, r.company, r.segment, r.is_partner, r.day1, r.day2,
    r.match_type, r.lead_id, r.contact_id, r.final_account_id
)
SELECT
  CURRENT_DATE()   AS snapshot_date,
  email, name, company, segment, is_partner, day1, day2,
  match_type, sfdc_lead_id, sfdc_contact_id, sfdc_account_id,
  opp_count, closed_won_count, total_net_new_arr, won_net_new_arr,
  CURRENT_TIMESTAMP() AS created_at
FROM opp_rollup
WHERE CURRENT_DATE() NOT IN (
  SELECT DISTINCT snapshot_date
  FROM `n8n-telemetry.itl_2026_snapshots.progression_snapshots`
)