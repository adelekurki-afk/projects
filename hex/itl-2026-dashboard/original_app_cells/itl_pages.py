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

if not _itl_ready('ga4_itl_weekly_pages'):
    fig = _itl_empty()
else:
    try:
        import pandas as pd
        df = ga4_itl_weekly_pages.copy()
        df['week_start'] = pd.to_datetime(df['week_start'])
        fig = go.Figure(go.Bar(
            x=df['week_start'],
            y=df['itl_page_views'],
            marker_color='#FF6D5A',
            text=[f'{int(v):,}' for v in df['itl_page_views']],
            textposition='outside',
        ))
        fig.add_vrect(
            x0='2026-10-12', x1='2026-10-19', fillcolor='#4F7FB8', opacity=0.12,
            line_width=0, annotation_text='Conference week', annotation_position='top left',
        )
        fig.update_layout(
            title=dict(text='In-the-loop page views by week · June–November', font=dict(size=17)),
            yaxis_title='Page views',
            height=420,
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(t=70, b=40, l=60, r=30),
            font=dict(family='Inter, Arial, sans-serif', color='#333'),
            yaxis=dict(showgrid=True, gridcolor='#F0F0F0'),
        )
    except Exception as e:
        fig = _itl_empty("Run all first (" + type(e).__name__ + ")")
fig
