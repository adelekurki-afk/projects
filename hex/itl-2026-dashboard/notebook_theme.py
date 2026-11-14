"""Plotly layout that stays readable on Hex light and dark app themes."""

CORAL = "#FF6D5A"
SLATE = "#7C8AA5"
INK = "#9CA3AF"


def apply_theme(fig, height=320, **layout):
    base = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
        height=height,
        margin=dict(t=56, b=36, l=16, r=24),
        legend=dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)"),
    )
    base.update(layout)
    fig.update_layout(**base)
    fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
    return fig
