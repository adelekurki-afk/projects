import plotly.graph_objects as go
from IPython.display import display, HTML

ITL_WEEK = "2026-10-12"


def _itl_int(value, default=0):
    try:
        if value is None:
            return default
        return int(value)
    except Exception:
        return default


def _week(val):
    return str(val)[:10]


def _line(df, y_cols, title, y_title):
    fig = go.Figure()
    colors = {"n8n_users": "#6B7280", "europe_users": "#4F7FB8", "germany_users": "#FF6D5A",
              "views_gained": "#FF6D5A", "videos_published": "#4F7FB8", "n8n_videos_published": "#111827"}
    names = {"n8n_users": "Worldwide", "europe_users": "Europe", "germany_users": "Germany",
             "views_gained": "Views gained", "videos_published": "Videos published",
             "n8n_videos_published": "n8n-related published"}
    x = [_week(v) for v in df["week_start"]]
    for col in y_cols:
        if col not in df.columns:
            continue
        y = [0 if v != v else float(v) for v in df[col].tolist()]
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name=names.get(col, col),
                line=dict(color=colors.get(col, "#111827"), width=2),
            )
        )
    fig.add_vrect(
        x0="2026-10-12",
        x1="2026-10-18",
        fillcolor="#FF6D5A",
        opacity=0.15,
        line_width=0,
        annotation_text="ITL week",
        annotation_position="top left",
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        height=340,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=60, b=40, l=50, r=20),
        font=dict(family="Inter, Arial, sans-serif", color="#333"),
        legend=dict(orientation="h", y=1.08),
        yaxis=dict(title=y_title, showgrid=True, gridcolor="#F0F0F0"),
        xaxis=dict(showgrid=False),
    )
    return fig


display(HTML(
    '<div style="font-family:Inter,Arial,sans-serif">'
    '<div style="font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#FF6D5A">In the Loop 2026</div>'
    '<h1 style="font-size:26px;margin:4px 0 8px 0">Intent</h1>'
    '<p style="color:#6B7280;font-size:14px">Longer-term demand. Coral band is conference week 12–18 Oct.</p>'
    '</div>'
))

try:
    w = intent_weekly.copy()
    w = w[w["week_start"].astype(str) < "2026-11-09"]
    display(_line(w, ["n8n_users"], "n8n.io users · worldwide", "Users"))
    display(_line(w, ["europe_users", "germany_users"], "n8n.io users · Europe and Germany", "Users"))
except Exception:
    display(HTML("<p>Run intent_weekly, then Run all.</p>"))

try:
    y = intent_youtube.copy()
    display(_line(y, ["views_gained"], "YouTube views gained", "Views"))
    display(_line(y, ["videos_published", "n8n_videos_published"], "YouTube videos published", "Videos"))
except Exception:
    display(HTML("<p>Run intent_youtube, then Run all. Views are reliable from July 2026.</p>"))

try:
    inst = intent_instances.copy()
    fig = go.Figure()
    palette = ["#FF6D5A", "#4F7FB8", "#111827", "#94A3B8", "#F59E0B", "#10B981"]
    types = list(inst["deployment_type"].dropna().unique())
    for i, dtype in enumerate(sorted(types)):
        part = inst[inst["deployment_type"] == dtype].sort_values("week_start")
        fig.add_trace(
            go.Scatter(
                x=[_week(v) for v in part["week_start"]],
                y=part["acquired_instances"],
                mode="lines",
                name=str(dtype),
                line=dict(color=palette[i % len(palette)], width=2),
            )
        )
    fig.add_vrect(x0="2026-10-12", x1="2026-10-18", fillcolor="#FF6D5A", opacity=0.15, line_width=0,
                  annotation_text="ITL week", annotation_position="top left")
    fig.update_layout(
        title=dict(text="Acquired instances by type", font=dict(size=18)),
        height=360,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=60, b=40, l=50, r=20),
        font=dict(family="Inter, Arial, sans-serif", color="#333"),
        legend=dict(orientation="h", y=1.08),
        yaxis=dict(title="Instances", showgrid=True, gridcolor="#F0F0F0"),
    )
    display(fig)
except Exception:
    display(HTML("<p>Run intent_instances, then Run all.</p>"))

try:
    rows = []
    for _, r in intent_paid_keywords.head(15).iterrows():
        rows.append(
            "<tr>"
            f"<td>{r['search_term']}</td>"
            f'<td style="text-align:right">{_itl_int(r["impressions"]):,}</td>'
            f'<td style="text-align:right">{_itl_int(r["clicks"]):,}</td>'
            f'<td style="text-align:right">{float(r["cost"]):.0f}</td>'
            "</tr>"
        )
    display(HTML(
        '<h3 style="font-family:Inter,Arial,sans-serif;font-size:16px">Paid Google Ads terms · 12–18 Oct</h3>'
        '<p style="font-family:Inter,Arial,sans-serif;color:#6B7280;font-size:13px">'
        "Organic SEO / AEO is not in this warehouse (no Search Console). Paid search terms are the closest signal."
        "</p>"
        '<table style="width:100%;border-collapse:collapse;font:13px Inter,Arial,sans-serif">'
        '<tr><th style="text-align:left;border-bottom:1px solid #E5E7EB;padding:6px 8px">Term</th>'
        '<th style="text-align:right;border-bottom:1px solid #E5E7EB;padding:6px 8px">Impr.</th>'
        '<th style="text-align:right;border-bottom:1px solid #E5E7EB;padding:6px 8px">Clicks</th>'
        '<th style="text-align:right;border-bottom:1px solid #E5E7EB;padding:6px 8px">Cost</th></tr>'
        + "".join(rows)
        + "</table>"
    ))
except Exception:
    display(HTML("<p>Run intent_paid_keywords, then Run all.</p>"))

display(HTML(
    '<div style="margin-top:18px;padding:12px 14px;background:#F9FAFB;border:1px solid #E5E7EB;border-radius:8px;'
    'font-family:Inter,Arial,sans-serif;font-size:13px;color:#6B7280">'
    "<b>Social posts.</b> No Common Room table exists in this warehouse. "
    "Cannot show conference-week social posts until that source is connected."
    "</div>"
))
