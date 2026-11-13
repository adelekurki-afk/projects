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
funnel_max = max((c for _, c, _ in funnel), default=1)

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

body = f"""
<div class="itl-dash">
  <div class="itl-kicker">In the Loop 2026</div>
  <h1 class="itl-title">Overview</h1>
  <div class="itl-ch">Visits</div>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val">1,269</div><div class="itl-label">Registered</div><div class="itl-hint">Paid + Free unique email</div></div>
    <div class="itl-tile"><div class="itl-val accent">426</div><div class="itl-label">Partner Day</div><div class="itl-hint">13 Oct · door + badge</div></div>
    <div class="itl-tile"><div class="itl-val accent">916</div><div class="itl-label">Ecosystem Day</div><div class="itl-hint">14 Oct · door + green YES</div></div>
    <div class="itl-tile"><div class="itl-val">1,018</div><div class="itl-label">Unique people</div><div class="itl-hint">Either day · 324 came both</div></div>
  </div>

  <div class="itl-ch">Salesforce conversion</div>
  <div class="itl-cwrap">{funnel_html}</div>
  <div class="itl-ch">Opportunities</div>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val accent">{_euro(pipe_total)}</div><div class="itl-label">Total pipeline</div><div class="itl-hint">NB + Expansion from 12 Oct</div></div>
    <div class="itl-tile"><div class="itl-val">{_euro(pipe_open)}</div><div class="itl-label">Open</div><div class="itl-hint">{pipe_open_n} deals</div></div>
    <div class="itl-tile"><div class="itl-val">{_euro(pipe_won)}</div><div class="itl-label">Closed Won</div><div class="itl-hint">{pipe_won_n} deals</div></div>
    <div class="itl-tile"><div class="itl-val">{pipe_opps}</div><div class="itl-label">Opportunities</div><div class="itl-hint">{pipe_meetings} from meetings booked</div></div>
  </div>
  <div class="itl-cwrap">
    <table class="itl-tbl">
      <tr><th>Type / segment</th><th class="num">Opps</th><th class="num">Total</th><th class="num">Open</th><th class="num">Won</th></tr>
      {mix_html}
    </table>
  </div>
</div>
"""
display(HTML("<style>" + ITL_CSS + "</style>" + body))
