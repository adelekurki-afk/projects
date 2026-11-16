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

if not _itl_ready('ga4_social_landings'):
    fig = _itl_empty()
else:
    try:
        import pandas as pd
        df = ga4_social_landings.copy()
        df['label'] = df['page'].astype(str).str.slice(0, 60)
        fig = go.Figure()
        for social, color in [('YouTube', '#7C5CBF'), ('LinkedIn', '#0A66C2')]:
            part = df[df['social'] == social].sort_values('page_views')
            fig.add_trace(go.Bar(
                name=social,
                y=part['label'],
                x=part['page_views'],
                orientation='h',
                marker_color=color,
                text=[f'{int(v):,}' for v in part['page_views']],
                textposition='outside',
            ))
        fig.update_layout(
            barmode='group',
            title=dict(text='n8n.io pages reached from YouTube or LinkedIn', font=dict(size=16)),
            xaxis_title='Page views',
            height=480,
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(t=60, b=40, l=280, r=60),
            font=dict(family='Inter, Arial, sans-serif', color='#333'),
            legend=dict(orientation='h', y=1.08, x=1, xanchor='right'),
            xaxis=dict(showgrid=True, gridcolor='#F0F0F0'),
        )
    except Exception as e:
        fig = _itl_empty("Run all first (" + type(e).__name__ + ")")
fig
