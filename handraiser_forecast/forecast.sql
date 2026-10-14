-- Quarterly handraiser counts for the softened forecast.
-- A single quarter's year-over-year rate is what makes the current forecast too steep.
-- This grain is the history that a trailing twelve months, and an eight-quarter anchor, need.
-- Fiscal quarters are calendar quarters because the fiscal year starts in January.
-- One person is counted once per quarter. lead_id alone drops responses that only have a contact or an email.
-- History starts in 2025. Earlier campaign responses are a December 2024 load, not a quarter of demand.
-- The open quarter is left out so a partial October cannot set the rate.

WITH params AS (
  SELECT DATE '2025-01-01' AS start_date, DATE '2026-10-01' AS end_date_exclusive
),
inbound_campaigns AS (
  SELECT campaign_name FROM UNNEST([
    'n8n Embed Contact Us Form',
    'n8n Talk to Sales Web Form',
    'n8n license@n8n.io inbound email',
    'n8n sales@n8n.io inbound email'
  ]) AS campaign_name
),
free_domains AS (
  SELECT domain FROM UNNEST([
    'gmail.com', 'googlemail.com', 'yahoo.com', 'yahoo.co.uk', 'hotmail.com',
    'outlook.com', 'live.com', 'msn.com', 'icloud.com', 'me.com', 'mac.com',
    'aol.com', 'proton.me', 'protonmail.com', 'gmx.com', 'gmx.de', 'mail.com',
    'yandex.com', 'qq.com', 'web.de', 'mail.ru'
  ]) AS domain
),
country_to_region AS (
  SELECT country_key, source_region
  FROM (
    SELECT LOWER(TRIM(Country)) AS country_key, Region__c AS source_region, COUNT(*) AS leads
    FROM `n8n-telemetry.salesforce_bq.Lead`
    WHERE IsDeleted = FALSE
      AND Region__c IN ('NA', 'LATAM', 'ANZ', 'EMEA', 'APAC')
      AND Country IS NOT NULL AND TRIM(Country) != ''
    GROUP BY 1, 2
  )
  QUALIFY ROW_NUMBER() OVER (PARTITION BY country_key ORDER BY leads DESC) = 1
),
members AS (
  SELECT
    m.campaign_member_id,
    m.lead_id,
    m.contact_id,
    m.account_id,
    NULLIF(LOWER(TRIM(m.email)), '') AS email_norm,
    m.lead_status,
    m.region AS member_region,
    m.country AS member_country,
    m.first_responded_date,
    DATE_TRUNC(m.first_responded_date, QUARTER) AS quarter_start
  FROM `n8n-telemetry.marts.fct_campaign_member_pipeline` AS m
  CROSS JOIN params AS p
  WHERE m.campaign_name IN (SELECT campaign_name FROM inbound_campaigns)
    AND m.first_responded_date >= p.start_date
    AND m.first_responded_date < p.end_date_exclusive
),
enriched AS (
  SELECT
    m.*,
    COALESCE(
      NULLIF(l.NumberOfEmployees, 0),
      NULLIF(a.NumberOfEmployees, 0),
      l.NumberOfEmployees,
      a.NumberOfEmployees
    ) AS employees,
    CASE
      WHEN UPPER(COALESCE(NULLIF(l.Region__c, ''), NULLIF(m.member_region, '')))
        IN ('NA', 'US', 'AMER', 'LATAM', 'ANZ', 'EMEA', 'APAC')
        THEN UPPER(COALESCE(NULLIF(l.Region__c, ''), NULLIF(m.member_region, '')))
      ELSE ctry.source_region
    END AS source_region,
    (
      m.email_norm IS NOT NULL
      AND COALESCE(l.Status, m.lead_status, '') != 'Suspect'
      AND NOT REGEXP_CONTAINS(m.email_norm, r'@n8n\.io\b')
      AND NOT REGEXP_CONTAINS(m.email_norm, r'@test')
      AND COALESCE(NULLIF(LOWER(l.Email_domain__c), ''), REGEXP_EXTRACT(m.email_norm, r'@([^@]+)$'), '')
        NOT IN (SELECT domain FROM free_domains)
    ) AS is_handraiser
  FROM members AS m
  LEFT JOIN `n8n-telemetry.salesforce_bq.Lead` AS l ON l.Id = m.lead_id
  LEFT JOIN `n8n-telemetry.salesforce_bq.Account` AS a
    ON a.Id = COALESCE(l.ConvertedAccountId, m.account_id) AND a.IsDeleted = FALSE
  LEFT JOIN country_to_region AS ctry
    ON ctry.country_key = LOWER(TRIM(COALESCE(l.Country, m.member_country)))
  WHERE m.lead_id IS NULL OR l.IsDeleted = FALSE
),
classified AS (
  SELECT
    *,
    COALESCE(lead_id, contact_id, email_norm, campaign_member_id) AS person_key,
    CASE
      WHEN employees IS NULL THEN 'Unknown'
      WHEN employees <= 100 THEN 'Self-Service'
      WHEN employees <= 1000 THEN 'Commercial'
      WHEN employees <= 5000 THEN 'Mid-Market'
      ELSE 'Enterprise'
    END AS segment,
    CASE
      WHEN source_region IN ('NA', 'US', 'AMER', 'LATAM', 'ANZ') THEN 'US+LATAM+ANZ'
      WHEN source_region IN ('EMEA', 'APAC') THEN 'EMEA+ASIA'
      ELSE 'Unknown'
    END AS region_group
  FROM enriched
),
handraiser_people AS (
  SELECT
    quarter_start,
    person_key,
    ARRAY_AGG(segment ORDER BY IF(segment = 'Unknown', 1, 0), first_responded_date, campaign_member_id LIMIT 1)[OFFSET(0)] AS segment,
    ARRAY_AGG(region_group ORDER BY IF(region_group = 'Unknown', 1, 0), first_responded_date, campaign_member_id LIMIT 1)[OFFSET(0)] AS region_group
  FROM classified
  WHERE is_handraiser
  GROUP BY 1, 2
),
quarterly AS (
  SELECT quarter_start, segment, region_group, COUNT(*) AS leads
  FROM handraiser_people
  GROUP BY 1, 2, 3
),
quarters AS (
  SELECT quarter_start
  FROM UNNEST(GENERATE_DATE_ARRAY(DATE '2025-01-01', DATE '2026-07-01', INTERVAL 3 MONTH)) AS quarter_start
),
segments AS (
  SELECT segment, segment_sort FROM UNNEST([
    STRUCT('Self-Service' AS segment, 1 AS segment_sort),
    STRUCT('Commercial', 2),
    STRUCT('Mid-Market', 3),
    STRUCT('Enterprise', 4),
    STRUCT('Unknown', 5),
    STRUCT('All segments', 6)
  ])
),
regions AS (
  SELECT region_group, region_sort FROM UNNEST([
    STRUCT('US+LATAM+ANZ' AS region_group, 1 AS region_sort),
    STRUCT('EMEA+ASIA', 2),
    STRUCT('Unknown', 3)
  ])
),
detail AS (
  SELECT
    quarters.quarter_start,
    segments.segment,
    segments.segment_sort,
    regions.region_group,
    regions.region_sort,
    COALESCE(q.leads, 0) AS leads
  FROM quarters
  CROSS JOIN segments
  CROSS JOIN regions
  LEFT JOIN quarterly AS q
    ON q.quarter_start = quarters.quarter_start
    AND q.segment = segments.segment
    AND q.region_group = regions.region_group
  WHERE segments.segment != 'All segments'
),
with_total AS (
  SELECT quarter_start, segment, segment_sort, region_group, region_sort, leads
  FROM detail
  UNION ALL
  SELECT quarter_start, 'All segments', 6, region_group, region_sort, SUM(leads)
  FROM detail
  GROUP BY 1, 2, 3, 4, 5
)
SELECT
  region_group AS region,
  segment,
  EXTRACT(YEAR FROM quarter_start) AS fiscal_year,
  EXTRACT(QUARTER FROM quarter_start) AS fiscal_quarter,
  leads
FROM with_total
ORDER BY region_sort, segment_sort, quarter_start
