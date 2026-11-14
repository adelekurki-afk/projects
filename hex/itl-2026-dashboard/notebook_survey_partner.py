# APP: Partner Day survey — Fillout, 13 Nov 2026 Europe/Madrid. 3 test rows dropped.
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

PINK = "#FF91AC"
PINK_MID = "#FFBCCA"
PINK_DEEP = "#87003C"
CORAL = PINK
BLUE = "#5B8FC7"
MUTED = "#94A3B8"
INK = "#9CA3AF"


def _brand_table(df, title=""):
    frame = pd.DataFrame(df)
    cols = [str(c) for c in frame.columns]
    n = len(frame)
    vals = [[("" if v is None else str(v)) for v in frame[c].tolist()] for c in frame.columns]
    stripe = [PINK_MID if i % 2 == 0 else "rgba(255,145,172,0.20)" for i in range(n)]
    fig = go.Figure(
        go.Table(
            header=dict(
                values=cols,
                fill_color=PINK_DEEP,
                font=dict(color="#F9FAFB", size=12, family="Inter, Arial, sans-serif"),
                align="left",
                line_color=PINK,
                height=30,
            ),
            cells=dict(
                values=vals,
                fill_color=[stripe] * len(cols),
                font=dict(color=INK, size=12, family="Inter, Arial, sans-serif"),
                align="left",
                line_color="rgba(255,145,172,0.35)",
                height=26,
            ),
        )
    )
    top = 44 if title else 8
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(text=title, font=dict(size=15, color=INK)) if title else None,
        height=min(max(top + 30 + 26 * max(n, 1) + 16, 110), 780),
        margin=dict(t=top, b=8, l=4, r=4),
        font=dict(family="Inter, Arial, sans-serif", color=INK),
    )
    return fig



def _theme(fig, height=300, axes=True, **kw):
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
    if axes:
        fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
        fig.update_yaxes(showgrid=False, zeroline=False, color=INK)
    return fig


kpis = go.Figure()
for i, (value, title, color, fmt) in enumerate(
    (
        (20, "Responses", CORAL, ","),
        (9.1, "Overall /10", CORAL, ".1f"),
        (75, "NPS-style", BLUE, ","),
        (8.7, "2027 plans /10", MUTED, ".1f"),
    )
):
    kpis.add_trace(
        go.Indicator(
            mode="number",
            value=value,
            number={"font": {"size": 36, "color": color}, "valueformat": fmt},
            title={"text": title, "font": {"size": 13, "color": INK}},
            domain={"x": [i * 0.25, i * 0.25 + 0.24], "y": [0, 1]},
        )
    )
display(_theme(kpis, height=160, axes=False))

overall = go.Figure(
    go.Bar(
        x=[8, 9, 10],
        y=[5, 8, 7],
        marker_color=CORAL,
        text=[5, 8, 7],
        textposition="outside",
        textfont={"color": INK},
        cliponaxis=False,
    )
)
display(
    _theme(
        overall,
        height=280,
        title=dict(text="Overall Partner Day (0–10) · n=20, tests dropped", font=dict(size=16, color=INK)),
        yaxis_title="Responses",
        xaxis=dict(dtick=1),
    )
)

tracks = go.Figure(
    go.Bar(
        y=["Node Partners", "Ambassadors", "Solution Partners"][::-1],
        x=[4, 8, 13][::-1],
        orientation="h",
        marker_color=BLUE,
        text=[4, 8, 13][::-1],
        textposition="outside",
        textfont={"color": INK},
        cliponaxis=False,
    )
)
display(
    _theme(
        tracks,
        height=240,
        title=dict(text="Tracks attended (multi-select)", font=dict(size=16, color=INK)),
        xaxis_title="People",
    )
)

display(
    _brand_table(
        pd.DataFrame(
            {
                "track": ["Solution Partners", "Ambassadors", "Node Partners"],
                "attended": [13, 8, 4],
                "content_mean": [8.46, 8.33, 7.50],
                "content_n": [13, 9, 4],
                "helps_work_closer": [8.69, 8.44, 7.25],
            }
        ),
        "Tracks attended",
    )
)

display(
    _brand_table(
        pd.DataFrame(
            {
                "score": [5, 6, 7, 8, 9, 10],
                "overall": [0, 0, 0, 5, 8, 7],
                "understand_2027": [1, 1, 2, 2, 8, 6],
            }
        ),
        "Score mix",
    )
)
