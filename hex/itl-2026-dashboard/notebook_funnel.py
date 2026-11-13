from IPython.display import display, HTML

# Self-contained Salesforce funnel. App runs top-to-bottom; SQL later in the
# notebook is not available here. Numbers from BQ on 13 Nov 2026 (Europe/Madrid).

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


def _euro(n):
    try:
        n = float(n)
    except Exception:
        n = 0
    if abs(n) >= 1_000_000:
        return f"€{n / 1_000_000:.2f}M"
    if abs(n) >= 10_000:
        return f"€{n / 1_000:.0f}k"
    return f"€{int(round(n)):,}"


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


funnel_rows = [
    ("Registered", 1119, 100.0),
    ("Attended (Eco Day or Partner Day)", 837, 74.8),
    ("Had n8n Meeting", 20, 1.8),
    ("Account with Opp (NB/Exp, >= Oct 12)", 70, 6.3),
    ("Closed Won", 6, 0.5),
]
try:
    funnel_rows = [
        (str(r["stage"]), int(r["count"]), float(r["pct_of_registered"]))
        for _, r in lead_funnel.iterrows()
    ]
except Exception:
    pass

sdr_rows = [("Not set", 25, 1851340), ("Human SDR", 4, 166000), ("Web", 1, 26000)]
try:
    sdr_rows = [
        (str(r["sdr_path"]), int(r["opp_count"]), float(r["amount"]))
        for _, r in itl_funnel_sdr.iterrows()
    ]
except Exception:
    pass

stage_rows = [
    ("Sourced", "Value Workshop", 6),
    ("Sourced", "Meeting Booked", 4),
    ("Sourced", "Stakeholder Alignment", 1),
    ("Sourced", "Closed Won Approved", 1),
    ("Influenced", "Meeting Booked", 7),
    ("Influenced", "Value Workshop", 6),
    ("Influenced", "Stakeholder Alignment", 2),
    ("Influenced", "Closed Won Approved", 2),
    ("Influenced", "Discovery", 1),
]
try:
    stage_rows = [
        (
            "Influenced" if str(r["bucket"]).startswith("Influenced") else str(r["bucket"]),
            str(r["stage"]),
            int(r["opp_count"]),
        )
        for _, r in funnel_stages.iterrows()
        if str(r["bucket"]) != "Renewal touched"
    ]
except Exception:
    pass

sourced = [
    ("Kongsberg Satellite Services AS", "Expansion", "Value Workshop", 215000, "MM"),
    ("Boston Consulting Group, Inc.", "Expansion", "Value Workshop", 200000, "ENT"),
    ("TeamViewer GmbH", "New Business", "Value Workshop", 196700, "MM"),
    ("N3 Engine Overhaul Services", "New Business", "Value Workshop", 113900, "MM"),
    ("Eleven Labs Inc.", "Expansion", "Value Workshop", 80000, "MM"),
    ("Trade Republic", "Expansion", "Value Workshop", 60000, "MM"),
    ("Retail Logistics Excellence - Relex Oy", "Expansion", "Stakeholder Alignment", 56000, "MM"),
    ("Next PLC", "Expansion", "Meeting Booked", 55000, "ENT"),
    ("SEFE", "New Business", "Meeting Booked", 28000, "MM"),
    ("RENOLIT SE", "New Business", "Closed Won Approved", 6400, "Unknown"),
    ("ECTIVE Automation", "New Business", "Meeting Booked", 0, "SMB"),
    ("Moonspring AI", "New Business", "Meeting Booked", 0, "SMB"),
]
influenced = [
    ("NVIDIA", "New Business", "Meeting Booked", 700000, "ENT"),
    ("Solaris SE", "New Business", "Stakeholder Alignment", 86000, "MM"),
    ("Rohde & Schwarz GmbH & Co. KG", "New Business", "Meeting Booked", 55000, "ENT"),
    ("Volkswagen AG", "New Business", "Meeting Booked", 55000, "ENT"),
    ("STX Next S.A.", "New Business", "Meeting Booked", 28000, "MM"),
    ("EngageTech", "New Business", "Meeting Booked", 28000, "MM"),
    ("Graphwise", "Expansion", "Stakeholder Alignment", 26701, "MM"),
    ("C Digital Technologies Limited", "New Business", "Value Workshop", 26000, "MM"),
    ("voize", "New Business", "Value Workshop", 26000, "MM"),
    ("HiSolutions AG", "New Business", "Value Workshop", 26000, "MM"),
    ("Cornelsen", "New Business", "Value Workshop", 26000, "MM"),
    ("Apaleo", "New Business", "Closed Won Approved", 22000, "MM"),
    ("Blue Light Card", "Expansion", "Value Workshop", 20000, "MM"),
    ("Deutsche Telekom MMS GmbH", "New Business", "Discovery", 16000, "ENT"),
    ("Moss", "New Business", "Value Workshop", 15000, "MM"),
    ("Delivery Hero", "Expansion", "Meeting Booked", 11150, "ENT"),
    ("Globalization Partners LLC", "Expansion", "Closed Won Approved", 3640, "MM"),
    ("Rakuten", "New Business", "Meeting Booked", 0, "ENT"),
]
won = [row for row in sourced + influenced if row[2].startswith("Closed Won")]

