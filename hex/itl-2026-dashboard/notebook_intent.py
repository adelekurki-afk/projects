# Intent · 12–18 Oct conference week · YouTube · Common Room · Paid Google Ads
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

CORAL = "#FF6D5A"
BLUE = "#5B8FC7"
INK = "#9CA3AF"
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


def _theme(fig, height=340, **kw):
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
        height=height,
        margin=dict(t=60, b=40, l=50, r=20),
        legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"),
    )
    layout.update(kw)
    fig.update_layout(**layout)
    fig.update_xaxes(showgrid=False, color=INK)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
    return fig


def _line(df, y_cols, title, y_title):
    fig = go.Figure()
    colors = {
        "n8n_users": "#9CA3AF",
        "europe_users": BLUE,
        "germany_users": CORAL,
        "views_gained": CORAL,
        "videos_published": BLUE,
        "n8n_videos_published": "#CBD5E1",
    }
    names = {
        "n8n_users": "Worldwide",
        "europe_users": "Europe",
        "germany_users": "Germany",
        "views_gained": "Views gained",
        "videos_published": "Videos published",
        "n8n_videos_published": "n8n-related published",
    }
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
                line=dict(color=colors.get(col, CORAL), width=2),
            )
        )
    fig.add_vrect(
        x0="2026-10-12",
        x1="2026-10-18",
        fillcolor=CORAL,
        opacity=0.18,
        line_width=0,
        annotation_text="ITL week",
        annotation_position="top left",
        annotation_font=dict(color=INK, size=11),
    )
    return _theme(fig, title=dict(text=title, font=dict(size=16, color=INK)), yaxis_title=y_title)


try:
    w = intent_weekly.copy()
    w = w[w["week_start"].astype(str) < "2026-11-09"]
    display(_line(w, ["n8n_users"], "n8n.io users · worldwide", "Users"))
    display(_line(w, ["europe_users", "germany_users"], "n8n.io users · Europe and Germany", "Users"))
except Exception:
    display(pd.DataFrame({"note": ["Run intent_weekly, then Run all."]}))

try:
    y = intent_youtube.copy()
    display(_line(y, ["views_gained"], "YouTube views gained", "Views"))
    display(_line(y, ["videos_published", "n8n_videos_published"], "YouTube videos published", "Videos"))
except Exception:
    display(pd.DataFrame({"note": ["Run intent_youtube, then Run all. Views are reliable from July 2026."]}))

try:
    inst = intent_instances.copy()
    fig = go.Figure()
    palette = [CORAL, BLUE, "#CBD5E1", "#94A3B8", "#F59E0B", "#10B981"]
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
    fig.add_vrect(
        x0="2026-10-12",
        x1="2026-10-18",
        fillcolor=CORAL,
        opacity=0.18,
        line_width=0,
        annotation_text="ITL week",
        annotation_position="top left",
        annotation_font=dict(color=INK, size=11),
    )
    display(_theme(fig, height=360, title=dict(text="Acquired instances by type", font=dict(size=16, color=INK)), yaxis_title="Instances"))
except Exception:
    display(pd.DataFrame({"note": ["Run intent_instances, then Run all."]}))

try:
    paid = intent_paid_keywords.head(15).copy()
    paid = paid.rename(columns={"search_term": "term"})
    keep = [c for c in ("term", "impressions", "clicks", "cost") if c in paid.columns]
    display(paid[keep] if keep else paid)
except Exception:
    display(pd.DataFrame({"note": ["Run intent_paid_keywords, then Run all. Paid Google Ads terms · 12–18 Oct. Organic SEO / AEO is not in this warehouse."]}))

display(
    pd.DataFrame(
        {
            "gap": ["Social posts"],
            "status": ["No Common Room table exists in this warehouse. Cannot show conference-week social posts until that source is connected."],
        }
    )
)
