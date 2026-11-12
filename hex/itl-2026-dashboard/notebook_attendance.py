from IPython.display import display, HTML

ITL_CSS = """
.itl-dash { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color:#111827; max-width: 1100px; }
.itl-kicker { font-size:11px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:#FF6D5A; margin:0 0 4px 0; }
.itl-title { font-size:26px; font-weight:700; margin:0 0 16px 0; }
.itl-ch { font-size:12px; font-weight:700; letter-spacing:.06em; text-transform:uppercase; color:#9CA3AF; margin:22px 0 10px 0; }
.itl-days { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
@media (max-width: 700px) { .itl-days { grid-template-columns:1fr; } }
.itl-day { border:1px solid #E5E7EB; border-radius:12px; padding:18px 20px 16px; background:#fff; }
.itl-day h3 { margin:0 0 4px 0; font-size:12px; color:#6B7280; font-weight:600; text-transform:uppercase; letter-spacing:.04em; }
.itl-day .big { font-size:52px; font-weight:700; color:#FF6D5A; line-height:1; font-variant-numeric:tabular-nums; }
.itl-stack { display:flex; height:28px; border-radius:6px; overflow:hidden; margin-top:14px; }
.itl-stack span { display:block; }
.itl-overlap { display:flex; height:40px; border-radius:8px; overflow:hidden; color:#fff; font-size:12px; font-weight:700; }
.itl-overlap span { display:flex; align-items:center; justify-content:center; }
.itl-leg { display:flex; flex-wrap:wrap; gap:14px; font-size:12px; color:#6B7280; margin-top:8px; }
.itl-dot { display:inline-block; width:8px; height:8px; border-radius:2px; margin-right:6px; vertical-align:middle; }
.itl-strip { display:grid; grid-template-columns:repeat(4, minmax(120px, 1fr)); gap:12px; }
.itl-strip-3 { display:grid; grid-template-columns:repeat(3, minmax(120px, 1fr)); gap:12px; }
.itl-tile { border:1px solid #E5E7EB; border-radius:10px; background:#fff; padding:14px 16px; }
.itl-val { font-size:28px; font-weight:700; line-height:1.1; font-variant-numeric:tabular-nums; }
.itl-label { margin-top:6px; font-size:12px; color:#6B7280; font-weight:600; }
.itl-hint { margin-top:2px; font-size:11px; color:#9CA3AF; }
.itl-cwrap { border:1px solid #E5E7EB; border-radius:10px; padding:14px 16px 12px; margin:12px 0 0 0; background:#fff; }
.itl-crow { display:grid; grid-template-columns:150px 1fr 70px; gap:10px; align-items:center; margin:6px 0; font-size:13px; }
.itl-cname { color:#374151; }
.itl-cbar { background:#F3F4F6; border-radius:4px; height:10px; overflow:hidden; }
.itl-cbar span { display:block; height:100%; border-radius:4px; }
.itl-cnum { text-align:right; font-variant-numeric:tabular-nums; font-weight:600; font-size:12px; }
.itl-note { margin-top:12px; font-size:13px; color:#6B7280; padding:12px 14px; background:#F9FAFB; border:1px solid #E5E7EB; border-radius:8px; }
.itl-sub { font-size:13px; color:#6B7280; margin:0 0 10px 0; }
"""


def _bars(rows, color="#FF6D5A"):
    if not rows:
        return '<div class="itl-sub">Run the SQL cell, then Run all.</div>'
    mx = max((n for _, n in rows), default=1) or 1
    bits = []
    for name, n in rows:
        width = 100.0 * n / mx
        safe = str(name).replace("&", "&amp;")
        bits.append(
            f'<div class="itl-crow"><div class="itl-cname">{safe}</div>'
            f'<div class="itl-cbar"><span style="width:{width:.1f}%;background:{color}"></span></div>'
            f'<div class="itl-cnum">{n:,}</div></div>'
        )
    return "\n".join(bits)


def _group_day(df, day, col):
    try:
        part = df[df["day_name"] == day]
        grouped = part.groupby(col, dropna=False)["people"].sum().sort_values(ascending=False)
        return [(str(i), int(v)) for i, v in grouped.items()]
    except Exception:
        return []


region_p = region_e = segment_p = segment_e = seniority_p = seniority_e = []
try:
    region_p = _group_day(attendance_region_segment, "Partner Day", "region")
    region_e = _group_day(attendance_region_segment, "Ecosystem Day", "region")
    segment_p = _group_day(attendance_region_segment, "Partner Day", "segment")
    segment_e = _group_day(attendance_region_segment, "Ecosystem Day", "segment")
except Exception:
    pass
try:
    seniority_p = _group_day(attendance_seniority, "Partner Day", "seniority")
    seniority_e = _group_day(attendance_seniority, "Ecosystem Day", "seniority")
except Exception:
    pass

