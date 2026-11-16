# APP: Chart · product users · Europe and Germany — one figure.
import plotly.graph_objects as go
from IPython.display import display

PINK = "#FF91AC"
BLUE = "#5B8FC7"
INK = "#9CA3AF"
CORAL = PINK

weeks = ["2026-06-01","2026-06-08","2026-06-15","2026-06-22","2026-06-29","2026-07-06","2026-07-13","2026-07-20","2026-07-27","2026-08-03","2026-08-10","2026-08-17","2026-08-24","2026-08-31","2026-09-07","2026-09-14","2026-09-21","2026-09-28","2026-10-05","2026-10-12","2026-10-19","2026-10-26","2026-11-02"]
europe = [149067,148845,143143,137830,139776,138292,133489,133869,131347,127682,121891,125612,127717,131824,132958,135546,134938,136673,138148,137437,139485,137388,138488]
germany = [31419,32655,31726,30896,31672,31794,31353,31304,30329,30573,29219,30221,29770,29831,29704,30205,29962,30810,30960,31434,31717,31673,32038]
fig = go.Figure()
fig.add_scatter(x=weeks, y=europe, mode="lines", name="Europe", line=dict(color=BLUE, width=2))
fig.add_scatter(x=weeks, y=germany, mode="lines", name="Germany", line=dict(color=CORAL, width=2))
fig.add_vrect(x0="2026-10-12", x1="2026-10-18", fillcolor=CORAL, opacity=0.18, line_width=0, annotation_text="ITL week", annotation_position="top left", annotation_font=dict(color=INK, size=11))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
    height=320,
    margin=dict(t=56, b=36, l=48, r=16),
    title=dict(text="Product users · Europe and Germany", font=dict(size=16, color=INK)),
    yaxis_title="Weekly active users",
    legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"),
)
fig.update_xaxes(showgrid=False, color=INK)
fig.update_yaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
display(fig)
