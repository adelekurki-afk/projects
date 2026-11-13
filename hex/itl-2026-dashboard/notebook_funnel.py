import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

CORAL = "#FF6D5A"
BLUE = "#5B8FC7"
INK = "#9CA3AF"


def _theme(fig, height=320, **kw):
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
        height=height,
        margin=dict(t=56, b=28, l=12, r=20),
        legend=dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)"),
    )
    layout.update(kw)
    fig.update_layout(**layout)
    fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
    return fig


def _euro(n):
    try:
        n = float(n)
    except Exception:
        n = 0
    if abs(n) >= 1_000_000:
        return f"€{n / 1_000_000:.2f}M"
    if abs(n) >= 10_000:
        return f"€{n / 1_000:.0f}k"
    return f"€{int(round(n)):,}"


STAGE_COLORS = [CORAL, "#FF8F80", "#E08A7A", "#6B7280"]


def _centered_funnel(rows, title, height=340):
    max_c = max(int(r[1]) for r in rows) or 1
    fig = go.Figure()
    for i, r in enumerate(rows):
        label = str(r[0])
        count = int(r[1])
        pct = float(r[2]) if len(r) > 2 else round(100.0 * count / max_c, 1)
        fig.add_bar(
            y=[label],
            x=[count],
            base=(max_c - count) / 2.0,
            orientation="h",
            marker=dict(color=STAGE_COLORS[i % len(STAGE_COLORS)], line=dict(width=0)),
            text=[f"{count:,}  ({pct}%)"],
            textposition="inside",
            insidetextanchor="middle",
            textfont={"size": 14, "color": "#111827" if i < 3 else "#F9FAFB"},
            hoverinfo="skip",
            showlegend=False,
            width=0.68,
        )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
        height=height,
        margin=dict(t=52, b=8, l=190, r=16),
        title=dict(text=title, font=dict(size=16, color=INK)),
        bargap=0.32,
        xaxis=dict(visible=False, range=[0, max_c * 1.02], showgrid=False, zeroline=False),
        yaxis=dict(autorange="reversed", showgrid=False, zeroline=False, ticks="", tickfont=dict(size=13, color=INK)),
    )
    return fig


funnel_rows = [
    ("Registered", 1119, 100.0),
    ("Attended (Eco Day or Partner Day)", 837, 74.8),
    ("Had n8n Meeting", 20, 1.8),
    ("Account with Opp (NB/Exp, >= Oct 12)", 70, 6.3),
    ("Closed Won", 6, 0.5),
]
try:
    funnel_rows = [
        (str(r["stage"]), int(r["count"]), float(r["pct_of_registered"]))
        for _, r in lead_funnel.iterrows()
    ]
except Exception:
    pass

sdr_rows = [("Not set", 25, 1851340), ("Human SDR", 4, 166000), ("Web", 1, 26000)]
try:
    sdr_rows = [
        (str(r["sdr_path"]), int(r["opp_count"]), float(r["amount"]))
        for _, r in itl_funnel_sdr.iterrows()
    ]
except Exception:
    pass

stage_rows = [
    ("Sourced", "Value Workshop", 6),
    ("Sourced", "Meeting Booked", 4),
    ("Sourced", "Stakeholder Alignment", 1),
    ("Sourced", "Closed Won Approved", 1),
    ("Influenced", "Meeting Booked", 7),
    ("Influenced", "Value Workshop", 6),
    ("Influenced", "Stakeholder Alignment", 2),
    ("Influenced", "Closed Won Approved", 2),
    ("Influenced", "Discovery", 1),
]
try:
    stage_rows = [
        (
            "Influenced" if str(r["bucket"]).startswith("Influenced") else str(r["bucket"]),
            str(r["stage"]),
            int(r["opp_count"]),
        )
        for _, r in funnel_stages.iterrows()
        if str(r["bucket"]) != "Renewal touched"
    ]
except Exception:
    pass

