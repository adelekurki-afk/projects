from IPython.display import display, HTML

def _itl_int(value, default):
    try:
        if value is None:
            return default
        return int(value)
    except Exception:
        return default


def _itl_short(n):
    n = int(n)
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 10_000:
        return f"{n / 1_000:.0f}k"
    return f"{n:,}"


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

web_users, web_europe, web_germany = 3784923, 1028583, 218861
web_views, web_europe_views, web_germany_views = 20443506, 5470052, 1200589
web_germany_week, web_europe_week = 11461, 55044
try:
    row = ga4_web_geo_kpis.iloc[0]
    web_users = _itl_int(row.get("users"), web_users)
    web_europe = _itl_int(row.get("europe_users"), web_europe)
    web_germany = _itl_int(row.get("germany_users"), web_germany)
    web_views = _itl_int(row.get("page_views"), web_views)
    web_europe_views = _itl_int(row.get("europe_page_views"), web_europe_views)
    web_germany_views = _itl_int(row.get("germany_page_views"), web_germany_views)
    web_germany_week = _itl_int(row.get("germany_users_conference_week"), web_germany_week)
    web_europe_week = _itl_int(row.get("europe_users_conference_week"), web_europe_week)
except Exception:
    pass
europe_share = int(round(100 * web_europe / web_users)) if web_users else 0
germany_share = int(round(100 * web_germany / web_europe)) if web_europe else 0

berlin_base, berlin_conf = 8601, 11428
users_base, users_conf = 173571, 174802
cta_conf, trial_conf, form_conf = 78744, 414, 180
try:
    g = ga4_signup_weekly
    b = g[g["week_label"].astype(str).str.contains("Baseline")].iloc[0]
    c = g[g["week_label"].astype(str).str.contains("Conference")].iloc[0]
    berlin_base = _itl_int(b.get("berlin_events"), berlin_base)
    berlin_conf = _itl_int(c.get("berlin_events"), berlin_conf)
    users_base = _itl_int(b.get("unique_users"), users_base)
    users_conf = _itl_int(c.get("unique_users"), users_conf)
    cta_conf = _itl_int(c.get("cta_clicks"), cta_conf)
    trial_conf = _itl_int(c.get("trial_starts"), trial_conf)
    form_conf = _itl_int(c.get("sales_form_completions"), form_conf)
except Exception:
    pass

countries = [
    ("Germany", 218861), ("France", 149377), ("United Kingdom", 106459),
    ("Spain", 85702), ("Netherlands", 66759),
]
try:
    countries = [
        (str(r["country"]), _itl_int(r["users"], 0))
        for _, r in ga4_web_europe_countries.iterrows()
        if str(r["country"]) != "Russia"
    ][:5]
except Exception:
    pass
max_users = max((u for _, u in countries), default=1)
country_rows = []
for name, users in countries:
    width = 100.0 * users / max_users
    color = "#FF6D5A" if name == "Germany" else "#4F7FB8"
    safe = name.replace("&", "&amp;").replace("<", "&lt;")
    country_rows.append(
        f'<div class="itl-crow"><div class="itl-cname">{safe}</div>'
        f'<div class="itl-cbar"><span style="width:{width:.1f}%;background:{color}"></span></div>'
        f'<div class="itl-cnum">{users:,}</div></div>'
    )
country_html = "\n".join(country_rows)

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

