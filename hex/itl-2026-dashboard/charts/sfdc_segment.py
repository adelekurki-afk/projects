# APP: Chart · SFDC by sales segment — one figure. Classic App only shows the first display().
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


statuses = ["Suspect", "New", "Working", "Qualified", "Nurturing", "Unqualified"]
series = {
    "ENT": [57, 143, 78, 50, 2, 2],
    "MM": [169, 147, 147, 109, 8, 7],
    "SMB": [441, 21, 39, 17, 19, 9],
    "Unknown": [19, 3, 5, 1, 1, 1],
}
colors = {"ENT": PINK_DEEP, "MM": PINK, "SMB": PINK_MID, "Unknown": INK}
fig = go.Figure()
for name, xs in series.items():
    fig.add_bar(name=name, y=statuses, x=xs, orientation="h", marker=dict(color=colors[name], line=dict(width=0)), text=[f"{v:,}" if v else "" for v in xs], textposition="outside", textfont={"size": 11, "color": INK}, cliponaxis=False)
fig.update_layout(barmode="group", bargap=0.28, yaxis=dict(autorange="reversed"))
display(_theme(
    fig,
    height=430,
    title=dict(text="SFDC lead reached · sales segment", font=dict(size=16, color=INK)),
    xaxis_title="People ever reached",
    legend=dict(orientation="h", y=-0.22, x=0, bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
    margin=dict(t=52, b=88, l=110, r=56),
))
