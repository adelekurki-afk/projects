# APP: Chart · Staff by crew — one figure. Classic App only shows the first display().
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


fig = go.Figure(go.Bar(y=["Other crew", "n8n (staff ticket)", "Content / merch / film", "Hospitality / QT Events", "C2"], x=[5, 13, 19, 36, 40], orientation="h", marker_color=PINK_DEEP, text=[5, 13, 19, 36, 40], textposition="outside", textfont={"color": INK}, cliponaxis=False))
display(_theme(fig, height=280, title=dict(text="Staff tickets by crew", font=dict(size=16, color=INK)), xaxis_title="Registered"))
