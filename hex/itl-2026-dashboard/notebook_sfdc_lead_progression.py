# SFDC lead progression chart. Live from lead_progression_table when that SQL has run.
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

CORAL = "#FF6D5A"
INK = "#9CA3AF"
rows = [
    ("ITL Free+Paid", 1102, 100.0),
    ("New — handed to sales", 314, 28.5),
    ("Working", 269, 24.4),
    ("Qualified", 177, 16.1),
]
try:
    rows = [
        (str(r["sfdc_status"]), int(r["people"]), float(r["pct_of_itl"]))
        for _, r in lead_progression_table.iterrows()
    ]
except Exception:
    pass

fig = go.Figure(
    go.Funnel(
        y=[s for s, _, _ in rows],
        x=[c for _, c, _ in rows],
        text=[f"{c:,} ({p}%)" for _, c, p in rows],
        textinfo="text",
        textfont={"size": 13, "color": "#F9FAFB"},
        marker=dict(color=[CORAL, "#FF8F80", "#E08A7A", "#6B7280"], line=dict(width=0)),
        connector=dict(line=dict(color="rgba(156,163,175,0.35)", dash="dot", width=2)),
    )
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
    height=360,
    margin=dict(t=56, b=20, l=200, r=40),
    title=dict(text="Lead progression · Salesforce status · ITL Free+Paid", font=dict(size=16, color=INK)),
)
display(fig)
display(pd.DataFrame({"sfdc_status": [s for s, _, _ in rows], "people": [c for _, c, _ in rows], "pct_of_itl": [p for _, _, p in rows]}))
