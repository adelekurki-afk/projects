-- YouTube views earned and n8n-related videos published, weekly.
-- Views per day are reliable from 2026-07-01 (YouTube guide).
WITH views AS (
  SELECT
    DATE_TRUNC(snapshot_date, WEEK(MONDAY)) AS week_start,
    SUM(views_gained) AS views_gained
  FROM `n8n-telemetry.marts.fct_youtube_video_daily_stats`
  WHERE snapshot_date BETWEEN '2026-07-01' AND '2026-11-08'
  GROUP BY 1
),
created AS (
  SELECT
    DATE_TRUNC(DATE(uploaded_at), WEEK(MONDAY)) AS week_start,
    COUNT(*) AS videos_published,
    COUNTIF(is_n8n_related IS TRUE) AS n8n_videos_published
  FROM `n8n-telemetry.marts.dim_youtube_video`
  WHERE DATE(uploaded_at) BETWEEN '2026-06-01' AND '2026-11-08'
  GROUP BY 1
)
SELECT
  COALESCE(v.week_start, c.week_start) AS week_start,
  v.views_gained,
  c.videos_published,
  c.n8n_videos_published
FROM views v
FULL OUTER JOIN created c USING (week_start)
ORDER BY week_start
