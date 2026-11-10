from IPython.display import display, HTML

html = """
<style>
.itl-dash { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color:#111827; max-width: 1100px; }
.itl-kicker { font-size:12px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:#FF6D5A; margin:0 0 6px 0; }
.itl-title { font-size:28px; font-weight:700; margin:0 0 6px 0; }
.itl-sub { font-size:14px; color:#6B7280; margin:0 0 20px 0; }
.itl-strip { display:grid; grid-template-columns:repeat(4, minmax(140px, 1fr)); gap:12px; margin:0 0 20px 0; }
@media (max-width: 900px) { .itl-strip { grid-template-columns:repeat(2, minmax(140px, 1fr)); } }
.itl-tile { border:1px solid #E5E7EB; border-radius:10px; background:#fff; padding:16px 18px 14px; }
.itl-val { font-size:32px; font-weight:700; color:#111827; line-height:1.1; font-variant-numeric:tabular-nums; }
.itl-val.accent { color:#FF6D5A; }
.itl-label { margin-top:8px; font-size:13px; color:#6B7280; font-weight:600; }
.itl-hint { margin-top:4px; font-size:11px; color:#9CA3AF; }
.itl-days { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:0 0 20px 0; }
@media (max-width: 700px) { .itl-days { grid-template-columns:1fr; } }
.itl-day { border:1px solid #E5E7EB; border-radius:10px; padding:18px 20px; background:#fff; }
.itl-day h3 { margin:0 0 8px 0; font-size:14px; color:#6B7280; font-weight:600; text-transform:uppercase; letter-spacing:.04em; }
.itl-day .big { font-size:44px; font-weight:700; color:#FF6D5A; line-height:1; font-variant-numeric:tabular-nums; }
.itl-day .meta { margin-top:10px; font-size:13px; color:#6B7280; }
.itl-row { display:grid; grid-template-columns:repeat(3, 1fr); gap:12px; }
@media (max-width: 800px) { .itl-row { grid-template-columns:1fr; } }
.itl-note { margin-top:18px; font-size:13px; color:#6B7280; padding:12px 14px; background:#F9FAFB; border:1px solid #E5E7EB; border-radius:8px; }
</style>
<div class="itl-dash">
  <div class="itl-kicker">In the Loop 2026</div>
  <h1 class="itl-title">Conference visits</h1>
  <p class="itl-sub">Fliplet door scans · people who came both days are counted on both days</p>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val">1,269</div><div class="itl-label">Registered</div><div class="itl-hint">Paid + Free, unique email</div></div>
    <div class="itl-tile"><div class="itl-val accent">391</div><div class="itl-label">Partner Day visits</div><div class="itl-hint">13 Oct door scans</div></div>
    <div class="itl-tile"><div class="itl-val accent">878</div><div class="itl-label">Ecosystem Day visits</div><div class="itl-hint">14 Oct door scans</div></div>
    <div class="itl-tile"><div class="itl-val">39</div><div class="itl-label">CAB overlay</div><div class="itl-hint">All 39 redeemed</div></div>
  </div>
  <div class="itl-days">
    <div class="itl-day"><h3>Partner Day · 13 Oct</h3><div class="big">391</div><div class="meta">487 had a ticket for this day</div></div>
    <div class="itl-day"><h3>Ecosystem Day · 14 Oct</h3><div class="big">878</div><div class="meta">1,205 had a ticket for this day</div></div>
  </div>
  <div class="itl-row">
    <div class="itl-tile"><div class="itl-val">113</div><div class="itl-label">Staff tickets</div><div class="itl-hint">Fliplet Ticket family = Staff</div></div>
    <div class="itl-tile"><div class="itl-val">116</div><div class="itl-label">Programme speakers</div><div class="itl-hint">62 Partner Day · 79 Eco Day</div></div>
    <div class="itl-tile"><div class="itl-val">39</div><div class="itl-label">CAB</div><div class="itl-hint">11 members · 28 guests</div></div>
  </div>
  <div class="itl-note">272 people visited both days, so they appear in Partner Day and Ecosystem Day. There is no either-day unique.</div>
</div>
"""
display(HTML(html))
