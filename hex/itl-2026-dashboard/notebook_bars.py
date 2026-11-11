import plotly.graph_objects as go

days = ["Partner Day", "Ecosystem Day"]
came = [426, 916]
tickets = [487, 1205]

bar = go.Figure()
bar.add_trace(go.Bar(
    name="Came (door + badge + YES)", x=days, y=came,
    marker_color="#FF6D5A", text=came, textposition="outside",
))
bar.add_trace(go.Bar(
    name="Had a ticket for this day", x=days, y=tickets,
    marker_color="#4F7FB8", text=tickets, textposition="outside",
))
bar.update_layout(
    barmode="group",
    title=dict(text="Partner Day vs Ecosystem Day", font=dict(size=16)),
    height=380,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(t=60, b=40, l=40, r=20),
    font=dict(family="Inter, Arial, sans-serif", color="#333"),
    legend=dict(orientation="h", y=1.12, x=1, xanchor="right"),
    yaxis=dict(title="People"),
)
bar
