-- ITL 2026 Lead Funnel: SFDC CampaignMember-driven + CAB corrections
-- Stage 1: Registered (ITL main campaign, Free + Paid)
-- Stage 2: Attended (Eco Day OR Partner Day) — SFDC + manual CAB corrections
-- Stage 3: Had an n8n Meeting (Meetings Booked campaign)
-- Stage 4: Account has active Opp >= 2026-10-12, NB or Expansion
-- Stage 5: Closed Won

WITH

-- ── CAB manual corrections (green/YES from Nov 2026 spreadsheet) ───────────
cab_eco_manual AS (
  SELECT email FROM UNNEST([
  ('aasenjo@indeed.com'),
  ('ahenson1@wayfair.com'),
  ('ajit.kumar@sixt.com'),
  ('andrada.dugan@gmail.com'),
  ('andreas.zehnpfund@mercedes-benz.com'),
  ('andy.wolf@sixt.com'),
  ('aneesh.kanakdande@symplytics.com'),
  ('anton.heindl@mercedes-benz.com'),
  ('antonius.wenhold@mercedes-benz.com'),
  ('aya@n8n.io'),
  ('bjoern.buechner@digits.schwarz'),
  ('carina.koller@sixt.com'),
  ('csalazar@indeed.com'),
  ('cynthia.gassmann@n8n.io'),
  ('david.a.moreira.m@gmail.com'),
  ('elen.karadeniz@bakkt.com'),
  ('elisabeth.halbe@mercedes-benz.com'),
  ('evers.julia@bcg.com'),
  ('fabio.farzat@ed.dev.br'),
  ('farouk.houjri@datasulting.com'),
  ('felix.baran@kaufland-ecommerce.com'),
  ('hasan@n8n.io'),
  ('hello@larsemil.ai'),
  ('hi@francomaciel.com'),
  ('ibrahim.mafhoum@aicrafters.com'),
  ('jan.schick@digits.schwarz'),
  ('jaruphat.j@peakwave.co.th'),
  ('jashan.patel@moonspringai.com'),
  ('jayakrishna.panda@sixt.com'),
  ('jemerson1@wayfair.com'),
  ('jim.le@subworkflow.ai'),
  ('joshua.wahler@kaufland-ecommerce.com'),
  ('julian.schnell@kaufland-ecommerce.com'),
  ('k.onurakbal@relexsolutions.com'),
  ('kaila@theaihomegirl.com'),
  ('kailashps.1011@gmail.com'),
  ('khylepanganiban12@gmail.com'),
  ('levan.salia@dtr.org'),
  ('levi.tochtermann@relyon.de'),
  ('maciej.wesolowski@gmail.com'),
  ('marcel.claus@geckse.de'),
  ('mariia.heiss@mercedes-benz.com'),
  ('marvin-micha.lutz@digits.schwarz'),
  ('matthew@morningbrew.tv'),
  ('max@flowgrammer.com'),
  ('mdpotter@gmail.com'),
  ('melanie@324marketing.com'),
  ('michael.mc.conrad@bmw.de'),
  ('mick@bitovi.com'),
  ('mirza.iqbal.de@gmail.com'),
  ('mobackes@expediagroup.com'),
  ('moritz_peter.bierlich@digits.schwarz'),
  ('niklas@n8n.io'),
  ('oldorr@microsoft.com'),
  ('oli.morris@n8n.io'),
  ('oliver.rasch@relyon.de'),
  ('paul.gordon@n8n.io'),
  ('petkova.alexandra@bcg.com'),
  ('przemyslaw.winszczyk@bakkt.com'),
  ('rafal.golubowicz@bakkt.com'),
  ('raphael.gomez@n8n.io'),
  ('remi.tuyaerts@bakkt.com'),
  ('ria@n8n.io'),
  ('rouven.knoerzer_dilo@digits.schwarz'),
  ('rutgere@indeed.com'),
  ('saiesh.prakash@coinbase.com'),
  ('sandra.lentini@n8n.io'),
  ('sean.morton@atos.ai'),
  ('steve.rotter@n8n.io'),
  ('tim.murko@sixt.com'),
  ('timothy.vermeiren@biztory.com'),
  ('tusharrayamajhi956@gmail.com'),
  ('umang.chhibber@atos.ai'),
  ('viktoriia.dankevych@n8n.io'),
  ('weronikawoloszautomatyzacja@gmail.com'),
  ('wiatowski.thomas@bcg.com'),
  ('xinkai.li@bayer.com'),
  ('ziga.hanzic@sixt.com')
  ]) AS email
),

