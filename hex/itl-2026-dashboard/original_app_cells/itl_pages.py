import plotly.graph_objects as go
import pandas as pd

df = ga4_itl_pages[ga4_itl_pages['event_name'] == 'page_view'].copy()
week_order = ['Baseline (5-11 Oct)', 'Conference (12-18 Oct)', 'Post-week (19-25 Oct)']
df['week_label'] = pd.Categorical(df['week_label'], categories=week_order, ordered=True)
df = df.sort_values('week_label')

colors = ['#FF6D5A', '#FF6D5A', '#CCCCCC']

fig = go.Figure(go.Bar(
    x=df['week_label'].tolist(),
    y=df['event_count'].tolist(),
    marker_color=colors,
    text=[f'{v:,}' for v in df['event_count']],
    textposition='outside',
    textfont=dict(size=14, color='#333')
))

fig.add_annotation(
    x='Post-week (19-25 Oct)', y=df[df['week_label']=='Post-week (19-25 Oct)']['event_count'].values[0] + 150,
    text='No post-event content — traffic cliff',
    showarrow=True, arrowhead=2, arrowcolor='#888',
    font=dict(size=12, color='#888'), ax=0, ay=-40
)

fig.update_layout(
    title=dict(text='ITL Page Views by Week — Pre-event Peak, Post-event Cliff', font=dict(size=17)),
    yaxis_title='Page Views',
    height=360,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin={"t": 70, "b": 50, "l": 60, "r": 40},
    font={"family": "Inter, Arial, sans-serif", "color": "#333"},
    yaxis=dict(showgrid=True, gridcolor='#F0F0F0', range=[0, df['event_count'].max() * 1.3])
)

fig
