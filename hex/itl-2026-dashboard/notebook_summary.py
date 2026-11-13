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
pipe_opps, pipe_won_n = 29, 3
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

src_n, src_amt, src_won, src_won_n = 12, 1011000, 6400, 1
inf_n, inf_amt, inf_won, inf_won_n = 18, 1170491, 25640, 2
try:
    for _, r in itl_attribution_kpis.iterrows():
        bucket = str(r["bucket"])
        if bucket == "Sourced":
            src_n = _itl_int(r["opp_count"], src_n)
            src_amt = float(r["amount"])
            src_won = float(r["won_amount"])
            src_won_n = _itl_int(r["won_count"], src_won_n)
        elif bucket == "Influenced":
            inf_n = _itl_int(r["opp_count"], inf_n)
            inf_amt = float(r["amount"])
            inf_won = float(r["won_amount"])
            inf_won_n = _itl_int(r["won_count"], inf_won_n)
except Exception:
    pass

type_rows = []
try:
    for _, r in funnel_type_mix.iterrows():
        type_rows.append(
            (
                str(r["bucket"]),
                str(r["opp_type"]),
                _itl_int(r["opp_count"], 0),
                float(r["amount"]),
                float(r["open_amount"]),
                float(r["won_amount"]),
            )
        )
except Exception:
    type_rows = [
        ("Sourced", "Expansion", 6, 666000, 666000, 0),
        ("Sourced", "New Business", 6, 345000, 338600, 6400),
        ("Influenced", "New Business", 14, 1109000, 1087000, 22000),
        ("Influenced", "Expansion", 4, 61491, 57851, 3640),
    ]

body = f"""
<div class="itl">
  <h2>Participants per day{_c("h2")}
  {_table(
      ["Metric", "People", "Note"],
      [
          ("Registered", "1,269", "Paid + Free unique email"),
          ("Partner Day", "426", "13 Oct · 87% of 487 tickets"),
          ("Ecosystem Day", "916", "14 Oct · 76% of 1,205 tickets"),
          ("Unique people", "1,018", "324 came both days"),
          ("Staff tickets", "113", "Inside 426 / 916, not extra"),
          ("Speakers", "116", "Programme overlay"),
          ("CAB", "39", "11 members · 28 guests"),
      ],
      "Fliplet visits. Unique attendance is 80% of 1,269 registered.",
  )}
  <h2>Full funnel · Salesforce{_c("h2")}
  {_table(
      ["Stage", "People", "% of registered"],
      [(name, f"{count:,}", f"{pct:.1f}%") for name, count, pct in funnel],
      "Free/Paid registered is not Fliplet 1,269. Attended is not 426 / 916.",
  )}
  <h2>Sourced vs influenced{_c("h2")}
  {_table(
      ["Bucket", "Opps", "Total", "Won"],
      [
          ("Sourced opps", f"{src_n}", _euro(src_amt), f"{src_won_n} · {_euro(src_won)}"),
          ("Influenced", f"{inf_n}", _euro(inf_amt), f"{inf_won_n} · {_euro(inf_won)}"),
          ("NB + Expansion", f"{pipe_opps}", _euro(pipe_total), f"{pipe_won_n} · {_euro(pipe_won)}"),
      ],
      "No Partner-typed opportunities — net new is New Business. Full lists are on the Funnel tab.",
  )}
  {_table(
      ["Attribution", "Type", "Opps", "Total", "Open", "Won"],
      [
          (bucket, opp_type, f"{n_opps}", _euro(total), _euro(open_amt), _euro(won_amt))
          for bucket, opp_type, n_opps, total, open_amt, won_amt in type_rows
      ],
  )}
  <h2>NB + Expansion by segment{_c("h2")}
  {_table(
      ["Type / segment", "Opps", "Total", "Open", "Won"],
      [
          (f"{opp_type} / {segment}", f"{n_opps}", _euro(total), _euro(open_amt), _euro(won_amt))
          for opp_type, segment, n_opps, total, open_amt, won_amt in pipe_mix
      ],
  )}
{_c("div")}
"""
display(HTML("<style>" + ITL_CSS + _c("style") + body))
