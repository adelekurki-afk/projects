-- Partner Day top-level summary (matches the brief)
SELECT
  CASE
    WHEN is_partner AND day1 AND day2     THEN 'Both Days (Partner + Ecosystem)'
    WHEN is_partner AND day1 AND NOT day2 THEN 'Partner Day Only'
    WHEN NOT is_partner AND day2          THEN 'Ecosystem Day Only'
    ELSE 'Other'
  END AS attendance_type,
  COUNT(*)       AS registrant_count,
  COUNTIF(redeemed) AS attended_count
FROM `n8n-telemetry.itl_2026_snapshots.registrants`
GROUP BY 1
ORDER BY 1