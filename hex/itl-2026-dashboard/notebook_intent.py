from IPython.display import display, HTML

ITL_CSS = """
.itl-dash { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color:#111827; max-width: 1100px; }
.itl-kicker { font-size:11px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:#FF6D5A; margin:0 0 4px 0; }
.itl-title { font-size:26px; font-weight:700; margin:0 0 6px 0; }
.itl-sub { font-size:13px; color:#6B7280; margin:0 0 18px 0; }
.itl-ch { font-size:12px; font-weight:700; letter-spacing:.06em; text-transform:uppercase; color:#9CA3AF; margin:22px 0 10px 0; }
.itl-strip { display:grid; grid-template-columns:repeat(4, minmax(140px, 1fr)); gap:12px; margin:0 0 8px 0; }
.itl-tile { border:1px solid #E5E7EB; border-radius:10px; background:#fff; padding:14px 16px 12px; }
.itl-val { font-size:32px; font-weight:700; line-height:1.1; font-variant-numeric:tabular-nums; }
.itl-val.accent { color:#FF6D5A; }
.itl-label { margin-top:6px; font-size:12px; color:#6B7280; font-weight:600; }
.itl-hint { margin-top:2px; font-size:11px; color:#9CA3AF; }
.itl-cwrap { border:1px solid #E5E7EB; border-radius:10px; padding:14px 16px 12px; margin:12px 0 0 0; background:#fff; }
.itl-spark { display:flex; align-items:flex-end; gap:3px; height:64px; margin:8px 0 4px 0; }
.itl-spark i { display:block; flex:1; min-width:6px; border-radius:2px 2px 0 0; background:#D1D5DB; }
.itl-spark i.hit { background:#FF6D5A; }
.itl-legend { font-size:11px; color:#9CA3AF; }
.itl-cname { color:#374151; font-size:13px; }
.itl-crow { display:grid; grid-template-columns:140px 1fr 80px; gap:10px; align-items:center; margin:7px 0; }
.itl-cbar { background:#F3F4F6; border-radius:4px; height:12px; overflow:hidden; }
.itl-cbar span { display:block; height:100%; border-radius:4px; }
.itl-cnum { text-align:right; font-variant-numeric:tabular-nums; font-weight:600; color:#111827; font-size:12px; }
"""


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


def _pct(new, old):
    if not old:
        return "—"
    p = 100.0 * (new - old) / old
    sign = "+" if p >= 0 else ""
    return f"{sign}{p:.0f}%"


def _spark(pairs, hit_week="2026-10-12"):
    mx = max((v for _, v in pairs), default=1) or 1
    bits = []
    for week, val in pairs:
        h = 6 + 58 * val / mx
        cls = "hit" if str(week).startswith(hit_week) else ""
        bits.append(f'<i class="{cls}" title="{week}: {val:,}" style="height:{h:.0f}px"></i>')
    return '<div class="itl-spark">' + "".join(bits) + "</div>"


users_base, users_conf, users_post = 173571, 174802, 186284
berlin_base, berlin_conf, berlin_post = 8601, 11428, 6995
cta_base, cta_conf = 80954, 78744
trial_base, trial_conf = 417, 414
try:
    g = ga4_signup_weekly
    b = g[g["week_label"].astype(str).str.contains("Baseline")].iloc[0]
    c = g[g["week_label"].astype(str).str.contains("Conference")].iloc[0]
    p = g[g["week_label"].astype(str).str.contains("Post")].iloc[0]
    users_base = _itl_int(b.get("unique_users"), users_base)
    users_conf = _itl_int(c.get("unique_users"), users_conf)
    users_post = _itl_int(p.get("unique_users"), users_post)
    berlin_base = _itl_int(b.get("berlin_events"), berlin_base)
    berlin_conf = _itl_int(c.get("berlin_events"), berlin_conf)
    berlin_post = _itl_int(p.get("berlin_events"), berlin_post)
    cta_base = _itl_int(b.get("cta_clicks"), cta_base)
    cta_conf = _itl_int(c.get("cta_clicks"), cta_conf)
    trial_base = _itl_int(b.get("trial_starts"), trial_base)
    trial_conf = _itl_int(c.get("trial_starts"), trial_conf)
except Exception:
    pass

web_users, web_europe, web_germany = 3784923, 1028583, 218861
web_views, web_germany_views = 20443506, 1200589
try:
    row = ga4_web_geo_kpis.iloc[0]
    web_users = _itl_int(row.get("users"), web_users)
    web_europe = _itl_int(row.get("europe_users"), web_europe)
    web_germany = _itl_int(row.get("germany_users"), web_germany)
    web_views = _itl_int(row.get("page_views"), web_views)
    web_germany_views = _itl_int(row.get("germany_page_views"), web_germany_views)
except Exception:
    pass
europe_share = int(round(100 * web_europe / web_users)) if web_users else 0
germany_share = int(round(100 * web_germany / web_europe)) if web_europe else 0

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

