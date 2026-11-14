# Participation tab — Attendance view
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

PINK = "#FF91AC"
PINK_MID = "#FFBCCA"
PINK_LIGHT = "#FFD0D9"
PINK_DEEP = "#87003C"
CORAL = PINK
BLUE = "#5B8FC7"
MUTED = "#94A3B8"
AMBER = "#FDBA74"
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


# Paid + Free only; Expired and Cancelled excluded. Snapshot from In The Loop Registrations
# tab Pacing (Detailed), last real day 2026-10-10. Goal is 850 unique people, not 6,000.
TICKET_SALES = """
2026-07-30,43,11,11,0,21,43
2026-07-31,17,19,11,0,30,60
2026-08-01,1,19,11,0,31,61
2026-08-02,3,19,11,0,34,64
2026-08-03,16,30,12,0,38,80
2026-08-04,12,34,14,0,43,91
2026-08-05,17,40,18,5,45,108
2026-08-06,11,45,18,7,48,118
2026-08-07,2,46,18,7,49,120
2026-08-08,0,46,18,7,49,120
2026-08-09,5,48,19,7,51,125
2026-08-10,4,49,19,7,54,129
2026-08-11,15,54,27,7,56,144
2026-08-12,3,54,27,7,59,147
2026-08-13,3,55,27,9,59,150
2026-08-14,30,57,31,13,78,179
2026-08-15,8,57,33,15,82,187
2026-08-16,5,58,34,15,85,192
2026-08-17,9,61,35,16,88,200
2026-08-18,12,69,37,16,90,212
2026-08-19,17,78,40,18,91,227
2026-08-20,20,92,44,19,92,245
2026-08-21,24,111,49,19,92,268
2026-08-22,1,111,49,19,93,269
2026-08-23,1,111,49,19,94,270
2026-08-24,5,113,51,20,94,275
2026-08-25,3,113,53,21,94,278
2026-08-26,10,114,59,21,96,287
2026-08-27,8,116,62,22,98,295
2026-08-28,22,117,62,22,114,310
2026-08-29,6,117,62,22,118,314
2026-08-30,1,117,62,22,119,315
2026-08-31,9,118,65,22,121,321
2026-09-01,18,122,71,22,127,337
2026-09-02,7,123,73,22,130,343
2026-09-03,7,126,73,23,131,348
2026-09-04,8,128,77,23,132,355
2026-09-05,1,128,78,23,132,356
2026-09-06,3,129,78,23,133,358
2026-09-07,10,135,82,23,133,367
2026-09-08,5,138,83,23,133,371
2026-09-09,9,145,85,23,133,380
2026-09-10,13,156,86,23,133,392
2026-09-11,11,164,88,23,133,402
2026-09-12,2,165,88,23,134,404
2026-09-13,0,165,88,23,134,404
2026-09-14,9,172,89,24,134,413
2026-09-15,18,185,91,24,135,429
2026-09-16,29,205,93,24,135,451
2026-09-17,97,231,159,24,136,544
2026-09-18,6,237,159,24,136,550
2026-09-19,5,242,159,24,136,555
2026-09-20,1,243,159,24,136,556
2026-09-21,23,257,162,24,138,574
2026-09-22,23,277,162,24,138,593
2026-09-23,15,291,163,24,138,607
2026-09-24,41,311,176,25,138,640
2026-09-25,24,327,183,25,138,661
2026-09-26,1,328,183,25,138,662
2026-09-27,1,328,183,25,139,663
2026-09-28,15,339,186,25,139,677
2026-09-29,30,355,190,25,139,697
2026-09-30,78,419,203,26,139,775
2026-10-01,42,450,205,26,140,808
2026-10-02,26,470,206,26,140,829
2026-10-03,2,471,206,26,141,831
2026-10-04,5,475,207,26,141,836
2026-10-05,39,502,211,27,141,866
2026-10-06,44,538,214,27,141,903
2026-10-07,6,544,214,27,141,909
2026-10-08,29,547,239,27,142,938
2026-10-09,3,550,239,27,142,941
2026-10-10,102,652,239,27,142,1043
"""
TICKET_GOAL = 850
TICKET_CAMPAIGN_DAYS = 77


def _ticket_rows():
    rows = []
    running = 0
    for line in TICKET_SALES.strip().splitlines():
        day, daily, ga, exp, node, amb, people = line.split(",")
        daily = int(daily)
        running += daily
        rows.append(
            {
                "day": day,
                "daily": daily,
                "registrations": running,
                "ga": int(ga),
                "exp": int(exp),
                "node": int(node),
                "amb": int(amb),
                "people": int(people),
            }
        )
    return rows


