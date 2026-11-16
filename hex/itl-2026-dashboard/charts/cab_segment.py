# APP: Chart · CAB · sales segment — one figure.
import plotly.graph_objects as go
from IPython.display import display

PINK = "#FF91AC"
PINK_DEEP = "#87003C"
PINK_MID = "#FFBCCA"
INK = "#9CA3AF"
labels = ["ENT", "MM", "SMB", "Unknown"]
values = [28, 4, 6, 1]
colors = [PINK_DEEP, PINK, PINK_MID, INK]
fig = go.Figure()
fig.add_bar(y=labels[::-1], x=values[::-1], orientation="h", marker_color=colors[::-1], text=values[::-1], textposition="outside", textfont={"color": INK}, cliponaxis=False)
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, Arial, sans-serif", color=INK, size=13), height=280, title=dict(text="CAB · sales segment", font=dict(size=16, color=INK)), xaxis_title="CAB overlay people", margin=dict(t=52, b=36, l=90, r=40), yaxis=dict(showgrid=False, color=INK), showlegend=False)
fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
display(fig)
