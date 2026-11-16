# APP: Chart · Partner Day · country — one figure.
import plotly.graph_objects as go
from IPython.display import display

PINK = "#FF91AC"
INK = "#9CA3AF"
rows = [("Germany", 198), ("Unknown", 22), ("United States", 21), ("France", 12), ("United Kingdom", 11), ("Canada", 10), ("Czechia", 8), ("Netherlands", 8), ("Austria", 8), ("India", 8), ("Italy", 7), ("Spain", 7), ("Other", 82)]
fig = go.Figure()
fig.add_bar(y=[r[0] for r in rows][::-1], x=[r[1] for r in rows][::-1], orientation="h", marker_color=PINK, text=[r[1] for r in rows][::-1], textposition="outside", textfont={"color": INK}, cliponaxis=False)
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, Arial, sans-serif", color=INK, size=13), height=440, title=dict(text="Partner Day · country", font=dict(size=16, color=INK)), xaxis_title="Salesforce Attended", margin=dict(t=52, b=36, l=120, r=40), yaxis=dict(showgrid=False, color=INK), showlegend=False)
fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
display(fig)