sourced = [
    ("Kongsberg Satellite Services AS", "Expansion", "Value Workshop", 215000, "MM"),
    ("Boston Consulting Group, Inc.", "Expansion", "Value Workshop", 200000, "ENT"),
    ("TeamViewer GmbH", "New Business", "Value Workshop", 196700, "MM"),
    ("N3 Engine Overhaul Services", "New Business", "Value Workshop", 113900, "MM"),
    ("Eleven Labs Inc.", "Expansion", "Value Workshop", 80000, "MM"),
    ("Trade Republic", "Expansion", "Value Workshop", 60000, "MM"),
    ("Retail Logistics Excellence - Relex Oy", "Expansion", "Stakeholder Alignment", 56000, "MM"),
    ("Next PLC", "Expansion", "Meeting Booked", 55000, "ENT"),
    ("SEFE", "New Business", "Meeting Booked", 28000, "MM"),
    ("RENOLIT SE", "New Business", "Closed Won Approved", 6400, "Unknown"),
    ("ECTIVE Automation", "New Business", "Meeting Booked", 0, "SMB"),
    ("Moonspring AI", "New Business", "Meeting Booked", 0, "SMB"),
]
influenced = [
    ("NVIDIA", "New Business", "Meeting Booked", 700000, "ENT"),
    ("Solaris SE", "New Business", "Stakeholder Alignment", 86000, "MM"),
    ("Rohde & Schwarz GmbH & Co. KG", "New Business", "Meeting Booked", 55000, "ENT"),
    ("Volkswagen AG", "New Business", "Meeting Booked", 55000, "ENT"),
    ("STX Next S.A.", "New Business", "Meeting Booked", 28000, "MM"),
    ("EngageTech", "New Business", "Meeting Booked", 28000, "MM"),
    ("Graphwise", "Expansion", "Stakeholder Alignment", 26701, "MM"),
    ("C Digital Technologies Limited", "New Business", "Value Workshop", 26000, "MM"),
    ("voize", "New Business", "Value Workshop", 26000, "MM"),
    ("HiSolutions AG", "New Business", "Value Workshop", 26000, "MM"),
    ("Cornelsen", "New Business", "Value Workshop", 26000, "MM"),
    ("Apaleo", "New Business", "Closed Won Approved", 22000, "MM"),
    ("Blue Light Card", "Expansion", "Value Workshop", 20000, "MM"),
    ("Deutsche Telekom MMS GmbH", "New Business", "Discovery", 16000, "ENT"),
    ("Moss", "New Business", "Value Workshop", 15000, "MM"),
    ("Delivery Hero", "Expansion", "Meeting Booked", 11150, "ENT"),
    ("Globalization Partners LLC", "Expansion", "Closed Won Approved", 3640, "MM"),
    ("Rakuten", "New Business", "Meeting Booked", 0, "ENT"),
]
won = [row for row in sourced + influenced if row[2].startswith("Closed Won")]
try:
    src_df = itl_sourced_influenced_opps
    sourced = [
        (str(r["account_name"]), str(r["opp_type"]), str(r["StageName"]), float(r["amount"]), str(r["segment"]))
        for _, r in src_df[src_df["attribution"] == "Sourced"].iterrows()
    ]
    inf_mask = src_df["attribution"].astype(str).str.startswith("Influenced")
    influenced = [
        (str(r["account_name"]), str(r["opp_type"]), str(r["StageName"]), float(r["amount"]), str(r["segment"]))
        for _, r in src_df[inf_mask].iterrows()
    ]
    won = [
        (str(r["account_name"]), str(r["opp_type"]), str(r["StageName"]), float(r["amount"]), str(r["segment"]))
        for _, r in src_df[src_df["status"] == "Closed won"].iterrows()
        if not str(r["attribution"]).startswith("Renewal")
    ]
except Exception:
    pass

src_n, src_amt, src_won_n, src_won = 12, 1011000, 1, 6400
inf_n, inf_amt, inf_won_n, inf_won = 18, 1170491, 2, 25640
try:
    for _, r in itl_attribution_kpis.iterrows():
        bucket = str(r["bucket"])
        if bucket == "Sourced":
            src_n, src_amt, src_won_n, src_won = int(r["opp_count"]), float(r["amount"]), int(r["won_count"]), float(r["won_amount"])
        elif bucket == "Influenced":
            inf_n, inf_amt, inf_won_n, inf_won = int(r["opp_count"]), float(r["amount"]), int(r["won_count"]), float(r["won_amount"])
except Exception:
    pass

