import plotly.graph_objects as go
from IPython.display import display, HTML

# Self-contained Salesforce funnel. App runs top-to-bottom; SQL cells later
# in the notebook are not available here. Numbers are from BQ on 13 Nov 2026
# (Europe/Madrid). Run lead_funnel / pipeline_arr / itl_sourced_influenced_opps
# in the notebook to refresh, then replace the baked fallbacks.


def _euro(n):
    try:
        n = float(n)
    except Exception:
        n = 0
    if n >= 1_000_000:
        return f"€{n / 1_000_000:.2f}M"
    if abs(n) >= 10_000:
        return f"€{n / 1_000:.0f}k"
    return f"€{int(round(n)):,}"


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

css = """
.itl-funnel { font-family: Inter, Arial, sans-serif; color:#111827; max-width:1100px; }
.itl-kicker { font-size:12px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:#FF6D5A; margin:0 0 6px 0; }
.itl-title { font-size:26px; font-weight:700; margin:0 0 6px 0; }
.itl-sub { font-size:14px; color:#6B7280; margin:0 0 16px 0; }
.itl-strip { display:grid; grid-template-columns:repeat(4,minmax(140px,1fr)); gap:12px; margin:0 0 16px 0; }
.itl-tile { border:1px solid #E5E7EB; border-radius:10px; background:#fff; padding:16px 18px 14px; }
.itl-val { font-size:28px; font-weight:700; line-height:1.1; font-variant-numeric:tabular-nums; }
.itl-val.accent { color:#FF6D5A; }
.itl-label { margin-top:8px; font-size:13px; color:#6B7280; font-weight:600; }
.itl-hint { margin-top:4px; font-size:11px; color:#9CA3AF; }
.itl-note { margin:12px 0 8px; font-size:13px; color:#6B7280; padding:12px 14px; background:#F9FAFB; border:1px solid #E5E7EB; border-radius:8px; }
"""
header = f"""
<style>{css}</style>
<div class="itl-funnel">
  <div class="itl-kicker">In the Loop 2026 · live from BigQuery</div>
  <h1 class="itl-title">Funnel</h1>
  <p class="itl-sub">Salesforce Free/Paid campaign members, not Fliplet 1,269 / 426 / 916. Snapshot 13 Nov 2026, Europe/Madrid.</p>
  <div class="itl-strip">
    <div class="itl-tile"><div class="itl-val accent">{src_n}</div><div class="itl-label">Sourced opps</div><div class="itl-hint">{_euro(src_amt)} · {src_won_n} won {_euro(src_won)}</div></div>
    <div class="itl-tile"><div class="itl-val">{inf_n}</div><div class="itl-label">Influenced opps</div><div class="itl-hint">{_euro(inf_amt)} · {inf_won_n} won {_euro(inf_won)}</div></div>
    <div class="itl-tile"><div class="itl-val">{_euro(pipe_total)}</div><div class="itl-label">NB + Expansion</div><div class="itl-hint">From 12 Oct · {pipe_opps} opps</div></div>
    <div class="itl-tile"><div class="itl-val">{_euro(pipe_won)}</div><div class="itl-label">Closed won</div><div class="itl-hint">{pipe_won_n} deals on that clock</div></div>
  </div>
  <div class="itl-note">70 people sit on an account with a NB/Expansion opp created from 12 Oct. That is not 70 opportunities. Pipeline below is 29 NB+Expansion deals / {_euro(pipe_open)} open. No Partner-typed opportunities — net new is New Business. AI SDR (Freddy) is not set on these 30 sourced+influenced deals.</div>
</div>
"""
display(HTML(header))

