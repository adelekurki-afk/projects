-- Salesforce sales sub-region for Partner / Eco Attended and CAB overlay.
-- Same grain as Funnel: DACH, North EMEA, South EMEA, US, Other.
-- Partner 701cj00001LbE7XAAV / Eco 701cj00001LbEQvAAN, member_status = Attended.
WITH cab AS (
  SELECT email FROM UNNEST([
    'remi.tuyaerts@bakkt.com','steve.rotter@n8n.io','sean.morton@atos.ai',
    'melanie@324marketing.com','marvin-micha.lutz@digits.schwarz','jemerson1@wayfair.com',
    'aasenjo@indeed.com','andy.wolf@sixt.com','michael.mc.conrad@bmw.de',
    'saiesh.prakash@coinbase.com','petkova.alexandra@bcg.com',
    'mariia.heiss@mercedes-benz.com','antonius.wenhold@mercedes-benz.com','anton.heindl@mercedes-benz.com',
    'mobackes@expediagroup.com','przemyslaw.winszczyk@bakkt.com','umang.chhibber@atos.ai',
    'ziga.hanzic@sixt.com','elen.karadeniz@bakkt.com','rafal.golubowicz@bakkt.com',
    'levan.salia@dtr.org','ahenson1@wayfair.com','rutgere@indeed.com',
    'csalazar@indeed.com','jayakrishna.panda@sixt.com','andreas.zehnpfund@mercedes-benz.com',
    'elisabeth.halbe@mercedes-benz.com','evers.julia@bcg.com','wiatowski.thomas@bcg.com',
    'carina.koller@sixt.com','tim.murko@sixt.com','ajit.kumar@sixt.com',
    'bjoern.buechner@digits.schwarz','felix.baran@kaufland-ecommerce.com',
    'joshua.wahler@kaufland-ecommerce.com','julian.schnell@kaufland-ecommerce.com',
    'rouven.knoerzer_dilo@digits.schwarz','jan.schick@digits.schwarz',
    'moritz_peter.bierlich@digits.schwarz'
  ]) AS email
),
region_of AS (
  SELECT
    LOWER(TRIM(email)) AS email,
    ANY_VALUE(
      CASE
        WHEN sub_region IN ('US', 'US W', 'US E', 'US Cent') THEN 'US'
        WHEN NULLIF(TRIM(sub_region), '') IS NULL THEN 'Unknown'
        ELSE TRIM(sub_region)
      END
    ) AS region
  FROM `n8n-telemetry.marts.fct_campaign_member_pipeline`
  GROUP BY 1
),
day_people AS (
  SELECT
    CASE p.campaign_id
      WHEN '701cj00001LbE7XAAV' THEN 'Partner Day'
      WHEN '701cj00001LbEQvAAN' THEN 'Ecosystem Day'
    END AS day_name,
    LOWER(TRIM(p.email)) AS email,
    CASE
      WHEN p.sub_region IN ('US', 'US W', 'US E', 'US Cent') THEN 'US'
      WHEN NULLIF(TRIM(p.sub_region), '') IS NULL THEN 'Unknown'
      ELSE TRIM(p.sub_region)
    END AS region
  FROM `n8n-telemetry.marts.fct_campaign_member_pipeline` p
  WHERE p.campaign_id IN ('701cj00001LbE7XAAV', '701cj00001LbEQvAAN')
    AND p.member_status = 'Attended'
    AND p.email IS NOT NULL
  UNION ALL
  SELECT 'CAB', cab.email, COALESCE(r.region, 'Unknown')
  FROM cab
  LEFT JOIN region_of r ON r.email = cab.email
)
SELECT day_name, region, COUNT(DISTINCT email) AS people
FROM day_people
WHERE day_name IS NOT NULL
GROUP BY 1, 2
ORDER BY day_name, people DESC
