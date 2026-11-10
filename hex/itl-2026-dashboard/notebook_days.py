# APP: Fliplet overlapping days
# Snapshot 10 Nov 2026. Per-day visits only (no either-day unique).
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display, Markdown

display(Markdown("**NOV 10 NOTEBOOK v8 is live** — per-day visits from Fliplet door scans. People who came both days are in both tiles."))

days = pd.DataFrame([
    {"day": "Partner Day", "date": "13 Oct", "came": 391, "registered": 487},
    {"day": "Ecosystem Day", "date": "14 Oct", "came": 878, "registered": 1205},
])

try:
    total_pipeline = float(pipeline_arr["total_amount"].sum())
except Exception:
    total_pipeline = 0.0

kpi = go.Figure()
specs = [
    (1269, "Registered (Fliplet)", "Paid + Free tickets, unique email"),
    (391, "Partner Day visits", "13 Oct door scans"),
    (878, "Ecosystem Day visits", "14 Oct door scans"),
    (total_pipeline, "Pipeline (USD)", "Salesforce Amount since 12 Oct"),
]
for i, (val, title, sub) in enumerate(specs):
    x0, x1 = i / 4 + 0.01, (i + 1) / 4 - 0.01
    kpi.add_trace(go.Indicator(
        mode="number",
        value=val,
        number={"font": {"size": 32, "color": "#FF6D5A"}, "valueformat": ",.0f"},
        title={"text": f"<b>{title}</b><br><span style='font-size:11px;color:#888'>{sub}</span>"},
        domain={"x": [x0, x1], "y": [0, 1]},
    ))
kpi.update_layout(
    title=dict(text="Per-day visits (overlapping)", font=dict(size=18)),
    height=200, paper_bgcolor="white", margin=dict(t=50, b=10, l=10, r=10),
    font=dict(family="Inter, Arial, sans-serif", color="#333"),
)
display(kpi)

bar = go.Figure()
bar.add_trace(go.Bar(
    name="Came (door scans)", x=days["day"], y=days["came"],
    marker_color="#FF6D5A", text=days["came"], textposition="outside",
))
bar.add_trace(go.Bar(
    name="Had a ticket for this day", x=days["day"], y=days["registered"],
    marker_color="#4F7FB8", text=days["registered"], textposition="outside",
))
bar.update_layout(
    barmode="group",
    title=dict(text="Partner Day vs Ecosystem Day", font=dict(size=16)),
    height=380, paper_bgcolor="white", plot_bgcolor="white",
    margin=dict(t=60, b=40, l=40, r=20),
    font=dict(family="Inter, Arial, sans-serif", color="#333"),
    legend=dict(orientation="h", y=1.12, x=1, xanchor="right"),
    yaxis=dict(title="People"),
)
display(bar)

cab = pd.DataFrame([
    {"group": "CAB total", "on_list": 39, "partner_day": 29, "eco_day": 39, "redeemed": 39},
    {"group": "CAB Member", "on_list": 11, "partner_day": 1, "eco_day": 11, "redeemed": 11},
    {"group": "CAB Guest", "on_list": 28, "partner_day": 28, "eco_day": 28, "redeemed": 28},
])
cab_fig = go.Figure()
for i, row in cab.iterrows():
    x0, x1 = i / 3 + 0.03, (i + 1) / 3 - 0.03
    cab_fig.add_trace(go.Indicator(
        mode="number", value=int(row["on_list"]),
        number={"font": {"size": 34, "color": "#4F7FB8"}},
        title={"text": (
            f"<b>{row['group']}</b><br>"
            f"<span style='font-size:11px;color:#888'>Partner Day {int(row['partner_day'])} / Eco Day {int(row['eco_day'])} · {int(row['redeemed'])} redeemed</span>"
        )},
        domain={"x": [x0, x1], "y": [0, 1]},
    ))
cab_fig.update_layout(
    title=dict(text="CAB overlay (all 39 redeemed)", font=dict(size=16)),
    height=200, paper_bgcolor="white", margin=dict(t=50, b=10, l=10, r=10),
    font=dict(family="Inter, Arial, sans-serif", color="#333"),
)
display(cab_fig)
display(Markdown("272 people visited both days, so they are counted in Partner Day and in Ecosystem Day. n8n ops door scans were Partner 388 / Eco 874. Raw Scans tab is Partner 391 / Eco 878 (Berlin day)."))
display(days)
display(cab)
