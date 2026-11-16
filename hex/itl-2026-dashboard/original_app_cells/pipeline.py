import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

df = pipeline_arr.copy()
df['label'] = df['opp_type'] + ' / ' + df['segment']
df = df.sort_values('total_amount', ascending=False)

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Pipeline by Type & Segment (€)", "Deal Counts"),
    column_widths=[0.65, 0.35]
)

fig.add_trace(go.Bar(
    name='Open Pipeline',
    x=df['label'],
    y=df['open_pipeline_amount'],
    marker_color='#FF6D5A',
    text=[f'€{v/1000:.0f}K' for v in df['open_pipeline_amount']],
    textposition='inside',
    textfont=dict(color='white', size=11)
), row=1, col=1)

fig.add_trace(go.Bar(
    name='Closed Won',
    x=df['label'],
    y=df['closed_won_amount'],
    marker_color='#2D2D2D',
    text=[f'€{v/1000:.0f}K' if v > 0 else '' for v in df['closed_won_amount']],
    textposition='inside',
    textfont=dict(color='white', size=11)
), row=1, col=1)

fig.add_trace(go.Bar(
    name='Open Opps',
    x=df['label'],
    y=df['open_opp_count'],
    marker_color='#FF6D5A',
    text=df['open_opp_count'],
    textposition='outside'
), row=1, col=2)

fig.add_trace(go.Bar(
    name='Won Opps',
    x=df['label'],
    y=df['closed_won_count'],
    marker_color='#2D2D2D',
    text=df['closed_won_count'],
    textposition='outside'
), row=1, col=2)

fig.update_layout(
    barmode='stack',
    title=dict(text=f"Pipeline Summary — €{df['total_amount'].sum()/1e6:.2f}M total · €{df['closed_won_amount'].sum()/1e3:.1f}K won", font=dict(size=17)),
    height=420,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin={"t": 80, "b": 80, "l": 40, "r": 40},
    font={"family": "Inter, Arial, sans-serif", "color": "#333"},
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='right', x=1)
)
fig.update_yaxes(showgrid=True, gridcolor='#F0F0F0')
fig.update_xaxes(tickangle=15)

fig
