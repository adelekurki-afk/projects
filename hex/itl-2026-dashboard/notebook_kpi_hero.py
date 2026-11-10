import plotly.graph_objects as go

# Per-day visits from Fliplet Purchases + Scans (snapshot 10 Nov 2026).
registered = 1269
partner = 391
eco = 878

try:
    total_pipeline = float(pipeline_arr["total_amount"].sum())
    opp_rows = int(len(pipeline_arr))
except Exception:
    total_pipeline = 0.0
    opp_rows = 0

kpis = [
    {"value": registered, "title": "Registered (Fliplet)", "sub": "Paid + Free tickets, unique email", "x": [0, 0.24]},
    {"value": partner, "title": "Partner Day visits", "sub": "13 Oct door scans", "x": [0.26, 0.49]},
    {"value": eco, "title": "Ecosystem Day visits", "sub": "14 Oct door scans", "x": [0.51, 0.74]},
    {"value": total_pipeline, "title": "Pipeline (USD)", "sub": f"{opp_rows} opp rows · Salesforce Amount", "x": [0.76, 1.0]},
]

fig = go.Figure()
for k in kpis:
    fig.add_trace(go.Indicator(
        mode="number",
        value=k["value"],
        number={"valueformat": ",", "font": {"size": 36, "color": "#FF6D5A"}},
        title={"text": f"<b>{k['title']}</b><br><span style='font-size:11px;color:#888'>{k['sub']}</span>"},
        domain={"x": k["x"], "y": [0, 1]},
    ))

fig.update_layout(
    height=180,
    paper_bgcolor="white",
    margin={"t": 20, "b": 10, "l": 10, "r": 10},
    font={"family": "Inter, Arial, sans-serif", "color": "#333"},
)

fig