def _ticket_pace(rows):
    days = [r["day"] for r in rows]
    pace = [round(TICKET_GOAL * (i + 1) / TICKET_CAMPAIGN_DAYS) for i in range(len(rows))]
    fig = go.Figure()
    fig.add_bar(
        name="Daily",
        x=days,
        y=[r["daily"] for r in rows],
        marker=dict(color=PINK, line=dict(width=0)),
        hoverinfo="skip",
    )
    fig.add_scatter(
        name="Cumulative",
        x=days,
        y=[r["registrations"] for r in rows],
        mode="lines",
        line=dict(color=PINK_DEEP, width=2.6),
        yaxis="y2",
        hoverinfo="skip",
    )
    fig.add_scatter(
        name="Pace to 850",
        x=days,
        y=pace,
        mode="lines",
        line=dict(color=INK, width=1.4, dash="dash"),
        yaxis="y2",
        hoverinfo="skip",
    )
    return _theme(
        fig,
        height=380,
        axes=False,
        title=dict(text="Ticket sales · daily and cumulative", font=dict(size=16, color=INK)),
        yaxis=dict(title="Daily", showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK),
        yaxis2=dict(
            title="Cumulative",
            overlaying="y",
            side="right",
            range=[0, 1250],
            showgrid=False,
            zeroline=False,
            color=INK,
        ),
        xaxis=dict(type="date", tickformat="%d %b", dtick=86400000 * 7, tickangle=-30, color=INK),
        legend=dict(orientation="h", yanchor="top", y=-0.18, x=0, bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=52, b=96, l=48, r=56),
    )


def _ticket_types(rows):
    days = [r["day"] for r in rows]
    fig = go.Figure()
    for name, key, color in (
        ("Node Partners", "node", "#6B7280"),
        ("Ambassadors", "amb", PINK_MID),
        ("Expert + Strategic", "exp", PINK_DEEP),
        ("General Admission", "ga", PINK),
    ):
        fig.add_scatter(
            name=name,
            x=days,
            y=[r[key] for r in rows],
            mode="lines",
            line=dict(width=0.6, color=color),
            stackgroup="tickets",
            fillcolor=color,
            hoverinfo="skip",
        )
    fig.add_scatter(
        name="Goal 850",
        x=days,
        y=[TICKET_GOAL] * len(rows),
        mode="lines",
        line=dict(color=INK, width=1.4, dash="dash"),
        hoverinfo="skip",
    )
    return _theme(
        fig,
        height=360,
        axes=False,
        title=dict(text="Ticket sales · unique people by type", font=dict(size=16, color=INK)),
        yaxis_title="Unique people",
        xaxis=dict(type="date", tickformat="%d %b", dtick=86400000 * 7, tickangle=-30, color=INK),
        legend=dict(orientation="h", yanchor="top", y=-0.18, x=0, bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=52, b=96, l=48, r=24),
    )


def _ticket_table(rows):
    last = rows[-1]
    return _brand_table(
        pd.DataFrame(
            {
                "type": [
                    "General Admission (Public)",
                    "Expert + Strategic Partners",
                    "Node Partners",
                    "Ambassadors",
                    "Total unique people",
                    "Registrations (Paid + Free)",
                ],
                "target": ["300", "250", "150", "150", "850", ""],
                "people": [
                    f"{last['ga']:,}",
                    f"{last['exp']:,}",
                    f"{last['node']:,}",
                    f"{last['amb']:,}",
                    f"{last['people']:,}",
                    f"{last['registrations']:,}",
                ],
                "vs_target": [
                    f"{round(100 * last['ga'] / 300)}%",
                    f"{round(100 * last['exp'] / 250)}%",
                    f"{round(100 * last['node'] / 150)}%",
                    f"{round(100 * last['amb'] / 150)}%",
                    f"{round(100 * last['people'] / TICKET_GOAL)}%",
                    "",
                ],
            }
        ),
        "Ticket sales · vs 850 unique-people goal",
    )


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

ticket_rows = _ticket_rows()
display(_ticket_pace(ticket_rows))
display(_ticket_types(ticket_rows))
display(_ticket_table(ticket_rows))

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
display(_brand_table(mix, "Role and seniority mix"))

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
display(_brand_table(also, "Also on site"))