html = f"""
<style>
.itl-dash {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color:#111827; max-width: 1100px; }}
.itl-kicker {{ font-size:12px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:#FF6D5A; margin:0 0 6px 0; }}
.itl-title {{ font-size:28px; font-weight:700; margin:0 0 6px 0; }}
.itl-sub {{ font-size:14px; color:#6B7280; margin:0 0 22px 0; }}
.itl-ch {{ font-size:13px; font-weight:700; letter-spacing:.06em; text-transform:uppercase; color:#6B7280; margin:28px 0 12px 0; padding-top:18px; border-top:1px solid #E5E7EB; }}
.itl-ch:first-of-type {{ border-top:none; margin-top:8px; padding-top:0; }}
.itl-strip {{ display:grid; grid-template-columns:repeat(4, minmax(140px, 1fr)); gap:12px; margin:0 0 16px 0; }}
.itl-strip-3 {{ display:grid; grid-template-columns:repeat(3, minmax(140px, 1fr)); gap:12px; margin:0 0 16px 0; }}
@media (max-width: 900px) {{ .itl-strip, .itl-strip-3 {{ grid-template-columns:repeat(2, minmax(140px, 1fr)); }} }}
.itl-tile {{ border:1px solid #E5E7EB; border-radius:10px; background:#fff; padding:16px 18px 14px; }}
.itl-val {{ font-size:32px; font-weight:700; color:#111827; line-height:1.1; font-variant-numeric:tabular-nums; }}
.itl-val.accent {{ color:#FF6D5A; }}
.itl-label {{ margin-top:8px; font-size:13px; color:#6B7280; font-weight:600; }}
.itl-hint {{ margin-top:4px; font-size:11px; color:#9CA3AF; }}
.itl-days {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:0 0 16px 0; }}
@media (max-width: 700px) {{ .itl-days {{ grid-template-columns:1fr; }} }}
.itl-day {{ border:1px solid #E5E7EB; border-radius:10px; padding:18px 20px; background:#fff; }}
.itl-day h3 {{ margin:0 0 8px 0; font-size:13px; color:#6B7280; font-weight:600; text-transform:uppercase; letter-spacing:.04em; }}
.itl-day .big {{ font-size:44px; font-weight:700; color:#FF6D5A; line-height:1; font-variant-numeric:tabular-nums; }}
.itl-day .meta {{ margin-top:10px; font-size:13px; color:#6B7280; }}
.itl-cwrap {{ border:1px solid #E5E7EB; border-radius:10px; padding:16px 18px 12px; margin:0 0 16px 0; background:#fff; }}
.itl-crow {{ display:grid; grid-template-columns:160px 1fr 130px; gap:10px; align-items:center; margin:7px 0; font-size:13px; }}
.itl-tbl {{ width:100%; border-collapse:collapse; font-size:13px; }}
.itl-tbl th {{ text-align:left; color:#6B7280; font-weight:600; padding:6px 8px; border-bottom:1px solid #E5E7EB; }}
.itl-tbl th.num {{ text-align:right; }}
.itl-tbl td {{ padding:7px 8px; border-bottom:1px solid #F3F4F6; }}
.itl-tbl td.num {{ text-align:right; font-variant-numeric:tabular-nums; font-weight:600; }}
.itl-cname {{ color:#374151; }}
.itl-cbar {{ background:#F3F4F6; border-radius:4px; height:10px; overflow:hidden; }}
.itl-cbar span {{ display:block; height:100%; border-radius:4px; }}
.itl-cnum {{ text-align:right; font-variant-numeric:tabular-nums; font-weight:600; color:#111827; font-size:12px; }}
.itl-note {{ margin-top:8px; font-size:13px; color:#6B7280; padding:12px 14px; background:#F9FAFB; border:1px solid #E5E7EB; border-radius:8px; }}
</style>
<div class="itl-dash">
  <div class="itl-kicker">In the Loop 2026</div>
  <h1 class="itl-title">Overview</h1>
  <p class="itl-sub">Conference visits · Salesforce conversion · opportunities. Then participation, site intent, and Partner Day.</p>

  <div class="itl-ch">1 · Conference visits</div>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val">1,269</div><div class="itl-label">Registered</div><div class="itl-hint">Paid + Free unique email</div></div>
    <div class="itl-tile"><div class="itl-val accent">426</div><div class="itl-label">Partner Day</div><div class="itl-hint">13 Oct · 391 door + 35 badge</div></div>
    <div class="itl-tile"><div class="itl-val accent">916</div><div class="itl-label">Ecosystem Day</div><div class="itl-hint">14 Oct · 878 door + 38 green YES</div></div>
    <div class="itl-tile"><div class="itl-val">1,018</div><div class="itl-label">Unique people</div><div class="itl-hint">Either day · 324 came both days</div></div>
  </div>

  <div class="itl-ch">2 · Pipeline conversion</div>
  <p class="itl-sub" style="margin-bottom:10px">Salesforce Free/Paid. This registered count is not the Fliplet 1,269. Attended is not Partner Day 426 or Ecosystem Day 916.</p>
  <div class="itl-cwrap">{funnel_html}</div>

  <div class="itl-ch">3 · Opportunities</div>
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

  <div class="itl-ch">Participation</div>
  <div class="itl-days">
    <div class="itl-day"><h3>Partner Day · 13 Oct</h3><div class="big">426</div><div class="meta">102 Partner only · 324 also came on Eco Day · 18 staff door scans sit inside · 487 had a ticket</div></div>
    <div class="itl-day"><h3>Ecosystem Day · 14 Oct</h3><div class="big">916</div><div class="meta">592 Eco only · 324 also came on Partner Day · 19 staff door scans sit inside · 1,205 had a ticket</div></div>
  </div>
  <div class="itl-strip-3">
    <div class="itl-tile"><div class="itl-val">113</div><div class="itl-label">Staff tickets</div><div class="itl-hint">Overlay inside 426 / 916</div></div>
    <div class="itl-tile"><div class="itl-val">116</div><div class="itl-label">Programme speakers</div><div class="itl-hint">Overlay · Speakers tab</div></div>
    <div class="itl-tile"><div class="itl-val">39</div><div class="itl-label">CAB overlay</div><div class="itl-hint">11 members · 28 guests</div></div>
  </div>

  <div class="itl-ch">Site intent</div>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val">{_itl_short(web_users)}</div><div class="itl-label">Website users</div><div class="itl-hint">Jun–Nov · n8n.io, docs, community, blog, learn, plans</div></div>
    <div class="itl-tile"><div class="itl-val accent">{_itl_short(web_europe)}</div><div class="itl-label">Europe</div><div class="itl-hint">{europe_share}% of website users</div></div>
    <div class="itl-tile"><div class="itl-val accent">{_itl_short(web_germany)}</div><div class="itl-label">Germany</div><div class="itl-hint">{germany_share}% of Europe · {_itl_short(web_germany_views)} page views</div></div>
    <div class="itl-tile"><div class="itl-val">{berlin_conf:,}</div><div class="itl-label">Berlin events · conference week</div><div class="itl-hint">Up from {berlin_base:,} the week before</div></div>
  </div>
  <div class="itl-strip-3">
    <div class="itl-tile"><div class="itl-val">{cta_conf:,}</div><div class="itl-label">CTA clicks</div><div class="itl-hint">n8n.io · 12–18 Oct</div></div>
    <div class="itl-tile"><div class="itl-val">{trial_conf:,}</div><div class="itl-label">Trial starts</div><div class="itl-hint">Conference week</div></div>
    <div class="itl-tile"><div class="itl-val">{form_conf:,}</div><div class="itl-label">Sales forms</div><div class="itl-hint">Conference week</div></div>
  </div>
  <div class="itl-cwrap">
    <div class="itl-label" style="margin:0 0 8px 0">Top Europe · website users</div>
    {country_html}
  </div>

  <div class="itl-ch">Partner Day</div>
  <div class="itl-days">
    <div class="itl-day"><h3>How 426 is built</h3><div class="big">426</div><div class="meta">391 unique door scans on 13 Oct, plus 35 people who collected a badge on 12 Oct and did not scan on Partner Day. Monday staff-only badge pickup (35) is not added. Salesforce Partner Day Attended is a different list.</div></div>
    <div class="itl-day"><h3>Vs Ecosystem Day</h3><div class="big">916</div><div class="meta">878 door on 14 Oct + 38 green YES (40 YES, 2 already in the door count). Partner Day is the smaller, partner-only room. Ecosystem Day is the public day.</div></div>
  </div>
  <div class="itl-note">Visits are Fliplet (door + badge + green YES). Conversion and opportunities are Salesforce. Website tiles are GA4 page-view users — not app.n8n.cloud.</div>
</div>
"""
display(HTML(html))
