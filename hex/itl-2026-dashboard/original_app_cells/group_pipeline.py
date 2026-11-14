import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

pipe = attendance_group_pipeline.copy()
funnel = attendance_group_funnel.copy()

group_colors = {
    'Both Days':            '#FF6D5A',
    'Partner Day only':     '#FF8F80',
    'Ecosystem Day only':   '#2D2D2D',
    'Gap (Did Not Attend)': '#CCCCCC',
}

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=(
        'Pipeline by Group (€, account-deduplicated)',
        'Meeting Rate vs Opp Rate (%)'
    ),
    column_widths=[0.55, 0.45],
    horizontal_spacing=0.12
)

for grp in pipe['attendance_group'].unique():
    row = pipe[pipe['attendance_group'] == grp].iloc[0]
    color = group_colors.get(grp, '#888')
    fig.add_trace(go.Bar(
        name=f'{grp} — open',
        x=[grp],
        y=[row['open_pipeline']],
        marker_color=color,
        opacity=0.8,
        text=[f'€{row["open_pipeline"]/1000:.0f}K'],
        textposition='inside',
        textfont=dict(color='white', size=11),
        legendgroup=grp,
        showlegend=False
    ), row=1, col=1)
    if row['closed_won_amount'] > 0:
        fig.add_trace(go.Bar(
            name=f'{grp} — won',
            x=[grp],
            y=[row['closed_won_amount']],
            marker_color='#2D2D2D',
            text=[f'€{row["closed_won_amount"]/1000:.0f}K won'],
            textposition='inside',
            textfont=dict(color='white', size=10),
            legendgroup=grp,
            showlegend=False
        ), row=1, col=1)

fig.add_trace(go.Bar(
    name='Meeting Rate %',
    x=funnel['attendance_group'].tolist(),
    y=[float(v) for v in funnel['meeting_rate_pct']],
    marker_color='#FF6D5A',
    text=[f'{v}%' for v in funnel['meeting_rate_pct']],
    textposition='outside'
), row=1, col=2)

fig.add_trace(go.Bar(
    name='Opp Rate %',
    x=funnel['attendance_group'].tolist(),
    y=[float(v) for v in funnel['opp_rate_pct']],
    marker_color='#2D2D2D',
    text=[f'{v}%' for v in funnel['opp_rate_pct']],
    textposition='outside'
), row=1, col=2)

fig.update_layout(
    barmode='group',
    title=dict(text='Pipeline & Conversion Rates by Attendance Group', font=dict(size=18)),
    height=440,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin={'t': 80, 'b': 90, 'l': 40, 'r': 40},
    font={'family': 'Inter, Arial, sans-serif', 'color': '#333'},
    legend=dict(orientation='h', yanchor='bottom', y=1.08, xanchor='right', x=1),
    yaxis=dict(showgrid=True, gridcolor='#F0F0F0'),
    yaxis2=dict(showgrid=True, gridcolor='#F0F0F0')
)
fig.update_xaxes(tickangle=15)

fig
