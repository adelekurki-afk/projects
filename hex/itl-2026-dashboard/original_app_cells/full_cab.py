import plotly.graph_objects as go
from plotly.subplots import make_subplots
from IPython.display import display

funnel_dict = dict(zip(lead_funnel['stage'], lead_funnel['count'].astype(int)))
pct_dict = dict(zip(lead_funnel['stage'], lead_funnel['pct_of_registered'].astype(float)))

registered = int(funnel_dict.get('Registered', 0))
attended = int(funnel_dict.get('Attended (Eco Day or Partner Day)', 0))
meetings = int(funnel_dict.get('Had n8n Meeting', 0))
opps_accts = int(funnel_dict.get('Account with Opp (NB/Exp, >= Oct 12)', 0))
closed_won_n = int(funnel_dict.get('Closed Won', 0))
attend_pct = float(pct_dict.get('Attended (Eco Day or Partner Day)', 0.0))
meet_rate = round(100.0 * meetings / attended, 1) if attended else 0.0

total_pipeline = float(pipeline_arr['total_amount'].sum())
closed_won_amt = float(pipeline_arr['closed_won_amount'].sum())

kpi = go.Figure()
kpi_specs = [
    (registered, 'Total registered', '', f'{attended:,} CAB-corrected attendees'),
    (attend_pct, 'Attendance rate', '%', f'{attended:,} showed up in Berlin'),
    (meetings, 'Meetings booked', '', f'{meet_rate}% of attendees'),
    (total_pipeline, 'Pipeline created (€)', '', f'{len(pipeline_arr)} opp type/segment rows'),
    (closed_won_amt, 'Closed won (€)', '', 'Since 12 Oct 2026'),
]
for i, (val, title, suffix, sub) in enumerate(kpi_specs):
    x0, x1 = i / 5 + 0.01, (i + 1) / 5 - 0.01
    number = {'suffix': suffix, 'font': {'size': 32, 'color': '#FF6D5A' if i < 3 else '#2D2D2D'}}
    if suffix == '':
        number['valueformat'] = ',.0f'
    elif suffix == '%':
        number['valueformat'] = '.1f'
    kpi.add_trace(go.Indicator(
        mode='number',
        value=val,
        number=number,
        title={'text': f'<b>{title}</b><br><span style="font-size:11px;color:#888">{sub}</span>'},
        domain={'x': [x0, x1], 'y': [0, 1]},
    ))
kpi.update_layout(
    title=dict(text='In the Loop 2026 — CAB-corrected KPIs', font=dict(size=18)),
    height=200, paper_bgcolor='white', margin=dict(t=50, b=10, l=10, r=10),
    font=dict(family='Inter, Arial, sans-serif', color='#333'),
)
display(kpi)

stages = lead_funnel['stage'].tolist()
counts = [int(c) for c in lead_funnel['count'].tolist()]
pcts = [float(p) for p in lead_funnel['pct_of_registered'].tolist()]
funnel_fig = go.Figure(go.Funnel(
    y=stages, x=counts,
    text=[f'{c:,} ({p}%)' for c, p in zip(counts, pcts)],
    textinfo='text',
    marker=dict(color=['#FF6D5A', '#FF8F80', '#FFB3A7', '#FFC8BF', '#2D2D2D'], line=dict(width=1, color='white')),
    connector=dict(line=dict(color='#E0E0E0', dash='dot', width=2)),
))
funnel_fig.update_layout(
    title=dict(text='Registrant-to-revenue funnel (CAB-corrected attendance = 836 / 74.7%)', font=dict(size=16)),
    height=400, paper_bgcolor='white', margin=dict(t=60, b=20, l=220, r=40),
    font=dict(family='Inter, Arial, sans-serif', color='#333'),
)
display(funnel_fig)

