import pandas as pd
import plotly.graph_objects as go
from IPython.display import display
from plotly.subplots import make_subplots

PINK = "#FF91AC"
PINK_MID = "#FFBCCA"
PINK_LIGHT = "#FFD0D9"
PINK_DEEP = "#87003C"
CORAL = PINK
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


def _reached_grouped(rows, title):
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
        title=dict(text=title, font=dict(size=16, color=INK)),
        barmode="group",
        bargap=0.28,
        bargroupgap=0.08,
        legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK, title="People ever reached"),
        yaxis=dict(autorange="reversed", showgrid=False, zeroline=False, ticks="", tickfont=dict(size=13, color=INK)),
    )
    return fig


def _dim_table(rows, series_order):
    statuses = [s for s in STATUS_ORDER if any(str(r[0]) == s for r in rows)]
    lookup = {(str(r[0]), str(r[1])): int(r[2]) for r in rows}
    data = {"status": statuses}
    for name in series_order:
        data[name] = [lookup.get((st, name), 0) for st in statuses]
    return pd.DataFrame(data)


def _reached_pair(segment_rows, region_rows):
    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("Sales segment", "Region"),
        vertical_spacing=0.14,
    )
    statuses = [s for s in STATUS_ORDER if any(str(r[0]) == s for r in segment_rows + region_rows)]
    seg_lookup = {(str(r[0]), str(r[1])): int(r[2]) for r in segment_rows}
    reg_lookup = {(str(r[0]), str(r[1])): int(r[2]) for r in region_rows}
    for name in SEGMENT_ORDER:
        xs = [seg_lookup.get((st, name), 0) for st in statuses]
        fig.add_bar(
            name=name,
            y=statuses,
            x=xs,
            orientation="h",
            marker=dict(color=SEGMENT_COLORS.get(name, PINK), line=dict(width=0)),
            text=[f"{v:,}" if v else "" for v in xs],
            textposition="outside",
            cliponaxis=False,
            hoverinfo="skip",
            legendgroup="segment",
            row=1,
            col=1,
        )
    for name in REGION_ORDER:
        xs = [reg_lookup.get((st, name), 0) for st in statuses]
        fig.add_bar(
            name=name,
            y=statuses,
            x=xs,
            orientation="h",
            marker=dict(color=REGION_COLORS.get(name, PINK), line=dict(width=0)),
            text=[f"{v:,}" if v else "" for v in xs],
            textposition="outside",
            cliponaxis=False,
            hoverinfo="skip",
            legendgroup="region",
            row=2,
            col=1,
        )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
        height=760,
        margin=dict(t=72, b=28, l=110, r=56),
        title=dict(text="SFDC lead reached · sales segment and region", font=dict(size=16, color=INK)),
        barmode="group",
        bargap=0.28,
        bargroupgap=0.06,
        legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK, title="People ever reached")
    fig.update_yaxes(autorange="reversed", showgrid=False, zeroline=False, ticks="", tickfont=dict(size=13, color=INK))
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

reached_rows = [
    ("Suspect", 546, 140, 686, 62.3),
    ("New", 302, 18, 314, 28.5),
    ("Working", 71, 206, 269, 24.4),
    ("Qualified", 135, 56, 177, 16.1),
    ("Nurturing", 27, 3, 30, 2.7),
    ("Unqualified", 7, 12, 19, 1.7),
]
try:
    reached_rows = [
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

display(_dim_table(segment_rows, SEGMENT_ORDER))
display(_dim_table(region_rows, REGION_ORDER))
display(_reached_pair(segment_rows, region_rows))
display(_reached_grouped(reached_rows, "SFDC lead reached · Lead and Contact"))

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
        marker=dict(color=[PINK, "#E56B8A", "#87003C", "#5A0026", "#44001B"], line=dict(width=0)),
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
