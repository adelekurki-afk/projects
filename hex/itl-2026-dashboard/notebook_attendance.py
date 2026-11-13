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
        title=dict(text="Attendance · 1,018 unique, 324 both days", font=dict(size=16, color=INK)),
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

display(
    _pair(
        "Region per day · Salesforce Attended (not Fliplet 426 / 916)",
        "Partner Day",
        [("EMEA", 194), ("Unknown", 154), ("NA", 48), ("LATAM", 5), ("APAC", 1), ("ANZ", 1)],
        "Ecosystem Day",
        [("EMEA", 415), ("Unknown", 358), ("NA", 80), ("APAC", 8), ("LATAM", 4)],
    )
)
display(
    _pair(
        "Sales segment per day · Salesforce Attended",
        "Partner Day",
        [("Unknown", 149), ("MM", 138), ("ENT", 64), ("SMB", 52)],
        "Ecosystem Day",
        [("Unknown", 343), ("MM", 304), ("ENT", 158), ("SMB", 60)],
    )
)
display(
    _pair(
        "Seniority · title on Salesforce Attended",
        "Partner Day",
        [
            ("Exec / founder", 87),
            ("Manager / lead", 83),
            ("IC / practitioner", 69),
            ("Other", 61),
            ("Director / head of", 42),
            ("Unknown title", 28),
            ("Partner / consultant", 28),
            ("VP", 4),
        ],
        "Ecosystem Day",
        [
            ("IC / practitioner", 206),
            ("Manager / lead", 187),
            ("Other", 145),
            ("Exec / founder", 130),
            ("Director / head of", 90),
            ("Partner / consultant", 56),
            ("Unknown title", 45),
            ("VP", 6),
        ],
    )
)

sessions = pd.DataFrame(
    {
        "zone": [
            "Community Lounge",
            "Cardputer Station",
            "Solution Zone n8n",
            "Candy Station",
            "Coffee Station",
            "Solution Zone Exhibitors",
            "Connection Zone",
            "Session ratings 4.8/5 (n=66)",
        ],
        "scans": [484, 425, 377, 350, 335, 293, 252, 66],
    }
)
meetings = pd.DataFrame(
    {
        "clock": ["Fliplet booked", "Meeting arrivals", "Sales meetings sheet", "Salesforce meeting booked"],
        "count": [1076, 425, 23, 20],
    }
)
feedback = pd.DataFrame(
    {
        "survey": [
            "Ecosystem recommend (n=43, NPS 72)",
            "Partner Day overall (n=23)",
            "Session rating (n=66)",
        ],
        "score": ["9.1 / 10", "8.8 / 10", "4.8 / 5"],
    }
)
display(sessions)
display(meetings)
display(feedback)
