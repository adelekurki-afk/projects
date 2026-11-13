import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

CORAL = "#FF6D5A"
BLUE = "#5B8FC7"
INK = "#9CA3AF"


def _theme(fig, height=300, axes=True, **kw):
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
        height=height,
        margin=dict(t=52, b=28, l=8, r=16),
        legend=dict(orientation="h", y=1.14, bgcolor="rgba(0,0,0,0)"),
    )
    layout.update(kw)
    fig.update_layout(**layout)
    if axes:
        fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
        fig.update_yaxes(showgrid=False, zeroline=False, color=INK)
    return fig


def _itl_int(value, default):
    try:
        if value is None:
            return default
        return int(value)
    except Exception:
        return default


def _euro(n):
    n = int(round(float(n)))
    if abs(n) >= 1_000_000:
        return f"€{n / 1_000_000:.2f}M"
    if abs(n) >= 10_000:
        return f"€{n / 1_000:.0f}k"
    return f"€{n:,}"


_STAGE_SHORT = {
    "Registered": "Registered",
    "Attended (Eco Day or Partner Day)": "Attended",
    "Had n8n Meeting": "Meeting booked",
    "Account with Opp (NB/Exp, >= Oct 12)": "Opportunity",
    "Closed Won": "Closed Won",
}
funnel = [
    ("Registered", 1119, 100.0),
    ("Attended", 837, 74.8),
    ("Meeting booked", 20, 1.8),
    ("Opportunity", 70, 6.3),
    ("Closed Won", 6, 0.5),
]
try:
    funnel = [
        (
            _STAGE_SHORT.get(str(r["stage"]), str(r["stage"])),
            _itl_int(r["count"], 0),
            float(r["pct_of_registered"]),
        )
        for _, r in lead_funnel.iterrows()
    ]
except Exception:
    pass

pipe_total, pipe_open, pipe_won = 2461063, 2427423, 33640
pipe_opps, pipe_won_n, pipe_meetings = 29, 3, 1
pipe_mix = [
    ("New Business", "ENT", 5, 834000, 826000, 8000),
    ("New Business", "MM", 12, 619200, 597200, 22000),
    ("Expansion", "ENT", 4, 516150, 516150, 0),
    ("Expansion", "MM", 8, 491713, 488073, 3640),
]
try:
    df = pipeline_arr
    pipe_total = int(round(float(df["total_amount"].sum())))
    pipe_open = int(round(float(df["open_pipeline_amount"].sum())))
    pipe_won = int(round(float(df["closed_won_amount"].sum())))
    pipe_opps = int(df["opp_count"].sum())
    pipe_won_n = int(df["closed_won_count"].sum())
    if "opps_from_meetings" in df.columns:
        pipe_meetings = int(df["opps_from_meetings"].sum())
    pipe_mix = [
        (
            str(r["opp_type"]),
            str(r["segment"]),
            _itl_int(r["opp_count"], 0),
            float(r["total_amount"]),
            float(r["open_pipeline_amount"]),
            float(r["closed_won_amount"]),
        )
        for _, r in df.iterrows()
    ]
except Exception:
    pass

kpis = go.Figure()
for i, (value, title, color, fmt, prefix, suffix) in enumerate(
    (
        (1018, "Unique people", CORAL, ",", "", ""),
        (426, "Partner Day", CORAL, ",", "", ""),
        (916, "Ecosystem Day", BLUE, ",", "", ""),
        (pipe_total / 1_000_000, "NB + Expansion", CORAL, ".2f", "€", "M"),
    )
):
    kpis.add_trace(
        go.Indicator(
            mode="number",
            value=value,
            number={
                "font": {"size": 36, "color": color},
                "valueformat": fmt,
                "prefix": prefix,
                "suffix": suffix,
            },
            title={"text": title, "font": {"size": 13, "color": INK}},
            domain={"x": [i * 0.25, i * 0.25 + 0.24], "y": [0, 1]},
        )
    )
display(_theme(kpis, height=160, axes=False))

stages = [s for s, _, _ in funnel][::-1]
counts = [c for _, c, _ in funnel][::-1]
conv = go.Figure(
    go.Bar(
        y=stages,
        x=counts,
        orientation="h",
        marker_color=CORAL,
        text=[f"{c:,}" for c in counts],
        textposition="outside",
        textfont={"color": INK},
        cliponaxis=False,
    )
)
display(
    _theme(
        conv,
        height=280,
        title=dict(text="Salesforce conversion", font=dict(size=16, color=INK)),
        xaxis_title="People",
    )
)

mix = go.Figure()
labels = [f"{t} / {s}" for t, s, _, _, _, _ in pipe_mix]
mix.add_bar(name="Open", x=labels, y=[o for *_, o, _ in pipe_mix], marker_color=BLUE)
mix.add_bar(name="Won", x=labels, y=[w for *_, w in pipe_mix], marker_color=CORAL)
display(
    _theme(
        mix,
        height=300,
        barmode="stack",
        title=dict(text="Opportunities · NB + Expansion from 12 Oct", font=dict(size=16, color=INK)),
        yaxis_title="€",
    )
)

visits = pd.DataFrame(
    {
        "metric": [
            "Registered",
            "Came · Partner Day",
            "Came · Ecosystem Day",
            "Unique people",
            "Staff tickets",
            "Programme speakers",
            "CAB overlay",
        ],
        "people": ["1,269", "426", "916", "1,018", "113", "116", "39"],
        "how_built": [
            "Paid + Free unique email",
            "13 Oct · 391 door + 35 badge",
            "14 Oct · 878 door + 38 green YES",
            "426 + 916 − 324 both days",
            "Overlay, not extra headcount",
            "Overlay, not extra headcount",
            "11 members · 28 guests",
        ],
    }
)
display(visits)

pipe_summary = pd.DataFrame(
    {
        "metric": ["NB + Expansion total", "Open", "Won"],
        "amount": [_euro(pipe_total), _euro(pipe_open), _euro(pipe_won)],
        "opps": [pipe_opps, "", pipe_won_n],
    }
)
display(pipe_summary)

opps = pd.DataFrame(
    {
        "type_segment": [f"{t} / {s}" for t, s, *_ in pipe_mix],
        "opps": [n for _, _, n, *_ in pipe_mix],
        "total": [_euro(total) for _, _, _, total, *_ in pipe_mix],
        "open": [_euro(open_amt) for *_, open_amt, _ in pipe_mix],
        "won": [_euro(won) for *_, won in pipe_mix],
    }
)
display(opps)
