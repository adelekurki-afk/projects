# APP: Chart · SFDC Lead vs Contact — one figure. Classic App only shows the first display().
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


rows = [("Suspect", 546, 140), ("New", 302, 18), ("Working", 71, 206), ("Qualified", 135, 56), ("Nurturing", 27, 3), ("Unqualified", 7, 12)]
fig = go.Figure()
fig.add_bar(name="Lead", y=[r[0] for r in rows], x=[r[1] for r in rows], orientation="h", marker=dict(color=PINK, line=dict(width=0)), text=[f"{r[1]:,}" for r in rows], textposition="outside", textfont={"size": 12, "color": INK}, cliponaxis=False, width=0.36)
fig.add_bar(name="Contact", y=[r[0] for r in rows], x=[r[2] for r in rows], orientation="h", marker=dict(color=PINK_DEEP, line=dict(width=0)), text=[f"{r[2]:,}" for r in rows], textposition="outside", textfont={"size": 12, "color": INK}, cliponaxis=False, width=0.36)
fig.update_layout(barmode="group", bargap=0.28, bargroupgap=0.08, yaxis=dict(autorange="reversed"))
display(_theme(
    fig,
    height=400,
    title=dict(text="SFDC lead reached · Lead and Contact", font=dict(size=16, color=INK)),
    xaxis_title="People ever reached",
    legend=dict(orientation="h", y=-0.18, x=0, bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
    margin=dict(t=52, b=80, l=110, r=64),
))
