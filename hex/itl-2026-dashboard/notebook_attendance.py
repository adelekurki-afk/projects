import plotly.graph_objects as go
from IPython.display import display

# Self-contained. Do not reference Hex dataframes defined later in the notebook —
# App runs top-to-bottom, and a forward reference red-errors this cell.


def _empty(msg):
    fig = go.Figure()
    fig.add_annotation(text=msg, showarrow=False, font=dict(size=14, color="#6B7280"))
    fig.update_layout(
        height=180,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(t=20, b=20, l=20, r=20),
        font=dict(family="Inter, Arial, sans-serif", color="#333"),
    )
    return fig


def _pair(title, left_title, left_rows, right_title, right_rows):
    from plotly.subplots import make_subplots

    n = max(len(left_rows), len(right_rows), 1)
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(left_title, right_title),
        horizontal_spacing=0.18,
    )
    for col, rows, color in (
        (1, left_rows, "#FF6D5A"),
        (2, right_rows, "#4F7FB8"),
    ):
        names = [name for name, _ in rows][::-1]
        vals = [val for _, val in rows][::-1]
        fig.add_bar(
            y=names,
            x=vals,
            orientation="h",
            marker_color=color,
            text=vals,
            textposition="outside",
            showlegend=False,
            row=1,
            col=col,
        )
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        height=max(280, 28 * n + 140),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=80, b=30, l=20, r=50),
        font=dict(family="Inter, Arial, sans-serif", color="#333", size=12),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#F0F0F0")
    return fig


def _bars(title, rows, color="#FF6D5A"):
    names = [name for name, _ in rows][::-1]
    vals = [val for _, val in rows][::-1]
    fig = go.Figure(
        go.Bar(
            y=names,
            x=vals,
            orientation="h",
            marker_color=color,
            text=vals,
            textposition="outside",
        )
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        height=max(260, 28 * len(rows) + 100),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=60, b=30, l=20, r=50),
        font=dict(family="Inter, Arial, sans-serif", color="#333", size=12),
        xaxis=dict(showgrid=True, gridcolor="#F0F0F0"),
    )
    return fig


try:
    days = go.Figure(
        go.Bar(
            x=["Partner Day · 13 Oct", "Ecosystem Day · 14 Oct"],
            y=[426, 916],
            marker_color=["#FF6D5A", "#4F7FB8"],
            text=["426", "916"],
            textposition="outside",
        )
    )
    days.update_layout(
        title=dict(
            text="Attendance · people per day (Fliplet) · 1,018 unique, 324 both days",
            font=dict(size=16),
        ),
        height=300,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=60, b=40, l=40, r=20),
        font=dict(family="Inter, Arial, sans-serif", color="#333"),
        yaxis=dict(title="People", showgrid=True, gridcolor="#F0F0F0"),
    )
    display(days)

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
    display(
        _bars(
            "Attendance to sessions · Fliplet (no named session-scan column)",
            [
                ("Community Lounge", 484),
                ("Cardputer Station", 425),
                ("Solution Zone n8n", 377),
                ("Candy Station", 350),
                ("Coffee Station", 335),
                ("Solution Zone Exhibitors", 293),
                ("Connection Zone", 252),
                ("Session ratings 4.8/5 (n=66)", 66),
            ],
        )
    )
    display(
        _bars(
            "Attendance to meetings",
            [
                ("Fliplet booked", 1076),
                ("Meeting arrivals", 425),
                ("Sales meetings sheet", 23),
                ("Salesforce meeting booked", 20),
            ],
            "#4F7FB8",
        )
    )
    display(
        _bars(
            "Feedback sheets · Partner Day overall 8.6/10 (22 surveys). No Ecosystem Day survey in Drive.",
            [
                ("Partner Day overall (x10)", 86),
                ("Session rating (x10, from /5)", 48),
            ],
        )
    )
except Exception as err:
    display(_empty("Attendance view: " + type(err).__name__))