cab_partner_manual AS (
  SELECT email FROM UNNEST([
  ('ahenson1@wayfair.com'),
  ('ajit.kumar@sixt.com'),
  ('andreas.zehnpfund@mercedes-benz.com'),
  ('anton.heindl@mercedes-benz.com'),
  ('antonius.wenhold@mercedes-benz.com'),
  ('bjoern.buechner@digits.schwarz'),
  ('carina.koller@sixt.com'),
  ('csalazar@indeed.com'),
  ('elen.karadeniz@bakkt.com'),
  ('elisabeth.halbe@mercedes-benz.com'),
  ('evers.julia@bcg.com'),
  ('felix.baran@kaufland-ecommerce.com'),
  ('jan.schick@digits.schwarz'),
  ('jayakrishna.panda@sixt.com'),
  ('joshua.wahler@kaufland-ecommerce.com'),
  ('julian.schnell@kaufland-ecommerce.com'),
  ('levan.salia@dtr.org'),
  ('mariia.heiss@mercedes-benz.com'),
  ('mobackes@expediagroup.com'),
  ('moritz_peter.bierlich@digits.schwarz'),
  ('petkova.alexandra@bcg.com'),
  ('przemyslaw.winszczyk@bakkt.com'),
  ('rafal.golubowicz@bakkt.com'),
  ('rouven.knoerzer_dilo@digits.schwarz'),
  ('rutgere@indeed.com'),
  ('tim.murko@sixt.com'),
  ('umang.chhibber@atos.ai'),
  ('wiatowski.thomas@bcg.com'),
  ('ziga.hanzic@sixt.com')
  ]) AS email
),

-- ── Registrant pool ──────────────────────────────────────────────────────────
itl_leads AS (
  SELECT LOWER(TRIM(l.Email)) AS email,
         COALESCE(l.ConvertedAccountId, l.Matched_Account__c) AS account_id
  FROM `n8n-telemetry.salesforce_bq.CampaignMember` cm
  JOIN `n8n-telemetry.salesforce_bq.Lead` l
    ON l.Id = cm.LeadId AND l.IsDeleted = FALSE
  WHERE cm.IsDeleted = FALSE AND cm.CampaignId = '701cj0000157ynMAAQ'
    AND cm.Status IN ('Free','Paid') AND cm.LeadId IS NOT NULL
),

itl_contacts AS (
  SELECT LOWER(TRIM(c.Email)) AS email, c.AccountId AS account_id
  FROM `n8n-telemetry.salesforce_bq.CampaignMember` cm
  JOIN `n8n-telemetry.salesforce_bq.Contact` c
    ON c.Id = cm.ContactId AND c.IsDeleted = FALSE
  WHERE cm.IsDeleted = FALSE AND cm.CampaignId = '701cj0000157ynMAAQ'
    AND cm.Status IN ('Free','Paid') AND cm.ContactId IS NOT NULL
),

registered AS (
  SELECT email, account_id FROM itl_leads
  UNION ALL
  SELECT email, account_id FROM itl_contacts
),

