# APP: Chart · Who came which days — one figure. Classic App only shows the first display().
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
fig.add_bar(name="Partner only", x=[102], y=["1,018 unique"], orientation="h", marker_color=MUTED, text=["102"], textposition="inside", insidetextanchor="middle")
fig.add_bar(name="Both days", x=[324], y=["1,018 unique"], orientation="h", marker_color=CORAL, text=["324"], textposition="inside", insidetextanchor="middle", textfont={"color": "#F9FAFB"})
fig.add_bar(name="Ecosystem only", x=[592], y=["1,018 unique"], orientation="h", marker_color=BLUE, text=["592"], textposition="inside", insidetextanchor="middle", textfont={"color": "#F9FAFB"})
display(_theme(fig, height=200, barmode="stack", title=dict(text="Who came which days", font=dict(size=16, color=INK)), xaxis_title="People", margin=dict(t=52, b=36, l=100, r=20)))