try:
    src_df = itl_sourced_influenced_opps
    sourced = [
        (str(r["account_name"]), str(r["opp_type"]), str(r["StageName"]), float(r["amount"]), str(r["segment"]))
        for _, r in src_df[src_df["attribution"] == "Sourced"].iterrows()
    ]
    inf_mask = src_df["attribution"].astype(str).str.startswith("Influenced")
    influenced = [
        (str(r["account_name"]), str(r["opp_type"]), str(r["StageName"]), float(r["amount"]), str(r["segment"]))
        for _, r in src_df[inf_mask].iterrows()
    ]
    won = [
        (str(r["account_name"]), str(r["opp_type"]), str(r["StageName"]), float(r["amount"]), str(r["segment"]))
        for _, r in src_df[src_df["status"] == "Closed won"].iterrows()
        if not str(r["attribution"]).startswith("Renewal")
    ]
except Exception:
    pass

src_n, src_amt, src_won_n, src_won = 12, 1011000, 1, 6400
inf_n, inf_amt, inf_won_n, inf_won = 18, 1170491, 2, 25640
try:
    for _, r in itl_attribution_kpis.iterrows():
        bucket = str(r["bucket"])
        if bucket == "Sourced":
            src_n, src_amt, src_won_n, src_won = int(r["opp_count"]), float(r["amount"]), int(r["won_count"]), float(r["won_amount"])
        elif bucket == "Influenced":
            inf_n, inf_amt, inf_won_n, inf_won = int(r["opp_count"]), float(r["amount"]), int(r["won_count"]), float(r["won_amount"])
except Exception:
    pass

pipe_total, pipe_open, pipe_won, pipe_opps, pipe_won_n = 2461063, 2427423, 33640, 29, 3
try:
    pipe_total = int(round(float(pipeline_arr["total_amount"].sum())))
    pipe_open = int(round(float(pipeline_arr["open_pipeline_amount"].sum())))
    pipe_won = int(round(float(pipeline_arr["closed_won_amount"].sum())))
    pipe_opps = int(pipeline_arr["opp_count"].sum())
    pipe_won_n = int(pipeline_arr["closed_won_count"].sum())
except Exception:
    pass


def _opp_rows(rows):
    return [
        (account, opp_type, stage, _euro(amount), segment)
        for account, opp_type, stage, amount, segment in rows
    ]


body = f"""
<div class="itl">
  <h2>Leads progression{_c("h2")}
  {_table(
      ["Stage", "People", "% of registered"],
      [(s, f"{c:,}", f"{p:.1f}%") for s, c, p in funnel_rows],
      "70 is people on an account with a NB/Expansion opp created from 12 Oct, not 70 opportunities.",
  )}
  <h2>Sourced vs influenced{_c("h2")}
  {_table(
      ["Bucket", "Opps", "Amount", "Won"],
      [
          ("Sourced", f"{src_n}", _euro(src_amt), f"{src_won_n} · {_euro(src_won)}"),
          ("Influenced", f"{inf_n}", _euro(inf_amt), f"{inf_won_n} · {_euro(inf_won)}"),
          ("NB + Expansion pipeline", f"{pipe_opps}", _euro(pipe_total), f"{pipe_won_n} · {_euro(pipe_won)}"),
      ],
      f"Open pipeline {_euro(pipe_open)}. No Partner-typed opportunities — net new is New Business.",
  )}
  <h2>First meeting source{_c("h2")}
  {_table(
      ["Path", "Opps", "Amount"],
      [(name, f"{n}", _euro(amt)) for name, n, amt in sdr_rows],
      "ITL sourced + influenced NB/Expansion deals. AI SDR (Freddy) is not set on these 30.",
  )}
  <h2>Opportunities per Salesforce stage{_c("h2")}
  {_table(
      ["Attribution", "Stage", "Opps"],
      [(b, s, f"{n}") for b, s, n in stage_rows],
  )}
  <h2>Opportunities sourced · {len(sourced)}{_c("h2")}
  {_table(["Account", "Type", "Stage", "Amount", "Segment"], _opp_rows(sourced))}
  <h2>Opportunities influenced · {len(influenced)}{_c("h2")}
  {_table(["Account", "Type", "Stage", "Amount", "Segment"], _opp_rows(influenced))}
  <h2>Closed won on this list · {len(won)}{_c("h2")}
  {_table(["Account", "Type", "Stage", "Amount", "Segment"], _opp_rows(won))}
{_c("div")}
"""
display(HTML("<style>" + ITL_CSS + _c("style") + body))
