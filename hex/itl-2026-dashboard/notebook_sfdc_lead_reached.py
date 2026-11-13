# SFDC lead reached. Live from sfdc_lead_reached when that SQL has run.
# Includes Leads (Lead.Status / LeadHistory) and Contacts (Status__c / ContactHistory).
# Grouped, not stacked: the same person can appear in both bars after conversion.
import plotly.graph_objects as go
from IPython.display import display

PINK = "#FF91AC"
PINK_DEEP = "#87003C"
INK = "#9CA3AF"
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

fig = go.Figure()
fig.add_bar(
    name="Lead",
    y=[r[0] for r in rows],
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
    y=[r[0] for r in rows],
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
    height=380,
    margin=dict(t=56, b=28, l=110, r=64),
    title=dict(text="SFDC lead reached · Lead and Contact · ITL Free+Paid", font=dict(size=16, color=INK)),
    barmode="group",
    bargap=0.28,
    bargroupgap=0.08,
    legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"),
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
