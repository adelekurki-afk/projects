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
.itl-days { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:0 0 16px 0; }
@media (max-width: 700px) { .itl-days { grid-template-columns:1fr; } }
.itl-day { border:1px solid #E5E7EB; border-radius:10px; padding:18px 20px; background:#fff; }
.itl-day h3 { margin:0 0 8px 0; font-size:13px; color:#6B7280; font-weight:600; text-transform:uppercase; letter-spacing:.04em; }
.itl-day .big { font-size:44px; font-weight:700; color:#FF6D5A; line-height:1; font-variant-numeric:tabular-nums; }
.itl-day .meta { margin-top:10px; font-size:13px; color:#6B7280; }
.itl-tbl { width:100%; border-collapse:collapse; font-size:13px; }
.itl-tbl th { text-align:left; color:#6B7280; font-weight:600; padding:6px 8px; border-bottom:1px solid #E5E7EB; }
.itl-tbl th.num { text-align:right; }
.itl-tbl td { padding:7px 8px; border-bottom:1px solid #F3F4F6; }
.itl-tbl td.num { text-align:right; font-variant-numeric:tabular-nums; font-weight:600; }
.itl-cwrap { border:1px solid #E5E7EB; border-radius:10px; padding:16px 18px 12px; margin:0 0 16px 0; background:#fff; }
.itl-note { margin-top:8px; font-size:13px; color:#6B7280; padding:12px 14px; background:#F9FAFB; border:1px solid #E5E7EB; border-radius:8px; }
.itl-mean { font-size:14px; color:#374151; line-height:1.55; margin:0 0 10px 0; }
"""

body = """
<div class="itl-dash">
  <div class="itl-kicker">In the Loop 2026</div>
  <h1 class="itl-title">Participation</h1>
  <p class="itl-sub">Who was in the room. Fliplet door scans, plus Monday badge pickup, plus green YES. Staff, speakers, and CAB sit inside these numbers — they are not extra headcount.</p>

  <div class="itl-ch">Who came</div>
  <div class="itl-days">
    <div class="itl-day"><h3>Partner Day · 13 Oct</h3><div class="big">426</div><div class="meta">102 Partner only · 324 also came on Ecosystem Day · 18 staff door scans sit inside · 487 had a ticket</div></div>
    <div class="itl-day"><h3>Ecosystem Day · 14 Oct</h3><div class="big">916</div><div class="meta">592 Eco only · 324 also came on Partner Day · 19 staff door scans sit inside · 1,205 had a ticket</div></div>
  </div>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val">324</div><div class="itl-label">Both days</div><div class="itl-hint">Counted in both 426 and 916</div></div>
    <div class="itl-tile"><div class="itl-val accent">1,018</div><div class="itl-label">Unique people</div><div class="itl-hint">426 + 916 − 324</div></div>
    <div class="itl-tile"><div class="itl-val">102</div><div class="itl-label">Partner only</div><div class="itl-hint">Came Monday, not Tuesday</div></div>
    <div class="itl-tile"><div class="itl-val">592</div><div class="itl-label">Ecosystem only</div><div class="itl-hint">Came Tuesday, not Monday</div></div>
  </div>

  <div class="itl-ch">Overlays · not extra people</div>
  <div class="itl-strip-3">
    <div class="itl-tile"><div class="itl-val">113</div><div class="itl-label">Staff tickets</div><div class="itl-hint">Inside 426 / 916 when scanned</div></div>
    <div class="itl-tile"><div class="itl-val">116</div><div class="itl-label">Programme speakers</div><div class="itl-hint">Speakers tab overlay</div></div>
    <div class="itl-tile"><div class="itl-val">39</div><div class="itl-label">CAB overlay</div><div class="itl-hint">11 members · 28 guests · all redeemed</div></div>
  </div>

  <div class="itl-ch">How the day counts are built</div>
  <div class="itl-cwrap">
    <table class="itl-tbl">
      <tr><th></th><th class="num">Partner Day</th><th class="num">Ecosystem Day</th></tr>
      <tr><td>Door scans</td><td class="num">391</td><td class="num">878</td></tr>
      <tr><td>Added</td><td class="num">35 badge on 12 Oct</td><td class="num">38 green YES</td></tr>
      <tr><td><b>Visits</b></td><td class="num"><b>426</b></td><td class="num"><b>916</b></td></tr>
      <tr><td>Tickets issued</td><td class="num">487</td><td class="num">1,205</td></tr>
    </table>
  </div>
  <p class="itl-mean">Partner Day 426 = 391 unique door scans on 13 Oct + 35 people who collected a badge on 12 Oct and did not scan on Partner Day. Monday staff-only badge pickup (35) is not added.</p>
  <p class="itl-mean">Ecosystem Day 916 = 878 door scans on 14 Oct + 38 of 40 green YES (2 were already in the door count).</p>
  <div class="itl-note">Salesforce Attended (835) is a different list from these Fliplet visits. Do not compare them.</div>
</div>
"""
display(HTML("<style>" + ITL_CSS + "</style>" + body))
