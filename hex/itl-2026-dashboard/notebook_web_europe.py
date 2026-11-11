import plotly.graph_objects as go

try:
    from IPython.display import display
except ImportError:
    def display(obj):
        return obj


def _itl_empty(msg="Run all, then refresh the App."):
    fig = go.Figure()
    fig.add_annotation(text=msg, showarrow=False, font=dict(size=14, color="#6B7280"))
    fig.update_layout(
        height=220,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(t=20, b=20, l=20, r=20),
        font=dict(family="Inter, Arial, sans-serif", color="#333"),
    )
    return fig


def _itl_ready(*names):
    return all(name in globals() for name in names)


if not _itl_ready("ga4_web_europe_countries"):
    fig = _itl_empty()
else:
    df = ga4_web_europe_countries.copy()
    df = df.sort_values("users", ascending=True)
    colors = ["#FF6D5A" if str(c) == "Germany" else "#4F7FB8" for c in df["country"]]
    fig = go.Figure(go.Bar(
        y=df["country"],
        x=df["users"],
        orientation="h",
        marker_color=colors,
        text=[f"{int(v):,}" for v in df["users"]],
        textposition="outside",
    ))
    fig.update_layout(
        title=dict(text="n8n website users in Europe · Jun–Nov", font=dict(size=16)),
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=60, b=40, l=80, r=40),
        font=dict(family="Inter, Arial, sans-serif", color="#333"),
        xaxis=dict(title="Users", showgrid=True, gridcolor="#F0F0F0"),
        yaxis=dict(title=""),
    )

fig
