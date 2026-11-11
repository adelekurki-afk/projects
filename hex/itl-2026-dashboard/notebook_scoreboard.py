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

html = f"""
<style>
.itl-dash {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color:#111827; max-width: 1100px; }}
.itl-kicker {{ font-size:12px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:#FF6D5A; margin:0 0 6px 0; }}
.itl-title {{ font-size:28px; font-weight:700; margin:0 0 6px 0; }}
.itl-sub {{ font-size:14px; color:#6B7280; margin:0 0 20px 0; }}
.itl-strip {{ display:grid; grid-template-columns:repeat(4, minmax(140px, 1fr)); gap:12px; margin:0 0 20px 0; }}
@media (max-width: 900px) {{ .itl-strip {{ grid-template-columns:repeat(2, minmax(140px, 1fr)); }} }}
.itl-tile {{ border:1px solid #E5E7EB; border-radius:10px; background:#fff; padding:16px 18px 14px; }}
.itl-val {{ font-size:32px; font-weight:700; color:#111827; line-height:1.1; font-variant-numeric:tabular-nums; }}
.itl-val.accent {{ color:#FF6D5A; }}
.itl-label {{ margin-top:8px; font-size:13px; color:#6B7280; font-weight:600; }}
.itl-hint {{ margin-top:4px; font-size:11px; color:#9CA3AF; }}
.itl-days {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:0 0 20px 0; }}
@media (max-width: 700px) {{ .itl-days {{ grid-template-columns:1fr; }} }}
.itl-day {{ border:1px solid #E5E7EB; border-radius:10px; padding:18px 20px; background:#fff; }}
.itl-day h3 {{ margin:0 0 8px 0; font-size:14px; color:#6B7280; font-weight:600; text-transform:uppercase; letter-spacing:.04em; }}
.itl-day .big {{ font-size:44px; font-weight:700; color:#FF6D5A; line-height:1; font-variant-numeric:tabular-nums; }}
.itl-day .meta {{ margin-top:10px; font-size:13px; color:#6B7280; }}
.itl-row {{ display:grid; grid-template-columns:repeat(3, 1fr); gap:12px; }}
@media (max-width: 800px) {{ .itl-row {{ grid-template-columns:1fr; }} }}
.itl-note {{ margin-top:18px; font-size:13px; color:#6B7280; padding:12px 14px; background:#F9FAFB; border:1px solid #E5E7EB; border-radius:8px; }}
.itl-webhead {{ font-size:12px; font-weight:600; letter-spacing:.06em; text-transform:uppercase; color:#6B7280; margin:4px 0 10px 0; }}
</style>
<div class="itl-dash">
  <div class="itl-kicker">In the Loop 2026</div>
  <h1 class="itl-title">Conference visits</h1>
  <p class="itl-sub">Everyone who participated · door scans + badge pickup + green YES on the attendance sheet · staff, speakers, and CAB sit inside · people who came both days are counted on both days</p>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val">1,269</div><div class="itl-label">Registered</div><div class="itl-hint">All participants · Paid + Free unique email</div></div>
    <div class="itl-tile"><div class="itl-val accent">426</div><div class="itl-label">Partner Day visits</div><div class="itl-hint">391 door + 35 badge pickup</div></div>
    <div class="itl-tile"><div class="itl-val accent">916</div><div class="itl-label">Ecosystem Day visits</div><div class="itl-hint">878 door + 38 green YES</div></div>
    <div class="itl-tile"><div class="itl-val">39</div><div class="itl-label">CAB overlay</div><div class="itl-hint">Already inside the day tiles when scanned or YES</div></div>
  </div>
  <div class="itl-webhead">n8n websites · Germany &amp; Europe · 1 Jun–9 Nov</div>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val">{_itl_short(web_users)}</div><div class="itl-label">Website users</div><div class="itl-hint">{web_users:,} · {_itl_short(web_views)} page views</div></div>
    <div class="itl-tile"><div class="itl-val accent">{_itl_short(web_europe)}</div><div class="itl-label">Europe users</div><div class="itl-hint">{europe_share}% of website users · {_itl_short(web_europe_views)} page views</div></div>
    <div class="itl-tile"><div class="itl-val accent">{_itl_short(web_germany)}</div><div class="itl-label">Germany users</div><div class="itl-hint">{germany_share}% of Europe · {_itl_short(web_germany_views)} page views</div></div>
    <div class="itl-tile"><div class="itl-val">{web_germany_week:,}</div><div class="itl-label">Germany · conference week</div><div class="itl-hint">12–18 Oct · {web_europe_week:,} Europe users that week</div></div>
  </div>
  <div class="itl-days">
    <div class="itl-day"><h3>Partner Day · 13 Oct</h3><div class="big">426</div><div class="meta">391 unique door scans on 13 Oct, plus 35 people who collected a badge on 12 Oct and did not scan on Partner Day. 18 staff door scans sit inside. 487 had a ticket.</div></div>
    <div class="itl-day"><h3>Ecosystem Day · 14 Oct</h3><div class="big">916</div><div class="meta">878 unique door scans on 14 Oct, plus 38 people marked YES on the green Incorrect no-show? column (40 YES, 2 already in the door count). 19 staff door scans sit inside. 1,205 had a ticket.</div></div>
  </div>
  <div class="itl-row">
    <div class="itl-tile"><div class="itl-val">113</div><div class="itl-label">Staff tickets</div><div class="itl-hint">Overlay · 18 / 19 door scans inside 426 / 916</div></div>
    <div class="itl-tile"><div class="itl-val">116</div><div class="itl-label">Programme speakers</div><div class="itl-hint">Overlay · 86 Partner / 79 Eco on Speakers tab</div></div>
    <div class="itl-tile"><div class="itl-val">39</div><div class="itl-label">CAB</div><div class="itl-hint">Overlay · 11 members · 28 guests</div></div>
  </div>
  <div class="itl-note">426 and 916 are everyone who participated, not attendees-minus-staff and not door scans alone. Monday staff-only badge pickup (35 people) is not added to Partner Day. 324 people are in both day tiles. Website tiles are GA4 page-view users on n8n.io, docs, community, blog, learn, and plans — not app.n8n.cloud.</div>
</div>
"""
display(HTML(html))