-- ── Attendance — SFDC + manual corrections ─────────────────────────────────
eco_attendees AS (
  SELECT LOWER(TRIM(COALESCE(l.Email, c.Email))) AS email
  FROM `n8n-telemetry.salesforce_bq.CampaignMember` cm
  LEFT JOIN `n8n-telemetry.salesforce_bq.Lead` l ON l.Id = cm.LeadId AND l.IsDeleted = FALSE
  LEFT JOIN `n8n-telemetry.salesforce_bq.Contact` c ON c.Id = cm.ContactId AND c.IsDeleted = FALSE
  WHERE cm.IsDeleted = FALSE AND cm.CampaignId = '701cj00001LbEQvAAN' AND cm.Status = 'Attended'
  UNION DISTINCT
  SELECT email FROM cab_eco_manual
),

partner_attendees AS (
  SELECT LOWER(TRIM(COALESCE(l.Email, c.Email))) AS email
  FROM `n8n-telemetry.salesforce_bq.CampaignMember` cm
  LEFT JOIN `n8n-telemetry.salesforce_bq.Lead` l ON l.Id = cm.LeadId AND l.IsDeleted = FALSE
  LEFT JOIN `n8n-telemetry.salesforce_bq.Contact` c ON c.Id = cm.ContactId AND c.IsDeleted = FALSE
  WHERE cm.IsDeleted = FALSE AND cm.CampaignId = '701cj00001LbE7XAAV' AND cm.Status = 'Attended'
  UNION DISTINCT
  SELECT email FROM cab_partner_manual
),

attended AS (
  SELECT email FROM eco_attendees
  UNION DISTINCT
  SELECT email FROM partner_attendees
),

meeting_booked AS (
  SELECT LOWER(TRIM(COALESCE(l.Email, c.Email))) AS email
  FROM `n8n-telemetry.salesforce_bq.CampaignMember` cm
  LEFT JOIN `n8n-telemetry.salesforce_bq.Lead` l ON l.Id = cm.LeadId AND l.IsDeleted = FALSE
  LEFT JOIN `n8n-telemetry.salesforce_bq.Contact` c ON c.Id = cm.ContactId AND c.IsDeleted = FALSE
  WHERE cm.IsDeleted = FALSE AND cm.CampaignId = '701cj00001MqzF9AAJ' AND cm.Status = 'Meeting Booked'
),

opp_accounts AS (
  SELECT DISTINCT AccountId AS account_id
  FROM `n8n-telemetry.salesforce_bq.Opportunity`
  WHERE IsDeleted = FALSE
    AND StageName NOT IN ('Closed Duplicate','Disqualified')
    AND Type IN ('New Business','Expansion')
    AND DATE(CreatedDate) >= '2026-10-12'
),

closed_won_accounts AS (
  SELECT DISTINCT AccountId AS account_id
  FROM `n8n-telemetry.salesforce_bq.Opportunity`
  WHERE IsDeleted = FALSE
    AND StageName IN ('Closed Won','Closed Won Approved')
    AND Type IN ('New Business','Expansion')
    AND DATE(CreatedDate) >= '2026-10-12'
)

SELECT stage, count,
  ROUND(100.0 * count / MAX(count) OVER(), 1) AS pct_of_registered
FROM (
  SELECT 1 AS n, 'Registered'                             AS stage,
    COUNT(DISTINCT email)                                AS count FROM registered

  UNION ALL
  SELECT 2, 'Attended (Eco Day or Partner Day)',
    COUNT(DISTINCT r.email)
    FROM registered r JOIN attended a ON a.email = r.email

  UNION ALL
  SELECT 3, 'Had n8n Meeting',
    COUNT(DISTINCT r.email)
    FROM registered r JOIN meeting_booked m ON m.email = r.email

  UNION ALL
  SELECT 4, 'Account with Opp (NB/Exp, >= Oct 12)',
    COUNT(DISTINCT r.email)
    FROM registered r JOIN opp_accounts o ON o.account_id = r.account_id
    WHERE r.account_id IS NOT NULL

  UNION ALL
  SELECT 5, 'Closed Won',
    COUNT(DISTINCT r.email)
    FROM registered r JOIN closed_won_accounts cw ON cw.account_id = r.account_id
    WHERE r.account_id IS NOT NULL
)
ORDER BY n