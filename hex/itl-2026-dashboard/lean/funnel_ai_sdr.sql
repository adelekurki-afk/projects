-- first_meeting_source on opportunities created from 1 Jul 2026 (covers Solaris-style existing-open).
-- Join to itl_sourced_influenced_opps in Python. AI Handoff* = Freddy.
SELECT
  opportunity_id AS opp_id,
  COALESCE(first_meeting_source, '(not set)') AS first_meeting_source,
  CASE
    WHEN first_meeting_source LIKE 'AI Handoff%' THEN 'AI SDR (Freddy)'
    WHEN first_meeting_source = 'SDR Handoff' THEN 'Human SDR'
    WHEN first_meeting_source = 'Web' THEN 'Web'
    ELSE 'Not set'
  END AS sdr_path
FROM `n8n-telemetry.marts.fct_opportunities`
WHERE DATE(created_at) BETWEEN '2026-07-01' AND '2026-11-12'
