"""Ticket sales from In The Loop Registrations · Pacing (Detailed).

Paid + Free only. Expired and Cancelled excluded. Last real day 2026-10-10.
Goal is 850 unique people. Hex App cells use these frames as native tables
so they can be restyled (bar / line / stacked area) without rewriting Plotly.
"""
from __future__ import annotations

import pandas as pd

TICKET_GOAL = 850
TICKET_CAMPAIGN_DAYS = 77
TICKET_SALES = """
2026-07-30,43,11,11,0,21,43
2026-07-31,17,19,11,0,30,60
2026-08-01,1,19,11,0,31,61
2026-08-02,3,19,11,0,34,64
2026-08-03,16,30,12,0,38,80
2026-08-04,12,34,14,0,43,91
2026-08-05,17,40,18,5,45,108
2026-08-06,11,45,18,7,48,118
2026-08-07,2,46,18,7,49,120
2026-08-08,0,46,18,7,49,120
2026-08-09,5,48,19,7,51,125
2026-08-10,4,49,19,7,54,129
2026-08-11,15,54,27,7,56,144
2026-08-12,3,54,27,7,59,147
2026-08-13,3,55,27,9,59,150
2026-08-14,30,57,31,13,78,179
2026-08-15,8,57,33,15,82,187
2026-08-16,5,58,34,15,85,192
2026-08-17,9,61,35,16,88,200
2026-08-18,12,69,37,16,90,212
2026-08-19,17,78,40,18,91,227
2026-08-20,20,92,44,19,92,245
2026-08-21,24,111,49,19,92,268
2026-08-22,1,111,49,19,93,269
2026-08-23,1,111,49,19,94,270
2026-08-24,5,113,51,20,94,275
2026-08-25,3,113,53,21,94,278
2026-08-26,10,114,59,21,96,287
2026-08-27,8,116,62,22,98,295
2026-08-28,22,117,62,22,114,310
2026-08-29,6,117,62,22,118,314
2026-08-30,1,117,62,22,119,315
2026-08-31,9,118,65,22,121,321
2026-09-01,18,122,71,22,127,337
2026-09-02,7,123,73,22,130,343
2026-09-03,7,126,73,23,131,348
2026-09-04,8,128,77,23,132,355
2026-09-05,1,128,78,23,132,356
2026-09-06,3,129,78,23,133,358
2026-09-07,10,135,82,23,133,367
2026-09-08,5,138,83,23,133,371
2026-09-09,9,145,85,23,133,380
2026-09-10,13,156,86,23,133,392
2026-09-11,11,164,88,23,133,402
2026-09-12,2,165,88,23,134,404
2026-09-13,0,165,88,23,134,404
2026-09-14,9,172,89,24,134,413
2026-09-15,18,185,91,24,135,429
2026-09-16,29,205,93,24,135,451
2026-09-17,97,231,159,24,136,544
2026-09-18,6,237,159,24,136,550
2026-09-19,5,242,159,24,136,555
2026-09-20,1,243,159,24,136,556
2026-09-21,23,257,162,24,138,574
2026-09-22,23,277,162,24,138,593
2026-09-23,15,291,163,24,138,607
2026-09-24,41,311,176,25,138,640
2026-09-25,24,327,183,25,138,661
2026-09-26,1,328,183,25,138,662
2026-09-27,1,328,183,25,139,663
2026-09-28,15,339,186,25,139,677
2026-09-29,30,355,190,25,139,697
2026-09-30,78,419,203,26,139,775
2026-10-01,42,450,205,26,140,808
2026-10-02,26,470,206,26,140,829
2026-10-03,2,471,206,26,141,831
2026-10-04,5,475,207,26,141,836
2026-10-05,39,502,211,27,141,866
2026-10-06,44,538,214,27,141,903
2026-10-07,6,544,214,27,141,909
2026-10-08,29,547,239,27,142,938
2026-10-09,3,550,239,27,142,941
2026-10-10,102,652,239,27,142,1043
"""


def ticket_sales() -> pd.DataFrame:
    rows = []
    running = 0
    for line in TICKET_SALES.strip().splitlines():
        day, daily, ga, exp, node, amb, people = line.split(",")
        daily_n = int(daily)
        running += daily_n
        rows.append(
            {
                "day": pd.Timestamp(day),
                "daily": daily_n,
                "registrations": running,
                "general_admission": int(ga),
                "expert_strategic": int(exp),
                "node_partners": int(node),
                "ambassadors": int(amb),
                "unique_people": int(people),
            }
        )
    frame = pd.DataFrame(rows)
    frame["pace_to_850"] = [
        round(TICKET_GOAL * (i + 1) / TICKET_CAMPAIGN_DAYS) for i in range(len(frame))
    ]
    return frame


def ticket_mix() -> pd.DataFrame:
    frame = ticket_sales()
    return frame[
        ["day", "general_admission", "expert_strategic", "node_partners", "ambassadors"]
    ].copy()


def ticket_vs_goal() -> pd.DataFrame:
    last = ticket_sales().iloc[-1]
    return pd.DataFrame(
        {
            "ticket_type": [
                "General Admission (Public)",
                "Expert + Strategic Partners",
                "Node Partners",
                "Ambassadors",
                "Total unique people",
                "Registrations (Paid + Free)",
            ],
            "target": [300, 250, 150, 150, TICKET_GOAL, pd.NA],
            "people": [
                int(last["general_admission"]),
                int(last["expert_strategic"]),
                int(last["node_partners"]),
                int(last["ambassadors"]),
                int(last["unique_people"]),
                int(last["registrations"]),
            ],
            "vs_target_pct": [
                round(100 * last["general_admission"] / 300),
                round(100 * last["expert_strategic"] / 250),
                round(100 * last["node_partners"] / 150),
                round(100 * last["ambassadors"] / 150),
                round(100 * last["unique_people"] / TICKET_GOAL),
                pd.NA,
            ],
        }
    )