gf = attendance_group_funnel.copy()
gp = attendance_group_pipeline.copy()
group_colors = {
    'Both Days': '#FF6D5A',
    'Partner Day only': '#FF8F80',
    'Ecosystem Day only': '#2D2D2D',
    'Gap (Did Not Attend)': '#CCCCCC',
}
groups = gf['attendance_group'].tolist()
n = max(len(groups), 1)
group_fig = go.Figure()
for idx, (_, row) in enumerate(gf.iterrows()):
    grp = row['attendance_group']
    color = group_colors.get(grp, '#888')
    x0, x1 = idx / n + 0.01, (idx + 1) / n - 0.01
    group_fig.add_trace(go.Indicator(
        mode='number', value=int(row['registrants']),
        number={'font': {'size': 34, 'color': color}},
        title={'text': f'<b>{grp}</b><br><span style="font-size:11px;color:#888">Registrants</span>'},
        domain={'x': [x0, x1], 'y': [0.70, 1.0]},
    ))
    group_fig.add_trace(go.Indicator(
        mode='number', value=float(row['meeting_rate_pct']),
        number={'suffix': '%', 'font': {'size': 28, 'color': color}},
        title={'text': f'<span style="font-size:12px">Meeting rate</span><br><span style="font-size:11px;color:#888">{int(row["meetings_booked"])} meetings</span>'},
        domain={'x': [x0, x1], 'y': [0.35, 0.62]},
    ))
    group_fig.add_trace(go.Indicator(
        mode='number', value=float(row['opp_rate_pct']),
        number={'suffix': '%', 'font': {'size': 28, 'color': color}},
        title={'text': f'<span style="font-size:12px">Opp rate</span><br><span style="font-size:11px;color:#888">{int(row["with_opp"])} with opp</span>'},
        domain={'x': [x0, x1], 'y': [0.0, 0.27]},
    ))
group_fig.update_layout(
    title=dict(text='Attendance groups — CAB-corrected', font=dict(size=16)),
    height=420, paper_bgcolor='white', margin=dict(t=50, b=10, l=10, r=10),
    font=dict(family='Inter, Arial, sans-serif', color='#333'),
)
display(group_fig)

pipe_fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Pipeline by group (€)', 'Meeting rate vs opp rate (%)'),
    column_widths=[0.55, 0.45], horizontal_spacing=0.12,
)
for grp in gp['attendance_group']:
    row = gp[gp['attendance_group'] == grp].iloc[0]
    color = group_colors.get(grp, '#888')
    pipe_fig.add_trace(go.Bar(
        name=grp, x=[grp], y=[row['open_pipeline']],
        marker_color=color, text=[f"€{row['open_pipeline']/1000:.0f}K"],
        textposition='inside', showlegend=False,
    ), row=1, col=1)
    if float(row['closed_won_amount']) > 0:
        pipe_fig.add_trace(go.Bar(
            x=[grp], y=[row['closed_won_amount']], marker_color='#2D2D2D',
            text=[f"€{row['closed_won_amount']/1000:.0f}K won"], textposition='inside',
            showlegend=False,
        ), row=1, col=1)
pipe_fig.add_trace(go.Bar(
    name='Meeting rate %', x=gf['attendance_group'].tolist(),
    y=[float(v) for v in gf['meeting_rate_pct']], marker_color='#FF6D5A',
    text=[f'{v}%' for v in gf['meeting_rate_pct']], textposition='outside',
), row=1, col=2)
pipe_fig.add_trace(go.Bar(
    name='Opp rate %', x=gf['attendance_group'].tolist(),
    y=[float(v) for v in gf['opp_rate_pct']], marker_color='#2D2D2D',
    text=[f'{v}%' for v in gf['opp_rate_pct']], textposition='outside',
), row=1, col=2)
pipe_fig.update_layout(
    barmode='group',
    title=dict(text='Pipeline and conversion by attendance group', font=dict(size=16)),
    height=420, paper_bgcolor='white', plot_bgcolor='white',
    margin=dict(t=80, b=80, l=40, r=40),
    font=dict(family='Inter, Arial, sans-serif', color='#333'),
    legend=dict(orientation='h', y=1.08, x=1, xanchor='right'),
)
pipe_fig.update_xaxes(tickangle=15)
display(pipe_fig)
