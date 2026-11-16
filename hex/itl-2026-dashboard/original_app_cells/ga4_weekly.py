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

if not _itl_ready('ga4_post_event_trend'):
    fig = _itl_empty()
else:
    try:
        import pandas as pd
        from plotly.subplots import make_subplots

        df = ga4_post_event_trend.copy()
        df['week_start'] = pd.to_datetime(df['week_start'])
        fig = make_subplots(
            rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
            subplot_titles=('n8n.io users and Berlin events', 'YouTube and LinkedIn arrivals on n8n.io'),
            row_heights=[0.58, 0.42],
        )
        fig.add_trace(go.Scatter(
            x=df['week_start'], y=df['n8n_users'], name='Users',
            mode='lines+markers', line=dict(color='#FF6D5A', width=2.5), marker=dict(size=6),
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=df['week_start'], y=df['berlin_events'], name='Berlin events',
            mode='lines+markers', line=dict(color='#4F7FB8', width=2.5), marker=dict(size=6),
        ), row=1, col=1)
        yt = df['youtube_referrer_events'] if 'youtube_referrer_events' in df.columns else 0
        li = df['linkedin_referrer_events'] if 'linkedin_referrer_events' in df.columns else 0
        fig.add_trace(go.Scatter(
            x=df['week_start'], y=yt, name='YouTube → n8n.io',
            mode='lines+markers', line=dict(color='#7C5CBF', width=2.5), marker=dict(size=6),
        ), row=2, col=1)
        fig.add_trace(go.Scatter(
            x=df['week_start'], y=li, name='LinkedIn → n8n.io',
            mode='lines+markers', line=dict(color='#0A66C2', width=2.5), marker=dict(size=6),
        ), row=2, col=1)
        fig.add_vrect(
            x0='2026-10-12', x1='2026-10-19', fillcolor='#FF6D5A', opacity=0.12,
            line_width=0, annotation_text='Conference week', annotation_position='top left',
            row=1, col=1,
        )
        fig.update_layout(
            title=dict(text='n8n.io traffic · June–November 2026', font=dict(size=18)),
            height=680,
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(t=90, b=40, l=50, r=30),
            font=dict(family='Inter, Arial, sans-serif', color='#333'),
            legend=dict(orientation='h', y=1.08, x=1, xanchor='right'),
        )
        fig.update_yaxes(showgrid=True, gridcolor='#F0F0F0')
        fig.update_xaxes(showgrid=False)
    except Exception as e:
        fig = _itl_empty("Run all first (" + type(e).__name__ + ")")
fig