def bq_ticket_sales_sql() -> str:
    structs = []
    for line in TICKET_SALES.strip().splitlines():
        day, daily, ga, exp, node, amb, people = line.split(",")
        structs.append(
            "  STRUCT(DATE '{day}' AS day, {daily} AS daily, {ga} AS general_admission, "
            "{exp} AS expert_strategic, {node} AS node_partners, {amb} AS ambassadors, "
            "{people} AS unique_people)".format(
                day=day,
                daily=int(daily),
                ga=int(ga),
                exp=int(exp),
                node=int(node),
                amb=int(amb),
                people=int(people),
            )
        )
    body = ",\n".join(structs)
    return f"""-- Ticket sales · In The Loop Registrations · Pacing (Detailed).
-- Paid + Free. Expired and Cancelled excluded. Last real day 2026-10-10.
-- Native Hex table: restyle in the App (bar / line / stacked area).
SELECT
  day,
  daily,
  SUM(daily) OVER (ORDER BY day) AS registrations,
  general_admission,
  expert_strategic,
  node_partners,
  ambassadors,
  unique_people,
  CAST(ROUND(850 * ROW_NUMBER() OVER (ORDER BY day) / 77) AS INT64) AS pace_to_850
FROM UNNEST([
{body}
])
ORDER BY day
"""


def bq_ticket_mix_sql() -> str:
    return """SELECT
  day,
  general_admission,
  expert_strategic,
  node_partners,
  ambassadors
FROM ticket_sales
ORDER BY day
"""


def bq_ticket_vs_goal_sql() -> str:
    return """WITH last AS (
  SELECT *
  FROM ticket_sales
  WHERE day = (SELECT MAX(day) FROM ticket_sales)
)
SELECT 'General Admission (Public)' AS ticket_type, 300 AS target, general_admission AS people,
  CAST(ROUND(100 * general_admission / 300) AS INT64) AS vs_target_pct
FROM last
UNION ALL
SELECT 'Expert + Strategic Partners', 250, expert_strategic,
  CAST(ROUND(100 * expert_strategic / 250) AS INT64)
FROM last
UNION ALL
SELECT 'Node Partners', 150, node_partners,
  CAST(ROUND(100 * node_partners / 150) AS INT64)
FROM last
UNION ALL
SELECT 'Ambassadors', 150, ambassadors,
  CAST(ROUND(100 * ambassadors / 150) AS INT64)
FROM last
UNION ALL
SELECT 'Total unique people', 850, unique_people,
  CAST(ROUND(100 * unique_people / 850) AS INT64)
FROM last
UNION ALL
SELECT 'Registrations (Paid + Free)', NULL, registrations, NULL
FROM last
"""


def _hex_loader() -> str:
    return f'''# Native Hex table. Restyle in the App with the chart icon (bar / line / stacked area).
import pandas as pd

TICKET_GOAL = {TICKET_GOAL}
TICKET_CAMPAIGN_DAYS = {TICKET_CAMPAIGN_DAYS}
TICKET_SALES = """{TICKET_SALES}"""


def _ticket_sales():
    rows = []
    running = 0
    for line in TICKET_SALES.strip().splitlines():
        day, daily, ga, exp, node, amb, people = line.split(",")
        daily_n = int(daily)
        running += daily_n
        rows.append(
            {{
                "day": pd.Timestamp(day),
                "daily": daily_n,
                "registrations": running,
                "general_admission": int(ga),
                "expert_strategic": int(exp),
                "node_partners": int(node),
                "ambassadors": int(amb),
                "unique_people": int(people),
            }}
        )
    frame = pd.DataFrame(rows)
    frame["pace_to_850"] = [
        round(TICKET_GOAL * (i + 1) / TICKET_CAMPAIGN_DAYS) for i in range(len(frame))
    ]
    return frame
'''


def hex_ticket_sales_code() -> str:
    return _hex_loader() + "\nticket_sales = _ticket_sales()\nticket_sales\n"


def hex_ticket_mix_code() -> str:
    return (
        _hex_loader()
        + """
ticket_sales_mix = _ticket_sales()[
    ["day", "general_admission", "expert_strategic", "node_partners", "ambassadors"]
].copy()
ticket_sales_mix
"""
    )


def hex_ticket_vs_goal_code() -> str:
    return (
        _hex_loader()
        + """
last = _ticket_sales().iloc[-1]
ticket_vs_goal = pd.DataFrame(
    {
        "ticket_type": [
            "General Admission (Public)",
            "Expert + Strategic Partners",
            "Node Partners",
            "Ambassadors",
            "Total unique people",
            "Registrations (Paid + Free)",
        ],
        "target": [300, 250, 150, 150, TICKET_GOAL, pd.NA],
        "people": [
            int(last["general_admission"]),
            int(last["expert_strategic"]),
            int(last["node_partners"]),
            int(last["ambassadors"]),
            int(last["unique_people"]),
            int(last["registrations"]),
        ],
        "vs_target_pct": [
            round(100 * last["general_admission"] / 300),
            round(100 * last["expert_strategic"] / 250),
            round(100 * last["node_partners"] / 150),
            round(100 * last["ambassadors"] / 150),
            round(100 * last["unique_people"] / TICKET_GOAL),
            pd.NA,
        ],
    }
)
ticket_vs_goal
"""
    )

