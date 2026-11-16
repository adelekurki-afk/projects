# APP: Chart · Partner Day · region — one figure.
import plotly.graph_objects as go
from IPython.display import display

PINK = "#FF91AC"
INK = "#9CA3AF"
labels = ["DACH", "North EMEA", "South EMEA", "US", "Other"]
values = [121, 29, 35, 22, 196]
fig = go.Figure()
fig.add_bar(y=labels[::-1], x=values[::-1], orientation="h", marker_color=PINK, text=values[::-1], textposition="outside", textfont={"color": INK}, cliponaxis=False)
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, Arial, sans-serif", color=INK, size=13), height=300, title=dict(text="Partner Day · region", font=dict(size=16, color=INK)), xaxis_title="Salesforce Attended", margin=dict(t=52, b=36, l=110, r=40), yaxis=dict(showgrid=False, color=INK), showlegend=False)
fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
display(fig)
