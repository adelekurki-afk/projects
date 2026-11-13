from IPython.display import display, HTML

ITL_CSS = """
.itl { font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color:#111827; max-width: 920px; }
.itl h2 { font-size: 18px; font-weight: 700; margin: 28px 0 8px; letter-spacing: -0.01em; }
.itl h2:first-child { margin-top: 4px; }
.itl p { font-size: 14px; line-height: 1.55; color: #4B5563; margin: 0 0 12px; }
.itl table { width: 100%; border-collapse: collapse; font-size: 13px; margin: 0 0 4px; }
.itl th { text-align: left; font-weight: 600; color: #6B7280; padding: 8px 12px 8px 0; border-bottom: 1px solid #E5E7EB; }
.itl td { padding: 8px 12px 8px 0; border-bottom: 1px solid #F3F4F6; }
.itl th.n, .itl td.n { text-align: right; font-variant-numeric: tabular-nums; padding-right: 0; }
.itl .cap { font-size: 13px; color: #6B7280; margin: 4px 0 20px; }
"""


def _itl_int(value, default):
    try:
        if value is None:
            return default
        return int(value)
    except Exception:
        return default


def _euro(n):
    n = int(round(float(n)))
    if n >= 1_000_000:
        return f"€{n / 1_000_000:.2f}M"
    if abs(n) >= 10_000:
        return f"€{n / 1_000:.0f}k"
    return f"€{n:,}"


def _c(tag):
    return "<" + "/" + tag + ">"


def _table(headers, rows, caption=""):
    head = []
    for i, h in enumerate(headers):
        head.append(f'<th class="n">{h}{_c("th")}' if i else f"<th>{h}{_c('th')}")
    body = []
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            cls = ' class="n"' if i else ""
            cells.append(f"<td{cls}>{cell}{_c('td')}")
        body.append("<tr>" + "".join(cells) + _c("tr"))
    cap = f'<p class="cap">{caption}{_c("p")}' if caption else ""
    return "<table><tr>" + "".join(head) + _c("tr") + "".join(body) + _c("table") + cap


_STAGE_SHORT = {
    "Registered": "Registered",
    "Attended (Eco Day or Partner Day)": "Attended",
    "Had n8n Meeting": "Meeting booked",
    "Account with Opp (NB/Exp, >= Oct 12)": "Opportunity",
    "Closed Won": "Closed Won",
}
funnel = [
    ("Registered", 1119, 100.0),
    ("Attended", 837, 74.8),
    ("Meeting booked", 20, 1.8),
    ("Opportunity", 70, 6.3),
    ("Closed Won", 6, 0.5),
]
try:
    funnel = [
        (
            _STAGE_SHORT.get(str(r["stage"]), str(r["stage"])),
            _itl_int(r["count"], 0),
            float(r["pct_of_registered"]),
        )
        for _, r in lead_funnel.iterrows()
    ]
except Exception:
    pass

pipe_total, pipe_open, pipe_won = 2461063, 2427423, 33640
pipe_opps, pipe_won_n, pipe_open_n, pipe_meetings = 29, 3, 26, 1
pipe_mix = [
    ("New Business", "ENT", 5, 834000, 826000, 8000),
    ("New Business", "MM", 12, 619200, 597200, 22000),
    ("Expansion", "ENT", 4, 516150, 516150, 0),
    ("Expansion", "MM", 8, 491713, 488073, 3640),
]
try:
    df = pipeline_arr
    pipe_total = int(round(float(df["total_amount"].sum())))
    pipe_open = int(round(float(df["open_pipeline_amount"].sum())))
    pipe_won = int(round(float(df["closed_won_amount"].sum())))
    pipe_opps = int(df["opp_count"].sum())
    pipe_won_n = int(df["closed_won_count"].sum())
    pipe_open_n = int(df["open_opp_count"].sum())
    if "opps_from_meetings" in df.columns:
        pipe_meetings = int(df["opps_from_meetings"].sum())
    pipe_mix = [
        (
            str(r["opp_type"]),
            str(r["segment"]),
            _itl_int(r["opp_count"], 0),
            float(r["total_amount"]),
            float(r["open_pipeline_amount"]),
            float(r["closed_won_amount"]),
        )
        for _, r in df.iterrows()
    ]
except Exception:
    pass

body = f"""
<div class="itl">
  <h2>Visits{_c("h2")}
  {_table(
      ["Metric", "People", "How built"],
      [
          ("Registered", "1,269", "Paid + Free unique email"),
          ("Came · Partner Day", "426", "13 Oct · 391 door + 35 badge"),
          ("Came · Ecosystem Day", "916", "14 Oct · 878 door + 38 green YES"),
          ("Unique people", "1,018", "426 + 916 − 324 both days"),
          ("Staff tickets", "113", "Overlay, not extra headcount"),
          ("Programme speakers", "116", "Overlay, not extra headcount"),
          ("CAB overlay", "39", "11 members · 28 guests"),
      ],
      "Locked Fliplet counts. People who came both days are in both 426 and 916.",
  )}
  <h2>Salesforce conversion{_c("h2")}
  {_table(
      ["Stage", "People", "% of registered"],
      [(name, f"{count:,}", f"{pct:.1f}%") for name, count, pct in funnel],
      "Free/Paid CampaignMember, not Fliplet 1,269 / 426 / 916.",
  )}
  <h2>Opportunities{_c("h2")}
  {_table(
      ["Type / segment", "Opps", "Total", "Open", "Won"],
      [
          (f"{opp_type} / {segment}", f"{n_opps}", _euro(total), _euro(open_amt), _euro(won_amt))
          for opp_type, segment, n_opps, total, open_amt, won_amt in pipe_mix
      ],
      f"{pipe_opps} NB + Expansion from 12 Oct · {_euro(pipe_total)} total · {_euro(pipe_open)} open · {_euro(pipe_won)} won ({pipe_won_n} deals). {pipe_meetings} from meetings booked.",
  )}
{_c("div")}
"""
display(HTML("<style>" + ITL_CSS + _c("style") + body))
