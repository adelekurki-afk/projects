# APP: Chart · Lead to closed — one figure. Classic App only shows the first display().
import plotly.graph_objects as go
from IPython.display import display

PINK = "#FF91AC"
PINK_DEEP = "#87003C"
INK = "#9CA3AF"

stages = ["Lead", "Meeting booked", "Opportunity", "Pipeline opportunity", "Closed"]
counts = [1102, 20, 68, 33, 6]
pcts = [100.0, 1.8, 6.2, 3.0, 0.5]
fig = go.Figure(
    go.Funnel(
        y=stages,
        x=counts,
        text=[f"{c:,} ({p}%)" for c, p in zip(counts, pcts)],
        textinfo="text",
        textfont={"size": 13, "color": "#F9FAFB"},
        marker=dict(color=[PINK, "#E56B8A", PINK_DEEP, "#5A0026", "#44001B"], line=dict(width=0)),
        connector=dict(line=dict(color="rgba(156,163,175,0.35)", dash="dot", width=2)),
    )
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
    height=420,
    margin=dict(t=56, b=20, l=200, r=40),
    title=dict(text="Lead to closed", font=dict(size=16, color=INK)),
)
fig.update_xaxes(visible=False)
fig.update_yaxes(color=INK)
display(fig)
