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
        height=220, paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        margin=dict(t=20, b=20, l=20, r=20),
        font=dict(family="Inter, Arial, sans-serif", color="#333"),
    )
    return fig


def _itl_ready(*names):
    return all(name in globals() for name in names)


if not _itl_ready("persona_by_role"):
    fig = _itl_empty()
else:
    try:
        pr = persona_by_role.copy().sort_values("registrants", ascending=True)
        fig = go.Figure(go.Bar(
            y=pr["persona"],
            x=pr["registrants"],
            orientation="h",
            marker_color="#FF6D5A",
            text=[f"{int(r.registrants)}" for r in pr.itertuples()],
            textposition="outside",
        ))
        fig.update_layout(
            title=dict(text="Registrants by role (Salesforce Title)", font=dict(size=16)),
            height=420, paper_bgcolor="white", plot_bgcolor="white",
            margin=dict(t=50, b=30, l=160, r=80),
            xaxis_title="Registrants",
            font=dict(family="Inter, Arial, sans-serif", color="#333"),
        )
    except Exception as e:
        fig = _itl_empty("Run all first (" + type(e).__name__ + ")")

fig