stages = [s for s, _, _ in funnel_rows]
counts = [c for _, c, _ in funnel_rows]
pcts = [p for _, _, p in funnel_rows]
fig = go.Figure(
    go.Funnel(
        y=stages,
        x=counts,
        text=[f"{c:,} ({p}%)" for c, p in zip(counts, pcts)],
        textinfo="text",
        textfont={"size": 14},
        marker=dict(
            color=["#FF6D5A", "#FF8F80", "#FFB3A7", "#FFC8BF", "#2D2D2D"],
            line=dict(width=1, color="white"),
        ),
        connector=dict(line=dict(color="#E0E0E0", dash="dot", width=2)),
    )
)
fig.update_layout(
    title=dict(text="Leads progression · Salesforce CampaignMember", font=dict(size=18)),
    height=420,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin={"t": 60, "b": 20, "l": 260, "r": 60},
    font={"family": "Inter, Arial, sans-serif", "color": "#333"},
)
display(fig)

sdr_fig = go.Figure(
    go.Bar(
        x=[n for n, _, _ in sdr_rows],
        y=[c for _, c, _ in sdr_rows],
        marker_color="#FF6D5A",
        text=[c for _, c, _ in sdr_rows],
        textposition="outside",
    )
)
sdr_fig.update_layout(
    title=dict(text="ITL sourced + influenced · first meeting source", font=dict(size=18)),
    height=320,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(t=60, b=40, l=40, r=20),
    font=dict(family="Inter, Arial, sans-serif", color="#333"),
    yaxis=dict(title="Opportunities", showgrid=True, gridcolor="#F0F0F0"),
)
display(sdr_fig)

stage_order = []
for _, stage, _ in stage_rows:
    if stage not in stage_order:
        stage_order.append(stage)
stage_fig = go.Figure()
for bucket, color in (("Sourced", "#FF6D5A"), ("Influenced", "#4F7FB8")):
    x = [sum(n for b, s, n in stage_rows if b == bucket and s == stage) for stage in stage_order]
    stage_fig.add_bar(name=bucket, y=list(reversed(stage_order)), x=list(reversed(x)), orientation="h", marker_color=color)
stage_fig.update_layout(
    barmode="stack",
    title=dict(text="Opportunities per Salesforce stage", font=dict(size=18)),
    height=360,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(t=60, b=40, l=180, r=20),
    font=dict(family="Inter, Arial, sans-serif", color="#333"),
    legend=dict(orientation="h", y=1.08),
    xaxis=dict(title="Opps", showgrid=True, gridcolor="#F0F0F0"),
)
display(stage_fig)


def _opp_table(rows, title):
    body_rows = []
    for account, opp_type, stage, amount, segment in rows:
        body_rows.append(
            "<tr>"
            f"<td>{account}</td><td>{opp_type}</td><td>{stage}</td>"
            f'<td class="num">{_euro(amount)}</td><td>{segment}</td>'
            "</tr>"
        )
    body = "\n".join(body_rows) if body_rows else "<tr><td colspan='5'>No rows</td></tr>"
    return (
        f'<h3 style="font-family:Inter,Arial,sans-serif;font-size:16px;margin:24px 0 8px 0">{title} · {len(rows)}</h3>'
        '<table style="width:100%;border-collapse:collapse;font:13px Inter,Arial,sans-serif">'
        '<tr><th style="text-align:left;border-bottom:1px solid #E5E7EB;padding:6px 8px">Account</th>'
        '<th style="text-align:left;border-bottom:1px solid #E5E7EB;padding:6px 8px">Type</th>'
        '<th style="text-align:left;border-bottom:1px solid #E5E7EB;padding:6px 8px">Stage</th>'
        '<th style="text-align:right;border-bottom:1px solid #E5E7EB;padding:6px 8px">Amount</th>'
        '<th style="text-align:left;border-bottom:1px solid #E5E7EB;padding:6px 8px">Segment</th></tr>'
        f"{body}</table>"
    )


display(HTML(_opp_table(sourced, "Opportunities sourced")))
display(HTML(_opp_table(influenced, "Opportunities influenced")))
display(HTML(_opp_table(won, "Closed won on this list")))
