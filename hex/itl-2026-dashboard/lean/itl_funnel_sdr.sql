-- ITL sourced + influenced NB/Expansion opportunities by first_meeting_source.
-- IDs from itl_sourced_influenced_opps as of 2026-11-13 (exclude Renewal touched).
SELECT
  CASE
    WHEN first_meeting_source LIKE 'AI Handoff%' THEN 'AI SDR (Freddy)'
    WHEN first_meeting_source = 'SDR Handoff' THEN 'Human SDR'
    WHEN first_meeting_source = 'Web' THEN 'Web'
    ELSE 'Not set'
  END AS sdr_path,
  COUNT(*) AS opp_count,
  ROUND(SUM(amount_eur), 0) AS amount
FROM `n8n-telemetry.marts.fct_opportunities`
WHERE opportunity_id IN (
  '006cj00001xXsqLAAS','006cj00001sdWBiAAM','006cj00001qZGkzAAG','006cj00001qoGkgAAE',
  '006cj00001rkpzlAAA','006cj00001yywNpAAI','006cj00001ufWT0AAM','006cj00001wWKHpAAO',
  '006cj00001zfJ5UAAU','006cj00001zEcEfAAK','006cj00001nucnTAAQ','006cj00001nekSPAAY',
  '006cj00001v7pR3AAI','006cj00001w7P31AAE','006cj00001yqfaHAAQ','006cj00001zXuPaAAK',
  '006cj00001wV1fSAAS','006cj00001yaUHRAA2','006cj00001qV5mXAAS','006cj00001ugGFhAAM',
  '006cj00001sHftZAAS','006cj00001yWUb0AAG','006cj00001seDi6AAE','006cj00001zCrIfAAK',
  '006cj00001wBuhkAAC','006cj00001ypfPSAAY','006cj00001zFeBCAA0','006cj00001uNKtLAAW',
  '006cj00001zF1TBAA0','006cj00001MgR9tAAF'
)
GROUP BY 1
ORDER BY opp_count DESC
