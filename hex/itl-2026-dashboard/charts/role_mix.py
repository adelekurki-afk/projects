# APP: Chart · Role mix — one figure. Classic App only shows the first display().
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


cuts = ["Segment · Unknown", "Segment · MM", "Segment · ENT", "Segment · SMB", "Seniority · Exec / founder", "Seniority · Manager / lead", "Seniority · IC / practitioner"]
partner = [149, 138, 64, 52, 87, 83, 69]
eco = [343, 304, 158, 60, 130, 187, 206]
fig = go.Figure()
fig.add_bar(name="Partner Day", y=cuts[::-1], x=partner[::-1], orientation="h", marker_color=CORAL)
fig.add_bar(name="Ecosystem Day", y=cuts[::-1], x=eco[::-1], orientation="h", marker_color=BLUE)
display(_theme(fig, height=360, barmode="group", title=dict(text="Role and seniority mix", font=dict(size=16, color=INK)), xaxis_title="People", margin=dict(t=52, b=36, l=180, r=20)))
