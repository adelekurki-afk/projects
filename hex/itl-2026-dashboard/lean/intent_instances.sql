-- Weekly acquired instances by deployment type (Cloud vs self-hosted / Command line).
-- acquired_at = first UI activity, not cloud signup (acquisition.md).
SELECT
  DATE_TRUNC(acquired_at, WEEK(MONDAY)) AS week_start,
  COALESCE(deployment_type, 'Unknown') AS deployment_type,
  COUNT(*) AS acquired_instances
FROM `n8n-telemetry.computed.instances`
WHERE acquired IS TRUE
  AND DATE(acquired_at) BETWEEN '2026-06-01' AND '2026-11-08'
GROUP BY 1, 2
ORDER BY 1, 2
