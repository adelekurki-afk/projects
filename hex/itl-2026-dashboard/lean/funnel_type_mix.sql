-- Expansion, Partner, net-new pipeline and closed on ITL sourced + influenced.
SELECT
  CASE
    WHEN attribution LIKE 'Influenced%' THEN 'Influenced'
    ELSE attribution
  END AS bucket,
  COALESCE(opp_type, 'Unknown') AS opp_type,
  COUNT(*) AS opp_count,
  ROUND(SUM(amount), 0) AS amount,
  ROUND(SUM(CASE WHEN status = 'Open' THEN amount ELSE 0 END), 0) AS open_amount,
  ROUND(SUM(CASE WHEN status = 'Closed won' THEN amount ELSE 0 END), 0) AS won_amount,
  SUM(CASE WHEN status = 'Closed won' THEN 1 ELSE 0 END) AS won_count
FROM itl_sourced_influenced_opps
GROUP BY 1, 2
ORDER BY bucket, amount DESC
