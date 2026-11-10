import plotly.graph_objects as go

# Physical headcount from Fliplet Purchases + Scans (snapshot 10 Nov 2026).
# Overlapping on purpose. Do not use Salesforce campaign leftovers here.
registered = 1269
partner = 391
eco = 878
either = 997
both = 272

try:
    total_pipeline = float(pipeline_arr["total_amount"].sum())
    opp_rows = int(len(pipeline_arr))
except Exception:
    total_pipeline = 0.0
    opp_rows = 0

kpis = [
    {"value": registered, "title": "Registered (Fliplet)", "sub": "Paid + Free tickets, unique email", "x": [0, 0.18]},
    {"value": partner, "title": "Partner Day", "sub": "13 Oct door scans, overlapping", "x": [0.21, 0.39]},
    {"value": eco, "title": "Ecosystem Day", "sub": "14 Oct door scans, overlapping", "x": [0.42, 0.60]},
    {"value": either, "title": "Either day", "sub": f"{both:,} came both days", "x": [0.63, 0.81]},
    {"value": total_pipeline, "title": "Pipeline (USD)", "sub": f"{opp_rows} opp rows · Salesforce Amount", "x": [0.84, 1.0]},
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
