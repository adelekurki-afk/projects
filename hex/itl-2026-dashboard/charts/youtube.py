# APP: Chart · YouTube views gained — one figure. Classic App only shows the first display().
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


weeks = ["2026-07-06","2026-07-13","2026-07-20","2026-07-27","2026-08-03","2026-08-10","2026-08-17","2026-08-24","2026-08-31","2026-09-07","2026-09-14","2026-09-21","2026-09-28","2026-10-05","2026-10-12","2026-10-19","2026-10-26","2026-11-02"]
views = [3248654,2866279,2934305,2757976,2793957,2906293,2599058,3207865,4148747,3928055,3822707,3743902,3595988,3611676,3424076,3189414,2983691,2820043]
fig = go.Figure()
fig.add_scatter(x=weeks, y=views, mode="lines", name="Views gained", line=dict(color=CORAL, width=2))
fig.add_vrect(x0="2026-10-12", x1="2026-10-18", fillcolor=CORAL, opacity=0.18, line_width=0, annotation_text="ITL week", annotation_position="top left", annotation_font=dict(color=INK, size=11))
display(_theme(fig, height=320, title=dict(text="YouTube views gained", font=dict(size=16, color=INK)), yaxis_title="Views"))
