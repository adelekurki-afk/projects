import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

CORAL = "#FF6D5A"
BLUE = "#5B8FC7"
MUTED = "#94A3B8"
INK = "#9CA3AF"


def _theme(fig, height=300, **kw):
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
        height=height,
        margin=dict(t=52, b=28, l=8, r=20),
        legend=dict(orientation="h", y=1.14, bgcolor="rgba(0,0,0,0)"),
    )
    layout.update(kw)
    fig.update_layout(**layout)
    fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
    fig.update_yaxes(showgrid=False, zeroline=False, color=INK)
    return fig


days = go.Figure(
    go.Bar(
        x=["Partner Day · 13 Oct", "Ecosystem Day · 14 Oct"],
        y=[426, 916],
        marker_color=[CORAL, BLUE],
        text=["426", "916"],
        textposition="outside",
        textfont={"color": INK},
        cliponaxis=False,
    )
)
display(
    _theme(
        days,
        height=280,
        title=dict(text="Participation · 1,018 unique people", font=dict(size=16, color=INK)),
        yaxis_title="People",
    )
)

split = go.Figure()
split.add_bar(name="Door", x=["Partner Day", "Ecosystem Day"], y=[391, 878], marker_color=CORAL)
split.add_bar(name="Badge / green YES", x=["Partner Day", "Ecosystem Day"], y=[35, 38], marker_color="#FDBA74")
display(
    _theme(
        split,
        height=280,
        barmode="stack",
        title=dict(text="How 426 and 916 are built", font=dict(size=16, color=INK)),
        yaxis_title="People",
    )
)

overlap = go.Figure(
    go.Bar(
        x=["Partner only", "Both days", "Ecosystem only"],
        y=[102, 324, 592],
        marker_color=[MUTED, CORAL, BLUE],
        text=["102", "324", "592"],
        textposition="outside",
        textfont={"color": INK},
        cliponaxis=False,
    )
)
display(_theme(overlap, height=260, title=dict(text="Who came which days", font=dict(size=16, color=INK))))

overlays = pd.DataFrame(
    {
        "overlay": ["Staff tickets", "Programme speakers", "CAB"],
        "people": [113, 116, 39],
        "note": [
            "Inside 426 / 916, not extra headcount",
            "Inside 426 / 916, not extra headcount",
            "11 members · 28 guests",
        ],
    }
)
display(overlays)
