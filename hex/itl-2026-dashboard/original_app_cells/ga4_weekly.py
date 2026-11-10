import plotly.graph_objects as go
import pandas as pd

df = ga4_signup_weekly.copy()
week_order = ['Baseline (5-11 Oct)', 'Conference (12-18 Oct)', 'Post-week (19-25 Oct)']
df['week_label'] = pd.Categorical(df['week_label'], categories=week_order, ordered=True)
df = df.sort_values('week_label')
weeks = df['week_label'].tolist()

fig = go.Figure()

fig.add_trace(go.Bar(
    name='Berlin Events',
    x=weeks,
    y=df['berlin_events'].tolist(),
    marker_color='#FF6D5A',
    text=[f'{v:,}' for v in df['berlin_events']],
    textposition='outside'
))
fig.add_trace(go.Bar(
    name='CTA Clicks',
    x=weeks,
    y=df['cta_clicks'].tolist(),
    marker_color='#2D2D2D',
    text=[f'{v:,}' for v in df['cta_clicks']],
    textposition='outside'
))
fig.add_trace(go.Bar(
    name='Trial Starts',
    x=weeks,
    y=df['trial_starts'].tolist(),
    marker_color='#9B9B9B',
    text=[f'{v:,}' for v in df['trial_starts']],
    textposition='outside'
))
fig.add_trace(go.Bar(
    name='Sales Form Completions',
    x=weeks,
    y=df['sales_form_completions'].tolist(),
    marker_color='#CCCCCC',
    text=[f'{v:,}' for v in df['sales_form_completions']],
    textposition='outside'
))

fig.update_layout(
    barmode='group',
    title=dict(text='n8n.io Signals — 3 Weeks Around Event<br><sup>Berlin +33% on-site; global CTA clicks flat — no organic halo effect detected</sup>', font=dict(size=17)),
    height=440,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin={"t": 90, "b": 50, "l": 40, "r": 40},
    font={"family": "Inter, Arial, sans-serif", "color": "#333"},
    legend=dict(orientation='h', yanchor='bottom', y=1.10, xanchor='right', x=1),
    yaxis=dict(showgrid=True, gridcolor='#F0F0F0')
)

fig
