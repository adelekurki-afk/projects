# SFDC lead progression chart. Live from lead_progression_table when that SQL has run.
import plotly.graph_objects as go
from IPython.display import display

PINK = "#FF91AC"
PINK_MID = "#FFBCCA"
PINK_LIGHT = "#FFD0D9"
PINK_DEEP = "#87003C"
INK = "#9CA3AF"
STAGE_COLORS = [PINK, PINK_MID, PINK_LIGHT, PINK_DEEP]
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

max_c = max(int(r[1]) for r in rows) or 1
fig = go.Figure()
for i, (label, count, pct) in enumerate(rows):
    fig.add_bar(
        y=[label],
        x=[count],
        base=(max_c - count) / 2.0,
        orientation="h",
        marker=dict(color=STAGE_COLORS[i % len(STAGE_COLORS)], line=dict(width=0)),
        text=[f"{count:,}  ({pct}%)"],
        textposition="inside",
        insidetextanchor="middle",
        textfont={"size": 14, "color": "#191919" if i < 3 else "#F9FAFB"},
        hoverinfo="skip",
        showlegend=False,
        width=0.68,
    )
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
    height=340,
    margin=dict(t=52, b=8, l=190, r=16),
    title=dict(text="Lead progression · Salesforce status · ITL Free+Paid", font=dict(size=16, color=INK)),
    bargap=0.32,
    xaxis=dict(visible=False, range=[0, max_c * 1.02], showgrid=False, zeroline=False),
    yaxis=dict(autorange="reversed", showgrid=False, zeroline=False, ticks="", tickfont=dict(size=13, color=INK)),
)
display(fig)
