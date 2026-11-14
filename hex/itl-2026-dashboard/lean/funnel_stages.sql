-- ITL sourced + influenced opportunities by Salesforce stage.
SELECT
  CASE
    WHEN attribution LIKE 'Influenced%' THEN 'Influenced'
    ELSE attribution
  END AS bucket,
  StageName AS stage,
  COUNT(*) AS opp_count,
  ROUND(SUM(amount), 0) AS amount,
  SUM(CASE WHEN status = 'Closed won' THEN 1 ELSE 0 END) AS closed_won
FROM itl_sourced_influenced_opps
GROUP BY 1, 2
ORDER BY bucket, opp_count DESC
