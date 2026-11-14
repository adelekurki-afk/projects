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


if not _itl_ready("cab_overlay_kpis"):
    fig = _itl_empty()
else:
    try:
        cab = cab_overlay_kpis.copy()
        fig = go.Figure()
        colors = {"CAB total (overlay)": "#7C5CBF", "CAB Member": "#5B8DEF", "CAB Guest": "#3DDC97"}
        n = max(len(cab), 1)
        for idx, row in cab.iterrows():
            grp = row["attendance_group"]
            color = colors.get(grp, "#888")
            x0, x1 = idx / n + 0.02, (idx + 1) / n - 0.02
            fig.add_trace(go.Indicator(
                mode="number",
                value=int(row["on_cab_list"]),
                number={"font": {"size": 34, "color": color}},
                title={"text": f"<b>{grp}</b>"},
                domain={"x": [x0, x1], "y": [0, 1]},
            ))
        fig.update_layout(
            title=dict(text="CAB overlay · already inside the day tiles", font=dict(size=16)),
            height=220, paper_bgcolor="white",
            margin=dict(t=60, b=10, l=10, r=10),
            font=dict(family="Inter, Arial, sans-serif", color="#333"),
        )
    except Exception as e:
        fig = _itl_empty("Run all first (" + type(e).__name__ + ")")

fig
