# APP: Chart · Pipeline mix — one figure. Classic App only shows the first display().
import plotly.graph_objects as go
from IPython.display import display

PINK = "#FF91AC"
PINK_MID = "#FFBCCA"
PINK_DEEP = "#87003C"
BLUE = "#5B8FC7"
INK = "#9CA3AF"
CORAL = PINK
MUTED = "#94A3B8"
AMBER = "#FDBA74"


def _theme(fig, height=300, axes=True, **kw):
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
        height=height,
        margin=dict(t=52, b=36, l=16, r=24),
        legend=dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)"),
    )
    layout.update(kw)
    fig.update_layout(**layout)
    if axes:
        fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
    return fig


labels = ["New Business / ENT", "New Business / MM", "Expansion / ENT", "Expansion / MM"]
open_amt = [826000, 597200, 516150, 488073]
won_amt = [8000, 22000, 0, 3640]
fig = go.Figure()
fig.add_bar(name="Open", x=labels, y=open_amt, marker_color=BLUE)
fig.add_bar(name="Won", x=labels, y=won_amt, marker_color=CORAL)
display(_theme(fig, height=300, barmode="stack", title=dict(text="Opportunities · NB + Expansion from 12 Oct", font=dict(size=16, color=INK)), yaxis_title="€"))
