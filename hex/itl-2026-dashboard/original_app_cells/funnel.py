import plotly.graph_objects as go

stages = lead_funnel['stage'].tolist()
counts = [int(c) for c in lead_funnel['count'].tolist()]
pcts = [float(p) for p in lead_funnel['pct_of_registered'].tolist()]

custom_labels = [
    f"{s}<br><b>{c:,}</b> ({p}%)"
    for s, c, p in zip(stages, counts, pcts)
]

fig = go.Figure(go.Funnel(
    y=stages,
    x=counts,
    text=[f"{c:,} ({p}%)" for c, p in zip(counts, pcts)],
    textinfo="text",
    textfont={"size": 14},
    marker=dict(
        color=["#FF6D5A", "#FF8F80", "#FFB3A7", "#FFC8BF", "#2D2D2D"],
        line=dict(width=1, color="white")
    ),
    connector=dict(line=dict(color="#E0E0E0", dash="dot", width=2))
))

fig.update_layout(
    title=dict(text="Registrant-to-Revenue Funnel", font=dict(size=18)),
    height=420,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin={"t": 60, "b": 20, "l": 220, "r": 60},
    font={"family": "Inter, Arial, sans-serif", "color": "#333"},
    yaxis=dict(tickfont=dict(size=13))
)

fig
