# SFDC lead reached by sales segment and region. Live from sfdc_lead_reached_dims when SQL has run.
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

PINK = "#FF91AC"
PINK_MID = "#FFBCCA"
PINK_DEEP = "#87003C"
BLUE = "#5B8FC7"
INK = "#9CA3AF"


def _brand_table(df, title=""):
    frame = pd.DataFrame(df)
    cols = [str(c) for c in frame.columns]
    n = len(frame)
    vals = [[("" if v is None else str(v)) for v in frame[c].tolist()] for c in frame.columns]
    stub = [PINK_DEEP] * n
    numbers = ["#1B1F27" if i % 2 == 0 else "#141820" for i in range(n)]
    fills = [stub] + [numbers] * max(len(cols) - 1, 0)
    fonts = [["#F9FAFB"] * n] + [["#E5E7EB"] * n] * max(len(cols) - 1, 0)
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
                fill_color=fills,
                font=dict(color=fonts, size=12, family="Inter, Arial, sans-serif"),
                align="left",
                line_color="rgba(156,163,175,0.22)",
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


STATUS_ORDER = ["Suspect", "New", "Working", "Qualified", "Nurturing", "Unqualified"]
SEGMENT_ORDER = ["ENT", "MM", "SMB", "Unknown"]
REGION_ORDER = ["DACH", "North EMEA", "South EMEA", "US", "Other"]
SEGMENT_COLORS = {"ENT": "#87003C", "MM": PINK, "SMB": PINK_MID, "Unknown": "#9CA3AF"}
REGION_COLORS = {
    "DACH": PINK,
    "North EMEA": PINK_MID,
    "South EMEA": PINK_DEEP,
    "US": BLUE,
    "Other": "#6B7280",
}
segment_rows = [
    ("Suspect", "SMB", 441),
    ("Suspect", "MM", 169),
    ("Suspect", "ENT", 57),
    ("Suspect", "Unknown", 19),
    ("New", "MM", 147),
    ("New", "ENT", 143),
    ("New", "SMB", 21),
    ("New", "Unknown", 3),
    ("Working", "MM", 147),
    ("Working", "ENT", 78),
    ("Working", "SMB", 39),
    ("Working", "Unknown", 5),
    ("Qualified", "MM", 109),
    ("Qualified", "ENT", 50),
    ("Qualified", "SMB", 17),
    ("Qualified", "Unknown", 1),
    ("Nurturing", "SMB", 19),
    ("Nurturing", "MM", 8),
    ("Nurturing", "ENT", 2),
    ("Nurturing", "Unknown", 1),
    ("Unqualified", "SMB", 9),
    ("Unqualified", "MM", 7),
    ("Unqualified", "ENT", 2),
    ("Unqualified", "Unknown", 1),
]
region_rows = [
    ("Suspect", "Other", 283),
    ("Suspect", "DACH", 270),
    ("Suspect", "South EMEA", 54),
    ("Suspect", "North EMEA", 43),
    ("Suspect", "US", 36),
    ("New", "DACH", 186),
    ("New", "Other", 62),
    ("New", "North EMEA", 38),
    ("New", "US", 15),
    ("New", "South EMEA", 13),
    ("Working", "DACH", 179),
    ("Working", "US", 29),
    ("Working", "Other", 24),
    ("Working", "North EMEA", 23),
    ("Working", "South EMEA", 14),
    ("Qualified", "DACH", 102),
    ("Qualified", "US", 25),
    ("Qualified", "North EMEA", 21),
    ("Qualified", "Other", 15),
    ("Qualified", "South EMEA", 14),
    ("Nurturing", "DACH", 13),
    ("Nurturing", "Other", 6),
    ("Nurturing", "South EMEA", 5),
    ("Nurturing", "North EMEA", 4),
    ("Nurturing", "US", 2),
    ("Unqualified", "DACH", 14),
    ("Unqualified", "Other", 4),
    ("Unqualified", "North EMEA", 1),
]
try:
    dim_df = sfdc_lead_reached_dims
    segment_rows = [
        (str(r["sfdc_status"]), str(r["dim_value"]), int(r["people"]))
        for _, r in dim_df[dim_df["dim"] == "segment"].iterrows()
        if str(r["sfdc_status"]) in STATUS_ORDER
    ]
    region_rows = [
        (str(r["sfdc_status"]), str(r["dim_value"]), int(r["people"]))
        for _, r in dim_df[dim_df["dim"] == "region"].iterrows()
        if str(r["sfdc_status"]) in STATUS_ORDER
    ]
except Exception:
    pass


def _reached_by_dim(rows, series_order, colors, title):
    statuses = [s for s in STATUS_ORDER if any(str(r[0]) == s for r in rows)]
    lookup = {(str(r[0]), str(r[1])): int(r[2]) for r in rows}
    fig = go.Figure()
    for name in series_order:
        xs = [lookup.get((st, name), 0) for st in statuses]
        fig.add_bar(
            name=name,
            y=statuses,
            x=xs,
            orientation="h",
            marker=dict(color=colors.get(name, PINK), line=dict(width=0)),
            text=[f"{v:,}" if v else "" for v in xs],
            textposition="outside",
            textfont={"size": 11, "color": INK},
            cliponaxis=False,
            hoverinfo="skip",
        )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
        height=400,
        margin=dict(t=56, b=28, l=110, r=56),
        title=dict(text=title, font=dict(size=16, color=INK)),
        barmode="group",
        bargap=0.28,
        bargroupgap=0.06,
        legend=dict(orientation="h", y=1.1, bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK, title="People ever reached"),
        yaxis=dict(autorange="reversed", showgrid=False, zeroline=False, ticks="", tickfont=dict(size=13, color=INK)),
    )
    return fig


def _dim_table(rows, series_order, title):
    statuses = [s for s in STATUS_ORDER if any(str(r[0]) == s for r in rows)]
    lookup = {(str(r[0]), str(r[1])): int(r[2]) for r in rows}
    data = {"status": statuses}
    for name in series_order:
        data[name] = [lookup.get((st, name), 0) for st in statuses]
    return _brand_table(pd.DataFrame(data), title)


display(_reached_by_dim(segment_rows, SEGMENT_ORDER, SEGMENT_COLORS, "SFDC lead reached · sales segment"))
display(_reached_by_dim(region_rows, REGION_ORDER, REGION_COLORS, "SFDC lead reached · region"))
display(_dim_table(segment_rows, SEGMENT_ORDER, "SFDC lead reached · sales segment"))
display(_dim_table(region_rows, REGION_ORDER, "SFDC lead reached · region"))
