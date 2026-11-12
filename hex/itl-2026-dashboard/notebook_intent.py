from IPython.display import display, HTML

ITL_CSS = """
.itl-dash { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color:#111827; max-width: 1100px; }
.itl-kicker { font-size:12px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:#FF6D5A; margin:0 0 6px 0; }
.itl-title { font-size:28px; font-weight:700; margin:0 0 6px 0; }
.itl-sub { font-size:14px; color:#6B7280; margin:0 0 22px 0; }
.itl-ch { font-size:13px; font-weight:700; letter-spacing:.06em; text-transform:uppercase; color:#6B7280; margin:28px 0 12px 0; padding-top:18px; border-top:1px solid #E5E7EB; }
.itl-ch:first-of-type { border-top:none; margin-top:8px; padding-top:0; }
.itl-strip { display:grid; grid-template-columns:repeat(4, minmax(140px, 1fr)); gap:12px; margin:0 0 16px 0; }
.itl-strip-3 { display:grid; grid-template-columns:repeat(3, minmax(140px, 1fr)); gap:12px; margin:0 0 16px 0; }
@media (max-width: 900px) { .itl-strip, .itl-strip-3 { grid-template-columns:repeat(2, minmax(140px, 1fr)); } }
.itl-tile { border:1px solid #E5E7EB; border-radius:10px; background:#fff; padding:16px 18px 14px; }
.itl-val { font-size:32px; font-weight:700; color:#111827; line-height:1.1; font-variant-numeric:tabular-nums; }
.itl-val.accent { color:#FF6D5A; }
.itl-label { margin-top:8px; font-size:13px; color:#6B7280; font-weight:600; }
.itl-hint { margin-top:4px; font-size:11px; color:#9CA3AF; }
.itl-cwrap { border:1px solid #E5E7EB; border-radius:10px; padding:16px 18px 12px; margin:0 0 16px 0; background:#fff; }
.itl-tbl { width:100%; border-collapse:collapse; font-size:13px; }
.itl-tbl th { text-align:left; color:#6B7280; font-weight:600; padding:6px 8px; border-bottom:1px solid #E5E7EB; }
.itl-tbl th.num { text-align:right; }
.itl-tbl td { padding:7px 8px; border-bottom:1px solid #F3F4F6; vertical-align:top; }
.itl-tbl td.num { text-align:right; font-variant-numeric:tabular-nums; font-weight:600; }
.itl-note { margin-top:8px; font-size:13px; color:#6B7280; padding:12px 14px; background:#F9FAFB; border:1px solid #E5E7EB; border-radius:8px; }
.itl-mean { font-size:14px; color:#374151; line-height:1.55; margin:0 0 10px 0; }
.itl-spark { display:flex; align-items:flex-end; gap:3px; height:56px; margin:10px 0 4px 0; }
.itl-spark i { display:block; flex:1; min-width:6px; border-radius:2px 2px 0 0; background:#D1D5DB; }
.itl-spark i.hit { background:#FF6D5A; }
.itl-legend { font-size:11px; color:#9CA3AF; }
.itl-cname { color:#374151; }
.itl-crow { display:grid; grid-template-columns:150px 1fr 90px; gap:10px; align-items:center; margin:7px 0; font-size:13px; }
.itl-cbar { background:#F3F4F6; border-radius:4px; height:10px; overflow:hidden; }
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
        h = 6 + 50 * val / mx
        cls = "hit" if str(week).startswith(hit_week) else ""
        bits.append(f'<i class="{cls}" title="{week}: {val:,}" style="height:{h:.0f}px"></i>')
    return '<div class="itl-spark">' + "".join(bits) + "</div>"


# Conference week (n8n.io only) vs week before.
users_base, users_conf, users_post = 173571, 174802, 186284
berlin_base, berlin_conf, berlin_post = 8601, 11428, 6995
cta_base, cta_conf, cta_post = 80954, 78744, 68808
trial_base, trial_conf, trial_post = 417, 414, 286
form_base, form_conf, form_post = 175, 180, 132
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
    cta_post = _itl_int(p.get("cta_clicks"), cta_post)
    trial_base = _itl_int(b.get("trial_starts"), trial_base)
    trial_conf = _itl_int(c.get("trial_starts"), trial_conf)
    trial_post = _itl_int(p.get("trial_starts"), trial_post)
    form_base = _itl_int(b.get("sales_form_completions"), form_base)
    form_conf = _itl_int(c.get("sales_form_completions"), form_conf)
    form_post = _itl_int(p.get("sales_form_completions"), form_post)
except Exception:
    pass

# Long view: public n8n sites, 1 Jun–9 Nov.
web_users, web_europe, web_germany = 3784923, 1028583, 218861
web_views, web_europe_views, web_germany_views = 20443506, 5470052, 1200589
try:
    row = ga4_web_geo_kpis.iloc[0]
    web_users = _itl_int(row.get("users"), web_users)
    web_europe = _itl_int(row.get("europe_users"), web_europe)
    web_germany = _itl_int(row.get("germany_users"), web_germany)
    web_views = _itl_int(row.get("page_views"), web_views)
    web_europe_views = _itl_int(row.get("europe_page_views"), web_europe_views)
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

# Weekly n8n.io users / Berlin. Live frame fills Jun–Nov; fallback is the three conference weeks.
weekly_users = [
    ("2026-10-05", 173571), ("2026-10-12", 174802), ("2026-10-19", 186284),
]
weekly_berlin = [
    ("2026-10-05", 8601), ("2026-10-12", 11428), ("2026-10-19", 6995),
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
  <p class="itl-sub">Website demand around the conference — not Fliplet visits, not app.n8n.cloud.</p>

  <div class="itl-ch">What these numbers mean</div>
  <div class="itl-cwrap">
    <p class="itl-mean"><b>User</b> = a distinct browser that loaded a page. <b>Event</b> = one tracked hit (page view, click). These people were on the website, not necessarily in the room.</p>
    <p class="itl-mean"><b>Two clocks, two site sets.</b> The week comparison is <b>n8n.io only</b>, Monday–Sunday. The Jun–Nov tiles are public n8n sites together: n8n.io, docs, community, blog, learn, plans.</p>
    <p class="itl-mean" style="margin-bottom:0">Berlin events use <code>geo_city = Berlin</code>. Germany / Europe on the long view use country and continent. None of this is door scans.</p>
  </div>

  <div class="itl-ch">Did the conference week spike?</div>
  <p class="itl-mean">Compare <b>12–18 Oct</b> with the week before, <b>5–11 Oct</b>, on n8n.io.</p>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val accent">{_pct(berlin_conf, berlin_base)}</div><div class="itl-label">Berlin events</div><div class="itl-hint">{berlin_base:,} → {berlin_conf:,} · this is the spike</div></div>
    <div class="itl-tile"><div class="itl-val">{_pct(users_conf, users_base)}</div><div class="itl-label">n8n.io users worldwide</div><div class="itl-hint">{users_base:,} → {users_conf:,} · no global spike</div></div>
    <div class="itl-tile"><div class="itl-val">{_pct(cta_conf, cta_base)}</div><div class="itl-label">CTA clicks</div><div class="itl-hint">{cta_base:,} → {cta_conf:,}</div></div>
    <div class="itl-tile"><div class="itl-val">{_pct(trial_conf, trial_base)}</div><div class="itl-label">Trial starts</div><div class="itl-hint">{trial_base:,} → {trial_conf:,}</div></div>
  </div>
  <div class="itl-cwrap">
    <table class="itl-tbl">
      <tr><th>n8n.io</th><th class="num">5–11 Oct</th><th class="num">12–18 Oct conference</th><th class="num">19–25 Oct after</th><th>Read as</th></tr>
      <tr><td>Users</td><td class="num">{users_base:,}</td><td class="num">{users_conf:,}</td><td class="num">{users_post:,}</td><td>Worldwide traffic stayed flat in the week, then ticked up after</td></tr>
      <tr><td>Berlin events</td><td class="num">{berlin_base:,}</td><td class="num">{berlin_conf:,}</td><td class="num">{berlin_post:,}</td><td>Local demand jumped, then fell back below the week before</td></tr>
      <tr><td>CTA clicks</td><td class="num">{cta_base:,}</td><td class="num">{cta_conf:,}</td><td class="num">{cta_post:,}</td><td>No conference lift on Get started</td></tr>
      <tr><td>Trial starts</td><td class="num">{trial_base:,}</td><td class="num">{trial_conf:,}</td><td class="num">{trial_post:,}</td><td>No conference lift on trials</td></tr>
      <tr><td>Sales forms</td><td class="num">{form_base:,}</td><td class="num">{form_conf:,}</td><td class="num">{form_post:,}</td><td>Forms stayed ~flat in the week</td></tr>
    </table>
  </div>
  <div class="itl-note">The story: Berlin spiked. The rest of n8n.io did not. After the event, Berlin dropped and worldwide users rose slightly ({users_post:,}).</div>

  <div class="itl-ch">Long-term · 1 Jun–9 Nov</div>
  <p class="itl-mean">Public n8n websites (n8n.io + docs + community + blog + learn + plans). A different, wider set than the week table above.</p>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val">{_itl_short(web_users)}</div><div class="itl-label">Website users</div><div class="itl-hint">{web_views:,} page views · Jun–Nov</div></div>
    <div class="itl-tile"><div class="itl-val accent">{_itl_short(web_europe)}</div><div class="itl-label">Europe</div><div class="itl-hint">{europe_share}% of website users</div></div>
    <div class="itl-tile"><div class="itl-val accent">{_itl_short(web_germany)}</div><div class="itl-label">Germany</div><div class="itl-hint">{germany_share}% of Europe · {_itl_short(web_germany_views)} page views</div></div>
    <div class="itl-tile"><div class="itl-val">{_itl_short(peak_users[1])}</div><div class="itl-label">Busiest n8n.io week</div><div class="itl-hint">{peak_users[0]} · not conference week</div></div>
  </div>
  <div class="itl-cwrap">
    <div class="itl-label" style="margin:0">n8n.io users by week</div>
    {users_spark}
    <div class="itl-legend">Coral bar = conference week 12–18 Oct. Peak was early August, not ITL. Last partial week omitted.</div>
    <div class="itl-label" style="margin:14px 0 0 0">Berlin events by week</div>
    {berlin_spark}
    <div class="itl-legend">Conference week is the tallest Berlin bar in this window.</div>
  </div>
  <div class="itl-cwrap">
    <div class="itl-label" style="margin:0 0 8px 0">Top Europe · Jun–Nov website users</div>
    {country_html}
  </div>
  <div class="itl-note">If a number looks huge next to 426 / 916, it is this website clock — months of browsers, not two days in Berlin.</div>
</div>
"""
display(HTML("<style>" + ITL_CSS + "</style>" + body))
