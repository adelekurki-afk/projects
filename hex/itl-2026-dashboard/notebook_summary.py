from IPython.display import display, HTML

ITL_CSS = """
.itl-dash { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color:#111827; max-width: 1100px; }
.itl-kicker { font-size:12px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:#FF6D5A; margin:0 0 6px 0; }
.itl-title { font-size:28px; font-weight:700; margin:0 0 6px 0; }
.itl-sub { font-size:14px; color:#6B7280; margin:0 0 22px 0; }
.itl-ch { font-size:13px; font-weight:700; letter-spacing:.06em; text-transform:uppercase; color:#6B7280; margin:28px 0 12px 0; padding-top:18px; border-top:1px solid #E5E7EB; }
.itl-ch:first-of-type { border-top:none; margin-top:8px; padding-top:0; }
.itl-strip { display:grid; grid-template-columns:repeat(4, minmax(140px, 1fr)); gap:12px; margin:0 0 16px 0; }
.itl-tile { border:1px solid #E5E7EB; border-radius:10px; background:#fff; padding:16px 18px 14px; }
.itl-val { font-size:32px; font-weight:700; color:#111827; line-height:1.1; font-variant-numeric:tabular-nums; }
.itl-val.accent { color:#FF6D5A; }
.itl-label { margin-top:8px; font-size:13px; color:#6B7280; font-weight:600; }
.itl-hint { margin-top:4px; font-size:11px; color:#9CA3AF; }
.itl-cwrap { border:1px solid #E5E7EB; border-radius:10px; padding:16px 18px 12px; margin:0 0 16px 0; background:#fff; }
.itl-crow { display:grid; grid-template-columns:160px 1fr 130px; gap:10px; align-items:center; margin:7px 0; font-size:13px; }
.itl-tbl { width:100%; border-collapse:collapse; font-size:13px; }
.itl-tbl th { text-align:left; color:#6B7280; font-weight:600; padding:6px 8px; border-bottom:1px solid #E5E7EB; }
.itl-tbl th.num { text-align:right; }
.itl-tbl td { padding:7px 8px; border-bottom:1px solid #F3F4F6; }
.itl-tbl td.num { text-align:right; font-variant-numeric:tabular-nums; font-weight:600; }
.itl-cname { color:#374151; }
.itl-cbar { background:#F3F4F6; border-radius:4px; height:10px; overflow:hidden; }
.itl-cbar span { display:block; height:100%; border-radius:4px; }
.itl-cnum { text-align:right; font-variant-numeric:tabular-nums; font-weight:600; color:#111827; font-size:12px; }
.itl-note { margin-top:8px; font-size:13px; color:#6B7280; padding:12px 14px; background:#F9FAFB; border:1px solid #E5E7EB; border-radius:8px; }
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


_STAGE_SHORT = {
    "Registered": "Registered",
    "Attended (Eco Day or Partner Day)": "Attended",
    "Had n8n Meeting": "Meeting booked",
    "Account with Opp (NB/Exp, >= Oct 12)": "Opportunity",
    "Closed Won": "Closed Won",
}
funnel = [
    ("Registered", 1118, 100.0),
    ("Attended", 835, 74.7),
    ("Meeting booked", 20, 1.8),
    ("Opportunity", 57, 5.1),
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
funnel_max = max((c for _, c, _ in funnel), default=1)

pipe_total, pipe_open, pipe_won = 2421913, 2388273, 33640
pipe_opps, pipe_won_n, pipe_open_n, pipe_meetings = 27, 3, 24, 1
pipe_mix = [
    ("New Business", "ENT", 5, 834000, 826000, 8000),
    ("New Business", "MM", 11, 591200, 569200, 22000),
    ("Expansion", "ENT", 3, 505000, 505000, 0),
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

src_n, src_amt, src_won, src_won_n = 11, 983000, 6400, 1
inf_n, inf_amt, inf_won, inf_won_n = 16, 1131341, 25640, 2
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
        ("Sourced", "New Business", 5, 317000, 310600, 6400),
        ("Influenced", "New Business", 13, 1081000, 1059000, 22000),
        ("Influenced", "Expansion", 3, 50341, 46701, 3640),
    ]

funnel_rows = []
for name, count, pct in funnel:
    width = 100.0 * count / funnel_max if funnel_max else 0
    funnel_rows.append(
        f'<div class="itl-crow"><div class="itl-cname">{name}</div>'
        f'<div class="itl-cbar"><span style="width:{width:.1f}%;background:#FF6D5A"></span></div>'
        f'<div class="itl-cnum">{count:,} · {pct:.1f}%</div></div>'
    )
funnel_html = "\n".join(funnel_rows)

mix_rows = []
for opp_type, segment, n_opps, total, open_amt, won_amt in pipe_mix:
    mix_rows.append(
        "<tr>"
        f"<td>{opp_type} / {segment}</td>"
        f'<td class="num">{n_opps}</td>'
        f'<td class="num">{_euro(total)}</td>'
        f'<td class="num">{_euro(open_amt)}</td>'
        f'<td class="num">{_euro(won_amt)}</td>'
        "</tr>"
    )
mix_html = "\n".join(mix_rows)

attr_rows = []
for bucket, opp_type, n_opps, total, open_amt, won_amt in type_rows:
    attr_rows.append(
        "<tr>"
        f"<td>{bucket}</td><td>{opp_type}</td>"
        f'<td class="num">{n_opps}</td>'
        f'<td class="num">{_euro(total)}</td>'
        f'<td class="num">{_euro(open_amt)}</td>'
        f'<td class="num">{_euro(won_amt)}</td>'
        "</tr>"
    )
attr_html = "\n".join(attr_rows)

body = f"""
<div class="itl-dash">
  <div class="itl-kicker">In the Loop 2026</div>
  <h1 class="itl-title">Summary</h1>
  <p class="itl-sub">Participants, staff overlays, attendance rate, full funnel, sourced vs influenced, net-new vs expansion.</p>

  <div class="itl-ch">Participants per day</div>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val">1,269</div><div class="itl-label">Registered</div><div class="itl-hint">Paid + Free unique email</div></div>
    <div class="itl-tile"><div class="itl-val accent">426</div><div class="itl-label">Partner Day</div><div class="itl-hint">13 Oct · 87% of 487 tickets</div></div>
    <div class="itl-tile"><div class="itl-val accent">916</div><div class="itl-label">Ecosystem Day</div><div class="itl-hint">14 Oct · 76% of 1,205 tickets</div></div>
    <div class="itl-tile"><div class="itl-val">1,018</div><div class="itl-label">Unique people</div><div class="itl-hint">324 came both days</div></div>
  </div>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val">113</div><div class="itl-label">Staff tickets</div><div class="itl-hint">Inside 426 / 916, not extra</div></div>
    <div class="itl-tile"><div class="itl-val">116</div><div class="itl-label">Speakers</div><div class="itl-hint">Programme overlay</div></div>
    <div class="itl-tile"><div class="itl-val">39</div><div class="itl-label">CAB</div><div class="itl-hint">11 members · 28 guests</div></div>
    <div class="itl-tile"><div class="itl-val accent">80%</div><div class="itl-label">Unique attendance</div><div class="itl-hint">1,018 of 1,269 registered</div></div>
  </div>

  <div class="itl-ch">Full funnel · Salesforce</div>
  <p class="itl-sub" style="margin-bottom:10px">Free/Paid registered is not Fliplet 1,269. Attended is not 426 / 916.</p>
  <div class="itl-cwrap">{funnel_html}</div>

  <div class="itl-ch">Sourced vs influenced</div>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val accent">{src_n}</div><div class="itl-label">Sourced opps</div><div class="itl-hint">{_euro(src_amt)} · {src_won_n} won {_euro(src_won)}</div></div>
    <div class="itl-tile"><div class="itl-val">{inf_n}</div><div class="itl-label">Influenced opps</div><div class="itl-hint">{_euro(inf_amt)} · {inf_won_n} won {_euro(inf_won)}</div></div>
    <div class="itl-tile"><div class="itl-val">{_euro(pipe_total)}</div><div class="itl-label">NB + Expansion</div><div class="itl-hint">From 12 Oct · {pipe_opps} opps</div></div>
    <div class="itl-tile"><div class="itl-val">{_euro(pipe_won)}</div><div class="itl-label">Closed won</div><div class="itl-hint">{pipe_won_n} deals on that clock</div></div>
  </div>
  <div class="itl-cwrap">
    <table class="itl-tbl">
      <tr><th>Attribution</th><th>Type</th><th class="num">Opps</th><th class="num">Total</th><th class="num">Open</th><th class="num">Won</th></tr>
      {attr_html}
    </table>
  </div>
  <div class="itl-note">No Partner-typed opportunities in this list — net new is New Business. Partner Day is a campaign, not an opportunity type. Full lists are on the Funnel tab.</div>

  <div class="itl-ch">NB + Expansion by segment</div>
  <div class="itl-cwrap">
    <table class="itl-tbl">
      <tr><th>Type / segment</th><th class="num">Opps</th><th class="num">Total</th><th class="num">Open</th><th class="num">Won</th></tr>
      {mix_html}
    </table>
  </div>
</div>
"""
display(HTML("<style>" + ITL_CSS + "</style>" + body))
