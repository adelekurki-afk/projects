# APP: Chart · Paid search terms — one figure. Classic App only shows the first display().
import plotly.graph_objects as go
from IPython.display import display

PINK = "#FF91AC"
PINK_MID = "#FFBCCA"
PINK_DEEP = "#87003C"
BLUE = "#5B8FC7"
INK = "#9CA3AF"
CORAL = PINK
MUTED = "#94A3B8"
AMBER = "#FDBA74"


def _theme(fig, height=300, axes=True, **kw):
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
        height=height,
        margin=dict(t=52, b=36, l=16, r=24),
        legend=dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)"),
    )
    layout.update(kw)
    fig.update_layout(**layout)
    if axes:
        fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
    return fig


terms = ["n8n", "ai", "claude ai", "best business ai", "best ai for business", "n8n ai", "n8n login", "n8n workflows"]
clicks = [24376, 434, 186, 1283, 735, 650, 627, 468]
fig = go.Figure(go.Bar(y=terms[::-1], x=clicks[::-1], orientation="h", marker_color=PINK_DEEP, text=clicks[::-1], textposition="outside", textfont={"color": INK}, cliponaxis=False))
display(_theme(fig, height=320, title=dict(text="Paid Google Ads · clicks", font=dict(size=16, color=INK)), xaxis_title="Clicks", margin=dict(t=52, b=36, l=140, r=24)))
