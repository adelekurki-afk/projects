-- Locked Fliplet visits. Not Salesforce Attended.
SELECT * FROM UNNEST([
  STRUCT('Came · Partner Day' AS metric, 426 AS people, '13 Oct · 391 door + 35 badge' AS how_built),
  STRUCT('Came · Ecosystem Day', 916, '14 Oct · 878 door + 38 green YES'),
  STRUCT('Unique people', 1018, '426 + 916 − 324 both days'),
  STRUCT('Both days', 324, 'Inside both 426 and 916'),
  STRUCT('Partner only', 102, 'Monday not Tuesday'),
  STRUCT('Ecosystem only', 592, 'Tuesday not Monday'),
  STRUCT('Staff tickets', 113, 'Overlay, not extra headcount'),
  STRUCT('Programme speakers', 116, 'Overlay, not extra headcount'),
  STRUCT('CAB overlay', 39, '11 members · 28 guests')
])
