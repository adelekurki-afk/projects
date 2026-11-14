import plotly.graph_objects as go

registered = 1269
partner = 426
eco = 916

fig = go.Figure()
kpis = [
    {"value": registered, "title": "Registered", "sub": "All participants, incl. staff", "x": [0, 0.32]},
    {"value": partner, "title": "Partner Day visits", "sub": "391 door + 35 badge pickup", "x": [0.34, 0.66]},
    {"value": eco, "title": "Ecosystem Day visits", "sub": "878 door + 38 green YES", "x": [0.68, 1.0]},
]
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
