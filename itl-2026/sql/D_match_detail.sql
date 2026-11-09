-- ============================================================
-- PER-REGISTRANT SFDC MATCH STATUS
-- Use to QA the funnel and investigate unmatched registrants
-- ============================================================
WITH registrants AS (
  SELECT email, name, company, sfdc_account, segment, country, is_partner, day1, day2, best_ticket
  FROM `n8n-telemetry.itl_2026_snapshots.registrants`
),
email_lead AS (
  SELECT LOWER(r.email) AS email_lc, l.Id AS lead_id, l.IsConverted,
    l.ConvertedAccountId, l.Status AS lead_status
  FROM registrants r
  INNER JOIN `n8n-telemetry.salesforce_bq.Lead` l
    ON LOWER(r.email) = LOWER(l.Email) AND l.IsDeleted = FALSE
),
email_contact AS (
  SELECT LOWER(r.email) AS email_lc, c.Id AS contact_id, c.AccountId AS contact_account_id
  FROM registrants r
  INNER JOIN `n8n-telemetry.salesforce_bq.Contact` c
    ON LOWER(r.email) = LOWER(c.Email) AND c.IsDeleted = FALSE
),
email_match AS (
  SELECT
    COALESCE(el.email_lc, ec.email_lc) AS email_lc,
    el.lead_id, el.IsConverted AS lead_is_converted,
    el.ConvertedAccountId AS lead_account_id, el.lead_status,
    ec.contact_id, ec.contact_account_id,
    COALESCE(ec.contact_account_id, CASE WHEN el.IsConverted THEN el.ConvertedAccountId END) AS account_id_from_email
  FROM email_lead el
  FULL OUTER JOIN email_contact ec ON el.email_lc = ec.email_lc
),
rw AS (
  SELECT r.*, em.lead_id, em.lead_is_converted, em.lead_account_id, em.lead_status,
    em.contact_id, em.contact_account_id, em.account_id_from_email
  FROM registrants r
  LEFT JOIN email_match em ON LOWER(r.email) = em.email_lc
),
domain_fallback AS (
  SELECT rw.*,
    a.Id AS domain_account_id,
    a.Name AS domain_account_name
  FROM rw
  LEFT JOIN `n8n-telemetry.salesforce_bq.Account` a
    ON rw.account_id_from_email IS NULL AND rw.contact_id IS NULL AND rw.lead_id IS NULL
   AND LOWER(SPLIT(rw.email, '@')[SAFE_OFFSET(1)]) =
       LOWER(REGEXP_REPLACE(REGEXP_REPLACE(COALESCE(a.Website,''), r'^https?://(www\.)?',''), r'/.*$',''))
   AND a.IsDeleted = FALSE
)

SELECT
  email, name, company, sfdc_account AS n8n_sfdc_account, segment, country,
  CASE
    WHEN contact_id IS NOT NULL THEN 'contact'
    WHEN lead_id IS NOT NULL AND lead_is_converted THEN 'converted_lead'
    WHEN lead_id IS NOT NULL THEN 'open_lead'
    WHEN domain_account_id IS NOT NULL THEN 'domain_match'
    ELSE 'unmatched'
  END AS match_type,
  lead_id, lead_status, lead_is_converted,
  contact_id,
  COALESCE(contact_account_id, CASE WHEN lead_is_converted THEN lead_account_id END, domain_account_id) AS resolved_account_id,
  domain_account_name,
  is_partner, day1, day2, best_ticket
FROM domain_fallback
ORDER BY match_type, company, email