pipe_total, pipe_open, pipe_won, pipe_opps, pipe_won_n = 2461063, 2427423, 33640, 29, 3
try:
    pipe_total = int(round(float(pipeline_arr["total_amount"].sum())))
    pipe_open = int(round(float(pipeline_arr["open_pipeline_amount"].sum())))
    pipe_won = int(round(float(pipeline_arr["closed_won_amount"].sum())))
    pipe_opps = int(pipeline_arr["opp_count"].sum())
    pipe_won_n = int(pipeline_arr["closed_won_count"].sum())
except Exception:
    pass

sfdc_rows = [
    ("ITL Free+Paid", 1102, 100.0),
    ("New — handed to sales", 314, 28.5),
    ("Working", 269, 24.4),
    ("Qualified", 177, 16.1),
]
try:
    sfdc_rows = [
        (str(r["sfdc_status"]), int(r["people"]), float(r["pct_of_itl"]))
        for _, r in lead_progression_table.iterrows()
    ]
except Exception:
    pass

display(_centered_funnel(sfdc_rows, "Lead progression · Salesforce status · ITL Free+Paid", 340))

stages = [s for s, _, _ in funnel_rows]
counts = [c for _, c, _ in funnel_rows]
pcts = [p for _, _, p in funnel_rows]
funnel_fig = go.Figure(
    go.Funnel(
        y=stages,
        x=counts,
        text=[f"{c:,} ({p}%)" for c, p in zip(counts, pcts)],
        textinfo="text",
        textfont={"size": 13, "color": "#F9FAFB"},
        marker=dict(color=[CORAL, "#FF8F80", "#E08A7A", "#C97B6E", "#6B7280"], line=dict(width=0)),
        connector=dict(line=dict(color="rgba(156,163,175,0.35)", dash="dot", width=2)),
    )
)
display(
    _theme(
        funnel_fig,
        height=400,
        title=dict(text="Event people · CampaignMember attendance", font=dict(size=16, color=INK)),
        margin=dict(t=56, b=20, l=220, r=40),
    )
)

sdr_fig = go.Figure(
    go.Bar(
        x=[n for n, _, _ in sdr_rows],
        y=[c for _, c, _ in sdr_rows],
        marker_color=CORAL,
        text=[c for _, c, _ in sdr_rows],
        textposition="outside",
        textfont={"color": INK},
        cliponaxis=False,
    )
)
display(
    _theme(
        sdr_fig,
        height=280,
        title=dict(text="First meeting source · sourced + influenced", font=dict(size=16, color=INK)),
        yaxis_title="Opportunities",
    )
)

stage_order = []
for _, stage, _ in stage_rows:
    if stage not in stage_order:
        stage_order.append(stage)
stage_fig = go.Figure()
for bucket, color in (("Sourced", CORAL), ("Influenced", BLUE)):
    x = [sum(n for b, s, n in stage_rows if b == bucket and s == stage) for stage in stage_order]
    stage_fig.add_bar(
        name=bucket,
        y=list(reversed(stage_order)),
        x=list(reversed(x)),
        orientation="h",
        marker_color=color,
    )
display(
    _theme(
        stage_fig,
        height=320,
        barmode="stack",
        title=dict(text="Opportunities per Salesforce stage", font=dict(size=16, color=INK)),
        xaxis_title="Opps",
    )
)


def _opp_df(rows):
    return pd.DataFrame(
        {
            "account": [r[0] for r in rows],
            "type": [r[1] for r in rows],
            "stage": [r[2] for r in rows],
            "amount": [_euro(r[3]) for r in rows],
            "segment": [r[4] for r in rows],
        }
    )


kpis = pd.DataFrame(
    {
        "bucket": ["Sourced", "Influenced", "NB + Expansion pipeline"],
        "opps": [src_n, inf_n, pipe_opps],
        "amount": [_euro(src_amt), _euro(inf_amt), _euro(pipe_total)],
        "won": [f"{src_won_n} · {_euro(src_won)}", f"{inf_won_n} · {_euro(inf_won)}", f"{pipe_won_n} · {_euro(pipe_won)}"],
    }
)
display(kpis)
display(_opp_df(sourced))
display(_opp_df(influenced))
display(_opp_df(won))
