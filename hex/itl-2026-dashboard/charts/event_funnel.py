# APP: Chart · Event people funnel — one figure. Classic App only shows the first display().
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


stages = ["Registered", "Attended", "Meeting booked", "Opportunity", "Closed Won"]
counts = [1119, 837, 20, 70, 6]
pcts = [100.0, 74.8, 1.8, 6.3, 0.5]
fig = go.Figure(go.Funnel(y=stages, x=counts, text=[f"{c:,} ({p}%)" for c, p in zip(counts, pcts)], textinfo="text", textfont={"size": 13, "color": "#F9FAFB"}, marker=dict(color=[PINK, "#E56B8A", PINK_DEEP, "#5A0026", "#44001B"], line=dict(width=0)), connector=dict(line=dict(color="rgba(156,163,175,0.35)", dash="dot", width=2))))
_theme(fig, height=400, axes=False, title=dict(text="Event people · CampaignMember attendance", font=dict(size=16, color=INK)), margin=dict(t=56, b=20, l=220, r=40))
fig.update_xaxes(visible=False)
fig.update_yaxes(color=INK)
display(fig)
