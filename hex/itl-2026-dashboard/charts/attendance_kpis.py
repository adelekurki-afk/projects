# APP: Chart · Attendance KPIs — one figure. Classic App only shows the first display().
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
for i, (value, title, color) in enumerate(((426, "Partner Day", CORAL), (916, "Ecosystem Day", BLUE), (1018, "Unique people", CORAL), (324, "Both days", MUTED))):
    fig.add_trace(go.Indicator(mode="number", value=value, number={"font": {"size": 36, "color": color}, "valueformat": ","}, title={"text": title, "font": {"size": 13, "color": INK}}, domain={"x": [i * 0.25, i * 0.25 + 0.24], "y": [0, 1]}))
display(_theme(fig, height=160, axes=False))
