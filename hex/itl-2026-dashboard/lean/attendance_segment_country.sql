-- Participation by sales segment and country.
-- Partner / Eco = Salesforce Attended on those campaigns (not Fliplet 426/916).
-- CAB = 11 members + 28 guests from the Nov 2026 CAB sheet overlay.
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
attrs AS (
  SELECT
    LOWER(TRIM(email)) AS email,
    ANY_VALUE(COALESCE(NULLIF(TRIM(market_segment), ''), 'Unknown')) AS segment,
    ANY_VALUE(COALESCE(NULLIF(TRIM(country), ''), 'Unknown')) AS country
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
    COALESCE(NULLIF(TRIM(p.market_segment), ''), 'Unknown') AS segment,
    COALESCE(NULLIF(TRIM(p.country), ''), 'Unknown') AS country
  FROM `n8n-telemetry.marts.fct_campaign_member_pipeline` p
  WHERE p.campaign_id IN ('701cj00001LbE7XAAV', '701cj00001LbEQvAAN')
    AND p.member_status = 'Attended'
    AND p.email IS NOT NULL
  UNION ALL
  SELECT
    'CAB' AS day_name,
    cab.email,
    COALESCE(a.segment, 'Unknown') AS segment,
    COALESCE(a.country, 'Unknown') AS country
  FROM cab
  LEFT JOIN attrs a ON a.email = cab.email
)
SELECT day_name, 'segment' AS dim, segment AS dim_value, COUNT(DISTINCT email) AS people
FROM day_people
WHERE day_name IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT day_name, 'country' AS dim, country AS dim_value, COUNT(DISTINCT email) AS people
FROM day_people
WHERE day_name IS NOT NULL
GROUP BY 1, 2, 3
ORDER BY day_name, dim, people DESC
