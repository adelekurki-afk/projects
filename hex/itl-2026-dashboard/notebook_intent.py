# Intent · 12–18 Oct conference week · YouTube · Common Room · Paid Google Ads
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

CORAL = "#FF6D5A"
BLUE = "#5B8FC7"
INK = "#9CA3AF"

# Snapshot 13 Nov 2026 Europe/Madrid — baked so the App cell can run before the SQL cells.
_WEEKLY = pd.DataFrame(
    [
        ("2026-06-01", 212181, 58482, 12606),
        ("2026-06-08", 211254, 58645, 13511),
        ("2026-06-15", 197717, 54521, 12537),
        ("2026-06-22", 191155, 49089, 11727),
        ("2026-06-29", 185104, 49949, 12415),
        ("2026-07-06", 189926, 49332, 12054),
        ("2026-07-13", 188846, 47744, 12043),
        ("2026-07-20", 194738, 48513, 12136),
        ("2026-07-27", 236602, 56956, 13618),
        ("2026-08-03", 262172, 61565, 14579),
        ("2026-08-10", 249628, 57532, 11964),
        ("2026-08-17", 246108, 54330, 11695),
        ("2026-08-24", 248937, 60938, 12353),
        ("2026-08-31", 234251, 57310, 11403),
        ("2026-09-07", 183289, 45908, 9592),
        ("2026-09-14", 176849, 45743, 9928),
        ("2026-09-21", 171052, 43775, 9520),
        ("2026-09-28", 168643, 44217, 9699),
        ("2026-10-05", 173571, 45211, 9934),
        ("2026-10-12", 174802, 45978, 10563),
        ("2026-10-19", 186284, 47289, 10207),
        ("2026-10-26", 176581, 43195, 9029),
        ("2026-11-02", 163038, 40449, 8481),
    ],
    columns=["week_start", "n8n_users", "europe_users", "germany_users"],
)
_YOUTUBE = pd.DataFrame(
    [
        ("2026-07-06", 3248654),
        ("2026-07-13", 2866279),
        ("2026-07-20", 2934305),
        ("2026-07-27", 2757976),
        ("2026-08-03", 2793957),
        ("2026-08-10", 2906293),
        ("2026-08-17", 2599058),
        ("2026-08-24", 3207865),
        ("2026-08-31", 4148747),
        ("2026-09-07", 3928055),
        ("2026-09-14", 3822707),
        ("2026-09-21", 3743902),
        ("2026-09-28", 3595988),
        ("2026-10-05", 3611676),
        ("2026-10-12", 3424076),
        ("2026-10-19", 3189414),
        ("2026-10-26", 2983691),
        ("2026-11-02", 2820043),
    ],
    columns=["week_start", "views_gained"],
)
_PAID = pd.DataFrame(
    [
        ("n8n", 56162, 24376, 16650.13),
        ("ai", 9751, 434, 1161.03),
        ("claude ai", 2753, 186, 920.24),
        ("best business ai", 2336, 1283, 1485.32),
        ("best ai for business", 1381, 735, 647.39),
        ("n8n ai", 1369, 650, 608.77),
        ("n8n login", 1247, 627, 295.09),
        ("n8n workflows", 1109, 468, 621.32),
        ("ai platforms", 980, 526, 475.23),
        ("ai for work", 969, 496, 376.33),
        ("n8n pricing", 855, 538, 648.79),
        ("ai for businesses", 805, 423, 375.67),
        ("what is n8n", 757, 52, 58.45),
        ("n8n cloud", 556, 265, 359.89),
        ("n8n automation", 395, 118, 93.84),
    ],
    columns=["term", "impressions", "clicks", "cost"],
)


def _week(val):
    return str(val)[:10]


def _theme(fig, height=320, **kw):
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
        height=height,
        margin=dict(t=56, b=36, l=48, r=16),
        legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"),
    )
    layout.update(kw)
    fig.update_layout(**layout)
    fig.update_xaxes(showgrid=False, color=INK)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
    return fig


def _line(df, y_cols, title, y_title):
    fig = go.Figure()
    x = [_week(v) for v in df["week_start"]]
    for col, color, name in y_cols:
        if col not in df.columns:
            continue
        y = [0 if v != v else float(v) for v in df[col].tolist()]
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=name, line=dict(color=color, width=2)))
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


weekly = _WEEKLY.copy()
try:
    w = intent_weekly.copy()
    w["week_start"] = w["week_start"].map(_week)
    w = w[w["week_start"] < "2026-11-09"]
    if not w.empty:
        weekly = w
except Exception:
    pass

youtube = _YOUTUBE.copy()
try:
    y = intent_youtube.copy()
    y["week_start"] = y["week_start"].map(_week)
    if not y.empty:
        youtube = y
except Exception:
    pass

paid = _PAID.copy()
try:
    p = intent_paid_keywords.head(15).copy()
    p = p.rename(columns={"search_term": "term"})
    keep = [c for c in ("term", "impressions", "clicks", "cost") if c in p.columns]
    if keep:
        paid = p[keep]
except Exception:
    pass

display(
    _line(
        weekly,
        [("n8n_users", "#9CA3AF", "Worldwide")],
        "n8n.io users · worldwide",
        "Users",
    )
)
display(
    _line(
        weekly,
        [("europe_users", BLUE, "Europe"), ("germany_users", CORAL, "Germany")],
        "n8n.io users · Europe and Germany",
        "Users",
    )
)
display(
    _line(
        youtube,
        [("views_gained", CORAL, "Views gained")],
        "YouTube views gained",
        "Views",
    )
)
display(paid)
display(
    pd.DataFrame(
        {
            "gap": ["Social posts"],
            "status": [
                "No Common Room table exists in this warehouse. Cannot show conference-week social posts until that source is connected."
            ],
        }
    )
)