body = f"""
<div class="itl-dash">
  <div class="itl-kicker">In the Loop 2026</div>
  <h1 class="itl-title">Attendance</h1>
  <div class="itl-days">
    <div class="itl-day">
      <h3>Partner Day · 13 Oct</h3>
      <div class="big">426</div>
      <div class="itl-stack"><span style="width:91.8%;background:#FF6D5A"></span><span style="width:8.2%;background:#FDBA74"></span></div>
      <div class="itl-leg"><span><i class="itl-dot" style="background:#FF6D5A"></i>391 door</span><span><i class="itl-dot" style="background:#FDBA74"></i>35 badge</span></div>
    </div>
    <div class="itl-day">
      <h3>Ecosystem Day · 14 Oct</h3>
      <div class="big">916</div>
      <div class="itl-stack"><span style="width:95.9%;background:#FF6D5A"></span><span style="width:4.1%;background:#FDBA74"></span></div>
      <div class="itl-leg"><span><i class="itl-dot" style="background:#FF6D5A"></i>878 door</span><span><i class="itl-dot" style="background:#FDBA74"></i>38 green YES</span></div>
    </div>
  </div>
  <div class="itl-ch">1,018 unique people</div>
  <div class="itl-overlap">
    <span style="width:10.0%;background:#94A3B8">102</span>
    <span style="width:31.8%;background:#FF6D5A">324 both</span>
    <span style="width:58.2%;background:#4F7FB8">592</span>
  </div>
  <div class="itl-leg">
    <span><i class="itl-dot" style="background:#94A3B8"></i>Partner only 102</span>
    <span><i class="itl-dot" style="background:#FF6D5A"></i>Both days 324</span>
    <span><i class="itl-dot" style="background:#4F7FB8"></i>Ecosystem only 592</span>
  </div>
  <div class="itl-ch">Overlays · inside 426 / 916</div>
  <div class="itl-strip-3">
    <div class="itl-tile"><div class="itl-val">113</div><div class="itl-label">Staff tickets</div><div class="itl-hint">Not extra headcount</div></div>
    <div class="itl-tile"><div class="itl-val">116</div><div class="itl-label">Programme speakers</div><div class="itl-hint">Not extra headcount</div></div>
    <div class="itl-tile"><div class="itl-val">39</div><div class="itl-label">CAB</div><div class="itl-hint">11 members · 28 guests</div></div>
  </div>

  <div class="itl-ch">Region per day · Salesforce Attended</div>
  <p class="itl-sub">Account region on people marked Attended. This is not the Fliplet 426 / 916 clock.</p>
  <div class="itl-days">
    <div class="itl-cwrap"><div class="itl-label">Partner Day</div>{_bars(region_p)}</div>
    <div class="itl-cwrap"><div class="itl-label">Ecosystem Day</div>{_bars(region_e, "#4F7FB8")}</div>
  </div>

  <div class="itl-ch">Sales segment per day · Salesforce Attended</div>
  <div class="itl-days">
    <div class="itl-cwrap"><div class="itl-label">Partner Day</div>{_bars(segment_p)}</div>
    <div class="itl-cwrap"><div class="itl-label">Ecosystem Day</div>{_bars(segment_e, "#4F7FB8")}</div>
  </div>

  <div class="itl-ch">Seniority · title on Salesforce Attended</div>
  <div class="itl-days">
    <div class="itl-cwrap"><div class="itl-label">Partner Day</div>{_bars(seniority_p)}</div>
    <div class="itl-cwrap"><div class="itl-label">Ecosystem Day</div>{_bars(seniority_e, "#4F7FB8")}</div>
  </div>

  <div class="itl-ch">Attendance to sessions</div>
  <p class="itl-sub">Fliplet has no named session-scan column. Door scans match 391 / 878. Zone game scans and session feedback are the session proxies.</p>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val">1,633</div><div class="itl-label">Door scans</div><div class="itl-hint">1,039 unique · 18 scanners</div></div>
    <div class="itl-tile"><div class="itl-val">575</div><div class="itl-label">Zone game people</div><div class="itl-hint">2,516 scans · 7 locations</div></div>
    <div class="itl-tile"><div class="itl-val">66</div><div class="itl-label">Session ratings</div><div class="itl-hint">4.8 / 5 average</div></div>
    <div class="itl-tile"><div class="itl-val">484</div><div class="itl-label">Community Lounge</div><div class="itl-hint">Busiest game-scan zone</div></div>
  </div>
  <div class="itl-cwrap">
    <div class="itl-label">Game-scan zones</div>
    {_bars([("Community Lounge", 484), ("Cardputer Station", 425), ("Solution Zone n8n", 377), ("Candy Station", 350), ("Coffee Station", 335), ("Solution Zone Exhibitors", 293), ("Connection Zone", 252)])}
  </div>

  <div class="itl-ch">Attendance to meetings</div>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val accent">23</div><div class="itl-label">Sales meetings sheet</div><div class="itl-hint">14 new · 9 existing accounts</div></div>
    <div class="itl-tile"><div class="itl-val">1,076</div><div class="itl-label">Fliplet booked</div><div class="itl-hint">772 accepted · 236 pending · 70 rejected</div></div>
    <div class="itl-tile"><div class="itl-val">425</div><div class="itl-label">Meeting arrivals</div><div class="itl-hint">486 meetings seated</div></div>
    <div class="itl-tile"><div class="itl-val">20</div><div class="itl-label">Salesforce meeting booked</div><div class="itl-hint">Campaign member status</div></div>
  </div>
  <div class="itl-note">The sales meetings sheet is the n8n-staff list. Fliplet booked meetings are in-app 1:1s (mostly exhibitor / peer).</div>

  <div class="itl-ch">Feedback sheets</div>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val accent">8.6</div><div class="itl-label">Partner Day overall</div><div class="itl-hint">22 finished surveys · /10</div></div>
    <div class="itl-tile"><div class="itl-val">4.8</div><div class="itl-label">Session rating</div><div class="itl-hint">66 Fliplet ratings · /5</div></div>
    <div class="itl-tile"><div class="itl-val">6</div><div class="itl-label">Top session replies</div><div class="itl-hint">Networking · Ambassador programme</div></div>
    <div class="itl-tile"><div class="itl-val">—</div><div class="itl-label">Ecosystem Day survey</div><div class="itl-hint">No sheet found in Drive</div></div>
  </div>
</div>
"""
display(HTML("<style>" + ITL_CSS + "</style>" + body))
