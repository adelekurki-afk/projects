# APP: Partner vs Eco bars — one figure. Ticket sales live on Registration.
import plotly.graph_objects as go
from IPython.display import display

PINK = "#FF91AC"
BLUE = "#5B8FC7"
INK = "#9CA3AF"

regions = ["EMEA", "Unknown", "NA", "LATAM", "APAC", "ANZ"]
partner = [194, 154, 48, 5, 1, 1]
eco = [415, 358, 80, 4, 8, 0]
fig = go.Figure()
fig.add_bar(
    name="Partner Day",
    y=regions[::-1],
    x=partner[::-1],
    orientation="h",
    marker_color=PINK,
    text=partner[::-1],
    textposition="outside",
    textfont={"color": INK},
    cliponaxis=False,
)
fig.add_bar(
    name="Ecosystem Day",
    y=regions[::-1],
    x=eco[::-1],
    orientation="h",
    marker_color=BLUE,
    text=[v if v else "" for v in eco[::-1]],
    textposition="outside",
    textfont={"color": INK},
    cliponaxis=False,
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, Arial, sans-serif", color=INK, size=13),
    height=340,
    barmode="group",
    bargap=0.28,
    title=dict(text="Partner vs Eco · Salesforce Attended by region", font=dict(size=16, color=INK)),
    xaxis_title="People",
    legend=dict(orientation="h", y=-0.22, x=0, bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
    margin=dict(t=52, b=80, l=90, r=24),
    yaxis=dict(showgrid=False, color=INK),
)
fig.update_xaxes(showgrid=True, gridcolor="rgba(156,163,175,0.18)", zeroline=False, color=INK)
display(fig)
