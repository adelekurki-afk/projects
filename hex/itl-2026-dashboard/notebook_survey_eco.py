# APP: Ecosystem Day survey — Fillout, 13 Nov 2026 Europe/Madrid
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

CORAL = "#FF6D5A"
BLUE = "#5B8FC7"
INK = "#9CA3AF"


def _theme(fig, height=300, axes=True, **kw):
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
        height=height,
        margin=dict(t=52, b=28, l=8, r=20),
        legend=dict(orientation="h", y=1.14, bgcolor="rgba(0,0,0,0)"),
    )
    layout.update(kw)
    fig.update_layout(**layout)
    if axes:
        fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
        fig.update_yaxes(showgrid=False, zeroline=False, color=INK)
    return fig


kpis = go.Figure()
for i, (value, title, color, fmt) in enumerate(
    (
        (43, "Responses", CORAL, ","),
        (9.1, "Recommend /10", CORAL, ".1f"),
        (72, "NPS", BLUE, ","),
        (35, "Clearer picture 4–5", INK, ","),
    )
):
    kpis.add_trace(
        go.Indicator(
            mode="number",
            value=value,
            number={"font": {"size": 36, "color": color}, "valueformat": fmt},
            title={"text": title, "font": {"size": 13, "color": INK}},
            domain={"x": [i * 0.25, i * 0.25 + 0.24], "y": [0, 1]},
        )
    )
display(_theme(kpis, height=160, axes=False))

rec = go.Figure(
    go.Bar(
        x=[3, 6, 7, 8, 9, 10],
        y=[1, 1, 3, 5, 9, 24],
        marker_color=CORAL,
        text=[1, 1, 3, 5, 9, 24],
        textposition="outside",
        textfont={"color": INK},
        cliponaxis=False,
    )
)
display(
    _theme(
        rec,
        height=280,
        title=dict(text="Recommend attending In The Loop (0–10) · n=43", font=dict(size=16, color=INK)),
        yaxis_title="Responses",
        xaxis=dict(dtick=1),
    )
)

parts = pd.DataFrame(
    {
        "part": [
            "Opening keynote",
            "Talks and panels",
            "Lightning talks",
            "Feature Kitchens",
            "Community Lounge",
            "Market floor",
            "Networking time",
            "After-party",
        ],
        "mean_5": [3.97, 3.98, 3.59, 4.12, 3.92, 3.84, 4.00, 4.10],
        "n_rated": [38, 41, 27, 25, 26, 38, 39, 30],
        "top2_pct": [76.3, 78.0, 55.6, 76.0, 69.2, 63.2, 66.7, 73.3],
        "excellent": [9, 10, 3, 10, 9, 12, 14, 13],
        "very_good": [20, 22, 12, 9, 9, 12, 12, 9],
        "good": [8, 7, 10, 5, 6, 11, 12, 6],
        "fair": [1, 2, 2, 1, 1, 2, 1, 2],
        "poor": [0, 0, 0, 0, 1, 1, 0, 0],
        "did_not_attend": [5, 2, 16, 18, 17, 5, 4, 13],
    }
)
display(parts)

ops = pd.DataFrame(
    {
        "item": [
            "Registration and check-in",
            "Venue (Wilhelm Studios)",
            "Food and drinks",
            "Finding your way around",
            "Pre-event communication",
            "Audio/visual and room comfort",
        ],
        "mean_5": [4.53, 4.28, 4.35, 3.58, 3.95, 4.14],
        "n_rated": [43, 43, 43, 43, 42, 43],
        "top2_pct": [93.0, 79.1, 90.7, 53.5, 71.4, 76.7],
        "excellent": [30, 23, 22, 12, 15, 20],
        "very_good": [10, 11, 17, 11, 15, 13],
        "good": [1, 8, 2, 13, 8, 7],
        "fair": [0, 0, 1, 4, 3, 2],
        "poor": [2, 1, 1, 3, 1, 1],
    }
)
display(ops)

display(
    pd.DataFrame(
        {
            "question": [
                "Days attended",
                "Days attended",
                "Technical level",
                "Technical level",
                "Technical level",
                "Technical level",
                "Technical level",
            ],
            "answer": [
                "Ecosystem Day only",
                "Partner + Ecosystem Day",
                "About right",
                "A bit too basic",
                "Much too basic",
                "A bit too advanced",
                "Much too advanced",
            ],
            "n": [31, 11, 25, 13, 2, 1, 1],
        }
    )
)

display(
    pd.DataFrame(
        {
            "role": [
                "Developer or engineer",
                "Founder, freelancer or agency",
                "IT, platform or security",
                "Business leader or decision-maker",
                "Automation or ops lead",
                "Consultant or implementation partner",
                "Community contributor or ambassador",
                "Other",
            ],
            "n": [10, 7, 6, 6, 5, 4, 2, 2],
        }
    )
)

display(
    pd.DataFrame(
        {
            "n8n_today": [
                "Self-hosted Community Edition",
                "Enterprise (self-hosted or cloud)",
                "n8n Cloud",
                "Evaluating",
                "Not yet using",
            ],
            "n": [14, 12, 10, 3, 3],
        }
    )
)

display(
    pd.DataFrame(
        {
            "more_next_year": [
                "Business value and ROI",
                "Deep dives on n8n features and roadmap",
                "Running n8n at scale",
                "Practical workshops and build-alongs",
                "Building agents for production",
                "Customer case studies",
                "Community and open-mic formats",
                "Partner and integration showcases",
            ],
            "n": [21, 21, 19, 19, 19, 16, 6, 5],
        }
    )
)

display(
    pd.DataFrame(
        {
            "try_next_3_months": [
                "n8n Agents",
                "n8n Assistant",
                "Agentic Context Layer",
                "New execution engine",
                "New integrations and nodes",
                "Credential management",
                "Development lifecycle",
                "None of these yet",
            ],
            "n": [32, 22, 19, 14, 11, 9, 9, 1],
        }
    )
)
