# APP: SFDC lead reached. This cell is on the App — keep it CODE, not SQL.
# Live from sfdc_lead_reached when that SQL has already run; otherwise baked snapshot.
# Includes Leads (Lead.Status / LeadHistory) and Contacts (Status__c / ContactHistory).
# Grouped, not stacked: the same person can appear in both bars after conversion.
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

PINK = "#FF91AC"
PINK_MID = "#FFBCCA"
PINK_DEEP = "#87003C"
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

rows = [
    ("Suspect", 546, 140, 686, 62.3),
    ("New", 302, 18, 314, 28.5),
    ("Working", 71, 206, 269, 24.4),
    ("Qualified", 135, 56, 177, 16.1),
    ("Nurturing", 27, 3, 30, 2.7),
    ("Unqualified", 7, 12, 19, 1.7),
]
try:
    rows = [
        (
            str(r["sfdc_status"]),
            int(r["as_lead"]),
            int(r["as_contact"]),
            int(r["people_ever_reached"]),
            float(r["pct_of_itl"]),
        )
        for _, r in sfdc_lead_reached.iterrows()
        if str(r["sfdc_status"]) in ("Suspect", "New", "Working", "Qualified", "Nurturing", "Unqualified")
    ]
except Exception:
    pass

display(
    _brand_table(
        pd.DataFrame(
            {
                "status": ["Suspect", "New", "Working", "Qualified", "Nurturing", "Unqualified"],
                "ENT": [57, 143, 78, 50, 2, 2],
                "MM": [169, 147, 147, 109, 8, 7],
                "SMB": [441, 21, 39, 17, 19, 9],
                "Unknown": [19, 3, 5, 1, 1, 1],
            }
        ),
        "SFDC lead reached · sales segment",
    )
)
display(
    _brand_table(
        pd.DataFrame(
            {
                "status": ["Suspect", "New", "Working", "Qualified", "Nurturing", "Unqualified"],
                "DACH": [270, 186, 179, 102, 13, 14],
                "North EMEA": [43, 38, 23, 21, 4, 1],
                "South EMEA": [54, 13, 14, 14, 5, 0],
                "US": [36, 15, 29, 25, 2, 0],
                "Other": [283, 62, 24, 15, 6, 4],
            }
        ),
        "SFDC lead reached · region",
    )
)
try:
    live = sfdc_lead_reached
    if "ENT" in live.columns:
        display(
            _brand_table(
                live[
                    [
                        "sfdc_status",
                        "people_ever_reached",
                        "as_lead",
                        "as_contact",
                        "ENT",
                        "MM",
                        "SMB",
                        "DACH",
                        "North_EMEA",
                        "South_EMEA",
                        "US",
                        "Other",
                    ]
                ],
                "APP: SFDC lead reached",
            )
        )
except Exception:
    pass

labels = [f"{r[0]} · {int(r[3]):,}" for r in rows]
fig = go.Figure()
fig.add_bar(
    name="Lead",
    y=labels,
    x=[int(r[1]) for r in rows],
    orientation="h",
    marker=dict(color=PINK, line=dict(width=0)),
    text=[f"{int(r[1]):,}" for r in rows],
    textposition="outside",
    textfont={"size": 12, "color": INK},
    cliponaxis=False,
    hoverinfo="skip",
    width=0.36,
)
fig.add_bar(
    name="Contact",
    y=labels,
    x=[int(r[2]) for r in rows],
    orientation="h",
    marker=dict(color=PINK_DEEP, line=dict(width=0)),
    text=[f"{int(r[2]):,}" for r in rows],
    textposition="outside",
    textfont={"size": 12, "color": INK},
    cliponaxis=False,
    hoverinfo="skip",
    width=0.36,
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
    height=400,
    margin=dict(t=64, b=28, l=140, r=64),
    title=dict(text="APP: SFDC lead reached · Lead and Contact", font=dict(size=16, color=INK)),
    barmode="group",
    bargap=0.28,
    bargroupgap=0.08,
    legend=dict(orientation="h", y=1.1, bgcolor="rgba(0,0,0,0)"),
    xaxis=dict(
        showgrid=True,
        gridcolor="rgba(156,163,175,0.18)",
        zeroline=False,
        color=INK,
        title="People ever reached",
    ),
    yaxis=dict(autorange="reversed", showgrid=False, zeroline=False, ticks="", tickfont=dict(size=13, color=INK)),
)
display(fig)
