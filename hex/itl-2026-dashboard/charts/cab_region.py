# APP: Chart · CAB · region — one figure.
import plotly.graph_objects as go
from IPython.display import display

PINK_DEEP = "#87003C"
INK = "#9CA3AF"
labels = ["DACH", "North EMEA", "South EMEA", "US", "Other", "Unknown"]
values = [19, 2, 1, 9, 7, 1]
fig = go.Figure()
fig.add_bar(y=labels[::-1], x=values[::-1], orientation="h", marker_color=PINK_DEEP, text=values[::-1], textposition="outside", textfont={"color": INK}, cliponaxis=False)
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, Arial, sans-serif", color=INK, size=13), height=320, title=dict(text="CAB · region", font=dict(size=16, color=INK)), xaxis_title="CAB overlay people", margin=dict(t=52, b=36, l=110, r=40), yaxis=dict(showgrid=False, color=INK), showlegend=False)
fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
display(fig)
