# APP: Session feedback — Fliplet in-app, 13 Nov 2026 Europe/Madrid
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
        (66, "Ratings", CORAL, ","),
        (24, "People", BLUE, ","),
        (36, "Sessions", INK, ","),
        (4.8, "Session /5", CORAL, ".1f"),
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

dist = go.Figure(
    go.Bar(
        x=[2, 3, 4, 5],
        y=[1, 2, 4, 55],
        marker_color=CORAL,
        text=[1, 2, 4, 55],
        textposition="outside",
        textfont={"color": INK},
        cliponaxis=False,
    )
)
display(
    _theme(
        dist,
        height=260,
        title=dict(text="Session score (1–5) · n=62", font=dict(size=16, color=INK)),
        yaxis_title="Ratings",
        xaxis=dict(dtick=1),
    )
)

sessions = pd.DataFrame(
    {
        "session": [
            "Low-Pressure Networking for the n8n Community",
            "Building the Future of the Ambassador Program",
            "Building Autonomous Agents for Production",
            "Our Vision for What’s Next",
            "How to Host a Great n8n Event",
            "Inside n8n's Next Chapter",
            "Feature Kitchen: Agentic Context Layer",
            "Feature Kitchen: Credential Management",
            "We Didn’t Build an Agent Factory",
            "One Agent, Too Many Jobs: Rebuilding Nate",
            "Closing Words",
            "How We Got Here and Where We’re Going",
            "Scaling n8n Inside Regulated Enterprises",
            "Agents Need Hands",
            "Building a Self-Healing Research Agent",
        ],
        "n": [6, 6, 5, 5, 4, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1],
        "session_mean": [5.00, 5.00, 5.00, 4.80, 5.00, 5.00, 4.67, 5.00, 5.00, 4.50, 5.00, 5.00, 2.00, 3.00, 3.00],
        "speaker_mean": [5.83, 7.50, 6.40, 5.80, 5.00, 6.67, 6.33, 10.00, 9.00, 7.00, 5.00, 5.00, 2.00, 2.00, 2.00],
    }
)
display(sessions)

singles = pd.DataFrame(
    {
        "session": [
            "Building Communities That Matter",
            "Better Together: Partner Playbook",
            "Feature Kitchen: n8n Agents",
            "Enterprise and Partner Product Roadmap",
            "Building n8n's AI SDR",
            "Choosing the Right Workflows to Maximize ROI",
            "How to Teach n8n to Others",
            "How the Ecosystem Can Work Together",
            "GTM Evolution of n8n",
            "Highly GDPR Restricted Environments",
            "Lessons From the Frontline",
            "Running n8n in Production: Mercedes-Benz",
            "SAP x n8n Partnership",
            "Life Inside n8n Over the Years",
            "Suffering From Success",
            "The Ambassador Journey",
            "The Agent Is Half the System",
            "The Automation Relay",
            "The Fox Challenge",
            "User Insights on Autopilot",
            "Working With n8n: Nodes in Practice",
        ],
        "n": [1] * 21,
        "session_mean": [
            5.0, 4.0, 5.0, None, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0
        ],
    }
)
display(singles)
