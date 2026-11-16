# APP: Chart · CAB · country — one figure.
import plotly.graph_objects as go
from IPython.display import display

PINK_DEEP = "#87003C"
INK = "#9CA3AF"
rows = [("Germany", 20), ("United States", 7), ("Unknown", 4), ("United Kingdom", 2), ("Poland", 2), ("Spain", 2), ("Switzerland", 2)]
fig = go.Figure()
fig.add_bar(y=[r[0] for r in rows][::-1], x=[r[1] for r in rows][::-1], orientation="h", marker_color=PINK_DEEP, text=[r[1] for r in rows][::-1], textposition="outside", textfont={"color": INK}, cliponaxis=False)
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, Arial, sans-serif", color=INK, size=13), height=320, title=dict(text="CAB · country", font=dict(size=16, color=INK)), xaxis_title="CAB overlay people", margin=dict(t=52, b=36, l=120, r=40), yaxis=dict(showgrid=False, color=INK), showlegend=False)
fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
display(fig)
