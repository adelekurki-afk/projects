# APP: Chart · How visits are built — one figure. Classic App only shows the first display().
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


fig = go.Figure()
fig.add_bar(
    name="Door scans",
    x=["Partner Day", "Ecosystem Day"],
    y=[391, 878],
    marker_color=CORAL,
    text=["391", "878"],
    textposition="inside",
    insidetextanchor="middle",
    textfont={"color": "#F9FAFB"},
)
fig.add_bar(
    name="Badge / green YES",
    x=["Partner Day", "Ecosystem Day"],
    y=[35, 38],
    marker_color=AMBER,
    text=["35", "38"],
    textposition="inside",
    insidetextanchor="middle",
)
display(_theme(fig, height=280, barmode="stack", title=dict(text="How Fliplet visits are built · 426 and 916", font=dict(size=16, color=INK)), yaxis_title="People"))
