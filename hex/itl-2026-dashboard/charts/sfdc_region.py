# APP: Chart · SFDC by region — one figure. Classic App only shows the first display().
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
    "DACH": [270, 186, 179, 102, 13, 14],
    "North EMEA": [43, 38, 23, 21, 4, 1],
    "South EMEA": [54, 13, 14, 14, 5, 0],
    "US": [36, 15, 29, 25, 2, 0],
    "Other": [283, 62, 24, 15, 6, 4],
}
colors = {"DACH": PINK, "North EMEA": PINK_MID, "South EMEA": PINK_DEEP, "US": BLUE, "Other": "#6B7280"}
fig = go.Figure()
for name, xs in series.items():
    fig.add_bar(name=name, y=statuses, x=xs, orientation="h", marker=dict(color=colors[name], line=dict(width=0)), text=[f"{v:,}" if v else "" for v in xs], textposition="outside", textfont={"size": 11, "color": INK}, cliponaxis=False)
fig.update_layout(barmode="group", bargap=0.28, yaxis=dict(autorange="reversed"))
display(_theme(fig, height=400, title=dict(text="SFDC lead reached · region", font=dict(size=16, color=INK)), xaxis_title="People ever reached", margin=dict(t=56, b=28, l=110, r=56)))
