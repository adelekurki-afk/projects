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


if not _itl_ready("ga4_post_event_trend"):
    fig = _itl_empty()
else:
    try:
        from plotly.subplots import make_subplots
        tr = ga4_post_event_trend.copy()
        tr["week_start"] = tr["week_start"].astype(str)
        fig = make_subplots(
            rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.12,
            subplot_titles=("n8n.io events & users", "Trial starts, sales forms, YouTube → n8n.io"),
        )
        fig.add_trace(go.Scatter(x=tr["week_start"], y=tr["n8n_events"], name="Events", line=dict(color="#2D2D2D")), row=1, col=1)
        fig.add_trace(go.Scatter(x=tr["week_start"], y=tr["n8n_users"], name="Users", line=dict(color="#FF6D5A")), row=1, col=1)
        fig.add_trace(go.Bar(x=tr["week_start"], y=tr["trial_starts"], name="Trial starts", marker_color="#FF6D5A"), row=2, col=1)
        fig.add_trace(go.Bar(x=tr["week_start"], y=tr["sales_form_completions"], name="Sales forms", marker_color="#2D2D2D"), row=2, col=1)
        fig.add_trace(go.Scatter(x=tr["week_start"], y=tr["youtube_referrer_events"], name="YouTube → n8n.io", line=dict(color="#7C5CBF")), row=2, col=1)
        fig.update_layout(
            title=dict(text="n8n.io web traffic · Jun–Nov", font=dict(size=16)),
            height=520, paper_bgcolor="white", plot_bgcolor="white",
            margin=dict(t=80, b=40, l=50, r=20),
            font=dict(family="Inter, Arial, sans-serif", color="#333"),
            legend=dict(orientation="h", y=1.08),
            barmode="group",
        )
    except Exception as e:
        fig = _itl_empty("Run all first (" + type(e).__name__ + ")")

fig
