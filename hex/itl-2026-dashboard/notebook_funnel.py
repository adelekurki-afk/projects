import plotly.graph_objects as go
from IPython.display import display, HTML


def _itl_empty(msg="Run all, then refresh the App."):
    fig = go.Figure()
    fig.add_annotation(text=msg, showarrow=False, font=dict(size=14, color="#6B7280"))
    fig.update_layout(
        height=220,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(t=20, b=20, l=20, r=20),
        font=dict(family="Inter, Arial, sans-serif", color="#333"),
    )
    return fig


def _itl_int(value, default=0):
    try:
        if value is None:
            return default
        return int(value)
    except Exception:
        return default


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


if "lead_funnel" not in globals():
    fig = _itl_empty()
else:
    try:
        stages = lead_funnel["stage"].tolist()
        counts = [int(c) for c in lead_funnel["count"].tolist()]
        pcts = [float(p) for p in lead_funnel["pct_of_registered"].tolist()]
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
            title=dict(text="Leads progression", font=dict(size=18)),
            height=420,
            paper_bgcolor="white",
            plot_bgcolor="white",
            margin={"t": 60, "b": 20, "l": 220, "r": 60},
            font={"family": "Inter, Arial, sans-serif", "color": "#333"},
            yaxis=dict(tickfont=dict(size=13)),
        )
    except Exception as e:
        fig = _itl_empty("Run all first (" + type(e).__name__ + ")")
display(fig)

sdr_fig = _itl_empty("Run funnel_ai_sdr, then Run all.")
try:
    joined = itl_sourced_influenced_opps.merge(funnel_ai_sdr, on="opp_id", how="left")
    joined["sdr_path"] = joined["sdr_path"].fillna("Not set")
    grouped = (
        joined.groupby("sdr_path")
        .agg(opp_count=("opp_id", "count"), amount=("amount", "sum"))
        .reset_index()
        .sort_values("opp_count", ascending=False)
    )
    sdr_fig = go.Figure(
        go.Bar(
            x=grouped["sdr_path"],
            y=grouped["opp_count"],
            marker_color="#FF6D5A",
            text=grouped["opp_count"],
            textposition="outside",
        )
    )
    sdr_fig.update_layout(
        title=dict(text="ITL opps · AI SDR vs humans", font=dict(size=18)),
        height=320,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=60, b=40, l=40, r=20),
        font=dict(family="Inter, Arial, sans-serif", color="#333"),
        yaxis=dict(title="Opportunities", showgrid=True, gridcolor="#F0F0F0"),
        xaxis=dict(title=""),
    )
except Exception:
    pass
display(sdr_fig)

stage_fig = _itl_empty("Run funnel_stages, then Run all.")
try:
    sdf = funnel_stages.copy()
    stages_order = sdf.groupby("stage")["opp_count"].sum().sort_values(ascending=True)
    fig2 = go.Figure()
    for bucket, color in [("Sourced", "#FF6D5A"), ("Influenced", "#4F7FB8"), ("Renewal touched", "#94A3B8")]:
        part = sdf[sdf["bucket"] == bucket]
        y = list(stages_order.index)
        x = [int(part.loc[part["stage"] == s, "opp_count"].sum()) if s in part["stage"].values else 0 for s in y]
        fig2.add_bar(name=bucket, y=y, x=x, orientation="h", marker_color=color)
    fig2.update_layout(
        barmode="stack",
        title=dict(text="Opportunities per stage", font=dict(size=18)),
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=60, b=40, l=180, r=20),
        font=dict(family="Inter, Arial, sans-serif", color="#333"),
        legend=dict(orientation="h", y=1.08),
        xaxis=dict(title="Opps", showgrid=True, gridcolor="#F0F0F0"),
    )
    stage_fig = fig2
except Exception:
    pass
display(stage_fig)


def _opp_table(df, title):
    rows = []
    for _, r in df.head(25).iterrows():
        rows.append(
            "<tr>"
            f"<td>{r.get('account_name', '')}</td>"
            f"<td>{r.get('opp_type', '')}</td>"
            f"<td>{r.get('StageName', '')}</td>"
            f'<td class="num">{_euro(r.get("amount", 0))}</td>'
            f"<td>{r.get('segment', '')}</td>"
            "</tr>"
        )
    body = "\n".join(rows) if rows else "<tr><td colspan='5'>No rows</td></tr>"
    return (
        f'<h3 style="font-family:Inter,Arial,sans-serif;font-size:16px;margin:24px 0 8px 0">{title} · {len(df)}</h3>'
        '<table style="width:100%;border-collapse:collapse;font:13px Inter,Arial,sans-serif">'
        '<tr><th style="text-align:left;border-bottom:1px solid #E5E7EB;padding:6px 8px">Account</th>'
        '<th style="text-align:left;border-bottom:1px solid #E5E7EB;padding:6px 8px">Type</th>'
        '<th style="text-align:left;border-bottom:1px solid #E5E7EB;padding:6px 8px">Stage</th>'
        '<th style="text-align:right;border-bottom:1px solid #E5E7EB;padding:6px 8px">Amount</th>'
        '<th style="text-align:left;border-bottom:1px solid #E5E7EB;padding:6px 8px">Segment</th></tr>'
        f"{body}</table>"
    )


try:
    src = itl_sourced_influenced_opps[itl_sourced_influenced_opps["attribution"] == "Sourced"].copy()
    inf = itl_sourced_influenced_opps[itl_sourced_influenced_opps["attribution"].astype(str).str.startswith("Influenced")].copy()
    won = itl_sourced_influenced_opps[itl_sourced_influenced_opps["status"] == "Closed won"].copy()
    display(HTML(_opp_table(src, "Opportunities sourced")))
    display(HTML(_opp_table(inf, "Opportunities influenced")))
    display(HTML(_opp_table(won, "Closed won on this list")))
except Exception:
    display(HTML("<p>Run itl_sourced_influenced_opps, then Run all.</p>"))
