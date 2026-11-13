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
    if n >= 1_000_000:
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
pipe_opps, pipe_won_n = 29, 3
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

src_n, src_amt, src_won, src_won_n = 12, 1011000, 6400, 1
inf_n, inf_amt, inf_won, inf_won_n = 18, 1170491, 25640, 2
try:
    for _, r in itl_attribution_kpis.iterrows():
        bucket = str(r["bucket"])
        if bucket == "Sourced":
            src_n = _itl_int(r["opp_count"], src_n)
            src_amt = float(r["amount"])
            src_won = float(r["won_amount"])
            src_won_n = _itl_int(r["won_count"], src_won_n)
        elif bucket == "Influenced":
            inf_n = _itl_int(r["opp_count"], inf_n)
            inf_amt = float(r["amount"])
            inf_won = float(r["won_amount"])
            inf_won_n = _itl_int(r["won_count"], inf_won_n)
except Exception:
    pass

type_rows = []
try:
    for _, r in funnel_type_mix.iterrows():
        type_rows.append(
            (
                str(r["bucket"]),
                str(r["opp_type"]),
                _itl_int(r["opp_count"], 0),
                float(r["amount"]),
                float(r["open_amount"]),
                float(r["won_amount"]),
            )
        )
except Exception:
    type_rows = [
        ("Sourced", "Expansion", 6, 666000, 666000, 0),
        ("Sourced", "New Business", 6, 345000, 338600, 6400),
        ("Influenced", "New Business", 14, 1109000, 1087000, 22000),
        ("Influenced", "Expansion", 4, 61491, 57851, 3640),
    ]

days = go.Figure(
    go.Bar(
        x=["Partner Day · 87% of 487 tickets", "Ecosystem Day · 76% of 1,205 tickets"],
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
        title=dict(text="Participants per day", font=dict(size=16, color=INK)),
        yaxis_title="People",
    )
)

attr = go.Figure()
attr.add_bar(
    name="Total",
    x=["Sourced opps", "Influenced", "NB + Expansion"],
    y=[src_amt, inf_amt, pipe_total],
    marker_color=CORAL,
)
display(
    _theme(
        attr,
        height=280,
        title=dict(text="Sourced vs influenced vs pipeline", font=dict(size=16, color=INK)),
        yaxis_title="€",
    )
)

participants = pd.DataFrame(
    {
        "metric": [
            "Registered",
            "Partner Day",
            "Ecosystem Day",
            "Unique people",
            "Staff tickets",
            "Speakers",
            "CAB",
        ],
        "people": ["1,269", "426", "916", "1,018", "113", "116", "39"],
        "note": [
            "Paid + Free unique email",
            "13 Oct · 87% of 487 tickets",
            "14 Oct · 76% of 1,205 tickets",
            "324 came both days",
            "Inside 426 / 916, not extra",
            "Programme overlay",
            "11 members · 28 guests",
        ],
    }
)
display(participants)

sf = pd.DataFrame(
    {
        "stage": [name for name, _, _ in funnel],
        "people": [f"{count:,}" for _, count, _ in funnel],
        "pct_of_registered": [f"{pct:.1f}%" for _, _, pct in funnel],
    }
)
display(sf)

attribution = pd.DataFrame(
    {
        "bucket": ["Sourced opps", "Influenced", "NB + Expansion"],
        "opps": [src_n, inf_n, pipe_opps],
        "total": [_euro(src_amt), _euro(inf_amt), _euro(pipe_total)],
        "won": [
            f"{src_won_n} · {_euro(src_won)}",
            f"{inf_won_n} · {_euro(inf_won)}",
            f"{pipe_won_n} · {_euro(pipe_won)}",
        ],
    }
)
display(attribution)

mix = pd.DataFrame(
    {
        "attribution": [r[0] for r in type_rows],
        "type": [r[1] for r in type_rows],
        "opps": [r[2] for r in type_rows],
        "total": [_euro(r[3]) for r in type_rows],
        "open": [_euro(r[4]) for r in type_rows],
        "won": [_euro(r[5]) for r in type_rows],
    }
)
display(mix)

segment = pd.DataFrame(
    {
        "type_segment": [f"{t} / {s}" for t, s, *_ in pipe_mix],
        "opps": [n for _, _, n, *_ in pipe_mix],
        "total": [_euro(total) for _, _, _, total, *_ in pipe_mix],
        "open": [_euro(open_amt) for *_, open_amt, _ in pipe_mix],
        "won": [_euro(won) for *_, won in pipe_mix],
    }
)
display(segment)
