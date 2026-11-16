# Day visit KPIs — last line must be the figure so Hex renders it.
import plotly.graph_objects as go

kpi = go.Figure()
specs = [
    (1269, "Registered", "All participants, incl. staff"),
    (426, "Partner Day visits", "391 door + 35 badge pickup"),
    (916, "Ecosystem Day visits", "878 door + 38 green YES"),
]
for i, (val, title, sub) in enumerate(specs):
    x0, x1 = i / 3 + 0.02, (i + 1) / 3 - 0.02
    kpi.add_trace(go.Indicator(
        mode="number",
        value=val,
        number={"font": {"size": 36, "color": "#FF6D5A"}, "valueformat": ",.0f"},
        title={"text": f"<b>{title}</b><br><span style='font-size:12px;color:#888'>{sub}</span>"},
        domain={"x": [x0, x1], "y": [0, 1]},
    ))
kpi.update_layout(
    title=dict(text="Per-day visits · door + badge + YES", font=dict(size=18)),
    height=200,
    paper_bgcolor="white",
    margin=dict(t=50, b=10, l=10, r=10),
    font=dict(family="Inter, Arial, sans-serif", color="#333"),
)
kpi
