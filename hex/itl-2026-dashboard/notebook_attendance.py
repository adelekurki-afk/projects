# Participation tab — Attendance view
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

CORAL = "#FF6D5A"
BLUE = "#5B8FC7"
MUTED = "#94A3B8"
AMBER = "#FDBA74"
INK = "#9CA3AF"


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


def _pair(title, left_title, left_rows, right_title, right_rows):
    from plotly.subplots import make_subplots

    fig = make_subplots(rows=1, cols=2, subplot_titles=(left_title, right_title), horizontal_spacing=0.16)
    for col, rows, color in ((1, left_rows, CORAL), (2, right_rows, BLUE)):
        names = [n for n, _ in rows][::-1]
        vals = [v for _, v in rows][::-1]
        fig.add_bar(
            y=names,
            x=vals,
            orientation="h",
            marker_color=color,
            text=vals,
            textposition="outside",
            textfont={"color": INK},
            showlegend=False,
            cliponaxis=False,
            row=1,
            col=col,
        )
    n = max(len(left_rows), len(right_rows), 1)
    _theme(fig, height=max(260, 28 * n + 120), title=dict(text=title, font=dict(size=16, color=INK)))
    fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", color=INK)
    fig.update_yaxes(showgrid=False, color=INK)
    return fig


kpis = go.Figure()
for i, (value, title, color) in enumerate(
    (
        (426, "Partner Day", CORAL),
        (916, "Ecosystem Day", BLUE),
        (1018, "Unique people", CORAL),
        (324, "Both days", MUTED),
    )
):
    kpis.add_trace(
        go.Indicator(
            mode="number",
            value=value,
            number={"font": {"size": 36, "color": color}, "valueformat": ","},
            title={"text": title, "font": {"size": 13, "color": INK}},
            domain={"x": [i * 0.25, i * 0.25 + 0.24], "y": [0, 1]},
        )
    )
display(_theme(kpis, height=160, axes=False))

built = go.Figure()
built.add_bar(
    name="Door scans",
    x=["Partner Day", "Ecosystem Day"],
    y=[391, 878],
    marker_color=CORAL,
    text=["391", "878"],
    textposition="inside",
    insidetextanchor="middle",
    textfont={"color": "#F9FAFB"},
)
built.add_bar(
    name="Badge / green YES",
    x=["Partner Day", "Ecosystem Day"],
    y=[35, 38],
    marker_color=AMBER,
    text=["35", "38"],
    textposition="inside",
    insidetextanchor="middle",
)
display(
    _theme(
        built,
        height=280,
        barmode="stack",
        title=dict(text="How Fliplet visits are built · 426 and 916", font=dict(size=16, color=INK)),
        yaxis_title="People",
    )
)

uniq = go.Figure()
uniq.add_bar(
    name="Partner only",
    x=[102],
    y=["1,018 unique"],
    orientation="h",
    marker_color=MUTED,
    text=["102"],
    textposition="inside",
    insidetextanchor="middle",
)
uniq.add_bar(
    name="Both days",
    x=[324],
    y=["1,018 unique"],
    orientation="h",
    marker_color=CORAL,
    text=["324"],
    textposition="inside",
    insidetextanchor="middle",
    textfont={"color": "#F9FAFB"},
)
uniq.add_bar(
    name="Ecosystem only",
    x=[592],
    y=["1,018 unique"],
    orientation="h",
    marker_color=BLUE,
    text=["592"],
    textposition="inside",
    insidetextanchor="middle",
    textfont={"color": "#F9FAFB"},
)
display(
    _theme(
        uniq,
        height=200,
        barmode="stack",
        title=dict(text="Who came which days", font=dict(size=16, color=INK)),
        xaxis_title="People",
        margin=dict(t=52, b=36, l=100, r=20),
    )
)

zones = [
    ("Community Lounge", 484),
    ("Cardputer Station", 425),
    ("Solution Zone n8n", 377),
    ("Candy Station", 350),
    ("Coffee Station", 335),
    ("Solution Zone Exhibitors", 293),
    ("Connection Zone", 252),
]
zone_fig = go.Figure(
    go.Bar(
        y=[n for n, _ in zones][::-1],
        x=[v for _, v in zones][::-1],
        orientation="h",
        marker_color=CORAL,
        text=[v for _, v in zones][::-1],
        textposition="outside",
        textfont={"color": INK},
        cliponaxis=False,
    )
)
display(
    _theme(
        zone_fig,
        height=320,
        title=dict(text="Floor scans · not session headcount", font=dict(size=16, color=INK)),
        xaxis_title="Scans",
    )
)

display(
    _pair(
        "Region per day · Salesforce Attended (not Fliplet 426 / 916)",
        "Partner Day",
        [("EMEA", 194), ("Unknown", 154), ("NA", 48), ("LATAM", 5), ("APAC", 1), ("ANZ", 1)],
        "Ecosystem Day",
        [("EMEA", 415), ("Unknown", 358), ("NA", 80), ("APAC", 8), ("LATAM", 4)],
    )
)

mix = pd.DataFrame(
    {
        "cut": [
            "Segment · Unknown",
            "Segment · MM",
            "Segment · ENT",
            "Segment · SMB",
            "Seniority · Exec / founder",
            "Seniority · Manager / lead",
            "Seniority · IC / practitioner",
            "Seniority · Other",
            "Seniority · Director / head of",
            "Seniority · Partner / consultant",
            "Seniority · Unknown title",
            "Seniority · VP",
        ],
        "Partner Day": [149, 138, 64, 52, 87, 83, 69, 61, 42, 28, 28, 4],
        "Ecosystem Day": [343, 304, 158, 60, 130, 187, 206, 145, 90, 56, 45, 6],
    }
)
display(mix)

also = pd.DataFrame(
    {
        "item": [
            "Staff tickets",
            "Programme speakers",
            "CAB",
            "Fliplet booked meetings",
            "Meeting arrivals",
            "Sales meetings sheet",
            "Salesforce meeting booked",
            "Ecosystem recommend (n=43, NPS 72)",
            "Partner Day overall (n=23)",
            "Session rating (n=66)",
        ],
        "value": ["113", "116", "39", "1,076", "425", "23", "20", "9.1 / 10", "8.8 / 10", "4.8 / 5"],
        "note": [
            "Overlay inside 426 / 916, not extra headcount",
            "Overlay inside 426 / 916, not extra headcount",
            "11 members · 28 guests",
            "Fliplet bookings clock",
            "Arrivals clock",
            "n8n sales sheet",
            "Salesforce CampaignMember",
            "Shared Fliplet workbook",
            "Shared Fliplet workbook",
            "Session ratings 4.8/5",
        ],
    }
)
display(also)