weekly_users = [
    ("2026-06-01", 212181), ("2026-06-08", 211254), ("2026-06-15", 197717),
    ("2026-06-22", 191155), ("2026-06-29", 185104), ("2026-07-06", 189926),
    ("2026-07-13", 188846), ("2026-07-20", 194738), ("2026-07-27", 236602),
    ("2026-08-03", 262172), ("2026-08-10", 249628), ("2026-08-17", 246108),
    ("2026-08-24", 248937), ("2026-08-31", 234251), ("2026-09-07", 183289),
    ("2026-09-14", 176849), ("2026-09-21", 171052), ("2026-09-28", 168643),
    ("2026-10-05", 173571), ("2026-10-12", 174802), ("2026-10-19", 186284),
    ("2026-10-26", 176581), ("2026-11-02", 163038),
]
weekly_berlin = [
    ("2026-06-01", 10532), ("2026-06-08", 10476), ("2026-06-15", 9034),
    ("2026-06-22", 8234), ("2026-06-29", 7967), ("2026-07-06", 9187),
    ("2026-07-13", 9216), ("2026-07-20", 9091), ("2026-07-27", 8443),
    ("2026-08-03", 9234), ("2026-08-10", 8924), ("2026-08-17", 9183),
    ("2026-08-24", 9062), ("2026-08-31", 9155), ("2026-09-07", 7772),
    ("2026-09-14", 9202), ("2026-09-21", 7746), ("2026-09-28", 9752),
    ("2026-10-05", 8601), ("2026-10-12", 11428), ("2026-10-19", 6995),
    ("2026-10-26", 5833), ("2026-11-02", 5928),
]
try:
    trend = ga4_post_event_trend
    wu, wb = [], []
    for _, r in trend.iterrows():
        week = str(r["week_start"])[:10]
        if week >= "2026-11-09":
            continue
        wu.append((week, _itl_int(r.get("n8n_users"), 0)))
        wb.append((week, _itl_int(r.get("berlin_events"), 0)))
    if wu:
        weekly_users, weekly_berlin = wu, wb
except Exception:
    pass

peak_users = max(weekly_users, key=lambda x: x[1])
users_spark = _spark(weekly_users)
berlin_spark = _spark(weekly_berlin)

body = f"""
<div class="itl-dash">
  <div class="itl-kicker">In the Loop 2026</div>
  <h1 class="itl-title">Intent</h1>
  <p class="itl-sub">n8n.io · 12–18 Oct vs 5–11 Oct. Long view is public sites, 1 Jun–9 Nov.</p>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val accent">{_pct(berlin_conf, berlin_base)}</div><div class="itl-label">Berlin events</div><div class="itl-hint">{berlin_base:,} → {berlin_conf:,}</div></div>
    <div class="itl-tile"><div class="itl-val">{_pct(users_conf, users_base)}</div><div class="itl-label">n8n.io users worldwide</div><div class="itl-hint">{users_base:,} → {users_conf:,} · no global spike</div></div>
    <div class="itl-tile"><div class="itl-val">{_pct(cta_conf, cta_base)}</div><div class="itl-label">CTA clicks</div><div class="itl-hint">{cta_base:,} → {cta_conf:,}</div></div>
    <div class="itl-tile"><div class="itl-val">{_pct(trial_conf, trial_base)}</div><div class="itl-label">Trial starts</div><div class="itl-hint">{trial_base:,} → {trial_conf:,}</div></div>
  </div>
  <div class="itl-cwrap">
    <div class="itl-label" style="margin:0">n8n.io users by week</div>
    {users_spark}
    <div class="itl-legend">Coral = conference week 12–18 Oct. Peak {peak_users[0]} ({_itl_short(peak_users[1])}), not ITL.</div>
    <div class="itl-label" style="margin:14px 0 0 0">Berlin events by week</div>
    {berlin_spark}
    <div class="itl-legend">Conference week is the tallest Berlin bar. After: {berlin_post:,}.</div>
  </div>
  <div class="itl-ch">Public sites · 1 Jun–9 Nov</div>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val">{_itl_short(web_users)}</div><div class="itl-label">Website users</div><div class="itl-hint">{web_views:,} page views</div></div>
    <div class="itl-tile"><div class="itl-val accent">{_itl_short(web_europe)}</div><div class="itl-label">Europe</div><div class="itl-hint">{europe_share}% of users</div></div>
    <div class="itl-tile"><div class="itl-val accent">{_itl_short(web_germany)}</div><div class="itl-label">Germany</div><div class="itl-hint">{germany_share}% of Europe · {_itl_short(web_germany_views)} views</div></div>
    <div class="itl-tile"><div class="itl-val">{_itl_short(peak_users[1])}</div><div class="itl-label">Busiest n8n.io week</div><div class="itl-hint">{peak_users[0]}</div></div>
  </div>
  <div class="itl-cwrap">
    <div class="itl-label" style="margin:0 0 8px 0">Top Europe</div>
    {country_html}
  </div>
</div>
"""
display(HTML("<style>" + ITL_CSS + "</style>" + body))
