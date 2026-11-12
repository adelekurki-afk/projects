import plotly.graph_objects as go

bar = go.Figure()
bar.add_trace(go.Bar(
    name="Partner only", x=[102], y=["1,018 unique"], orientation="h",
    marker_color="#94A3B8", text=["102"], textposition="inside",
    insidetextanchor="middle",
))
bar.add_trace(go.Bar(
    name="Both days 324", x=[324], y=["1,018 unique"], orientation="h",
    marker_color="#FF6D5A", text=["324"], textposition="inside",
    insidetextanchor="middle",
))
bar.add_trace(go.Bar(
    name="Eco only", x=[592], y=["1,018 unique"], orientation="h",
    marker_color="#4F7FB8", text=["592"], textposition="inside",
    insidetextanchor="middle",
))
bar.update_layout(
    barmode="stack",
    height=220,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(t=40, b=30, l=20, r=20),
    font=dict(family="Inter, Arial, sans-serif", color="#333", size=12),
    legend=dict(orientation="h", y=1.25, x=0),
    xaxis=dict(visible=False),
    yaxis=dict(title=""),
)
bar
