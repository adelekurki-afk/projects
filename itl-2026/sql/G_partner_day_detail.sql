-- ============================================================
-- PARTNER DAY BREAKDOWN
-- Partner Day: ticket type contains 'partner' (case-insensitive)
-- Both days: partner ticket + day2 flag = TRUE
-- Ecosystem only: no partner ticket, day2 = TRUE
-- ============================================================
SELECT
  CASE
    WHEN is_partner AND day1 AND day2     THEN 'Both Days (Partner + Ecosystem)'
    WHEN is_partner AND day1 AND NOT day2 THEN 'Partner Day Only'
    WHEN NOT is_partner AND day2          THEN 'Ecosystem Day Only'
    ELSE 'Other'
  END                                           AS attendance_type,
  segment,
  country,
  COUNT(*)                                      AS registrant_count,
  COUNTIF(redeemed)                             AS attended_count,
  ROUND(100.0 * COUNTIF(redeemed) / COUNT(*), 1) AS attendance_rate_pct
FROM `n8n-telemetry.itl_2026_snapshots.registrants`
GROUP BY 1, 2, 3
ORDER BY 1, attendance_rate_pct DESC