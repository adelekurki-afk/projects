# APP: Chart · n8n.io Germany users — one figure. Classic App only shows the first display().
import plotly.graph_objects as go
from IPython.display import display

PINK = "#FF91AC"
INK = "#9CA3AF"
CORAL = PINK

weeks = ["2026-06-01","2026-06-08","2026-06-15","2026-06-22","2026-06-29","2026-07-06","2026-07-13","2026-07-20","2026-07-27","2026-08-03","2026-08-10","2026-08-17","2026-08-24","2026-08-31","2026-09-07","2026-09-14","2026-09-21","2026-09-28","2026-10-05","2026-10-12","2026-10-19","2026-10-26","2026-11-02"]
germany = [12606,13511,12537,11727,12415,12054,12043,12136,13618,14579,11964,11695,12353,11403,9592,9928,9520,9699,9934,10563,10207,9029,8481]
fig = go.Figure()
fig.add_scatter(x=weeks, y=germany, mode="lines", name="Germany", line=dict(color=CORAL, width=2))
fig.add_vrect(x0="2026-10-12", x1="2026-10-18", fillcolor=CORAL, opacity=0.18, line_width=0, annotation_text="ITL week", annotation_position="top left", annotation_font=dict(color=INK, size=11))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
    height=320,
    margin=dict(t=56, b=36, l=48, r=16),
    title=dict(text="n8n.io users · Germany", font=dict(size=16, color=INK)),
    yaxis_title="Users",
    showlegend=False,
)
fig.update_xaxes(showgrid=False, color=INK)
fig.update_yaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
display(fig)
