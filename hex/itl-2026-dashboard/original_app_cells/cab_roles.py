import plotly.graph_objects as go
from plotly.subplots import make_subplots
from IPython.display import display

cab = cab_overlay_kpis.copy()
cab_fig = go.Figure()
colors = {'CAB total (overlay)': '#7C5CBF', 'CAB Member': '#5B8DEF', 'CAB Guest': '#3DDC97'}
n = len(cab)
for idx, row in cab.iterrows():
    grp = row['attendance_group']
    color = colors.get(grp, '#888')
    x0, x1 = idx / n + 0.02, (idx + 1) / n - 0.02
    cab_fig.add_trace(go.Indicator(
        mode='number', value=int(row['on_cab_list']),
        number={'font': {'size': 34, 'color': color}},
        title={'text': f"<b>{grp}</b><br><span style='font-size:11px;color:#888'>{int(row['in_itl_registrants'])} in ITL · {int(row['with_opp'])} with opp ({row['opp_rate_pct']}%)</span>"},
        domain={'x': [x0, x1], 'y': [0, 1]},
    ))
cab_fig.update_layout(
    title=dict(text='CAB overlay — already counted in Both Days / Eco Day (0 meetings booked)', font=dict(size=16)),
    height=200, paper_bgcolor='white', margin=dict(t=60, b=10, l=10, r=10),
    font=dict(family='Inter, Arial, sans-serif', color='#333'),
)
display(cab_fig)

pr = persona_by_role.copy().sort_values('registrants', ascending=True)
role_fig = go.Figure(go.Bar(
    y=pr['persona'], x=pr['registrants'], orientation='h',
    marker_color='#FF6D5A',
    text=[f"{int(r.registrants)} · meet {r.meeting_rate_pct}% · opp {r.opp_rate_pct}%" for r in pr.itertuples()],
    textposition='outside',
))
role_fig.update_layout(
    title=dict(text='Registrants by role (Salesforce Title)', font=dict(size=16)),
    height=420, paper_bgcolor='white', plot_bgcolor='white',
    margin=dict(t=50, b=30, l=160, r=160),
    xaxis_title='Registrants',
    font=dict(family='Inter, Arial, sans-serif', color='#333'),
)
display(role_fig)

tr = ga4_post_event_trend.copy()
tr['week_start'] = tr['week_start'].astype(str)
traffic = make_subplots(
    rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.12,
    subplot_titles=('n8n.io events & users', 'Signup proxies (no native sign_up event) + YouTube referrer'),
)
traffic.add_trace(go.Scatter(x=tr['week_start'], y=tr['n8n_events'], name='Events', line=dict(color='#2D2D2D')), row=1, col=1)
traffic.add_trace(go.Scatter(x=tr['week_start'], y=tr['n8n_users'], name='Users', line=dict(color='#FF6D5A')), row=1, col=1)
traffic.add_trace(go.Bar(x=tr['week_start'], y=tr['trial_starts'], name='Trial starts', marker_color='#FF6D5A'), row=2, col=1)
traffic.add_trace(go.Bar(x=tr['week_start'], y=tr['sales_form_completions'], name='Sales forms', marker_color='#2D2D2D'), row=2, col=1)
traffic.add_trace(go.Scatter(x=tr['week_start'], y=tr['youtube_referrer_events'], name='YouTube → n8n.io events', line=dict(color='#7C5CBF')), row=2, col=1)
traffic.update_layout(
    title=dict(text='Post-event web traffic, signup proxies, YouTube referrer (through 8 Nov)', font=dict(size=16)),
    height=520, paper_bgcolor='white', plot_bgcolor='white',
    margin=dict(t=80, b=40, l=50, r=20),
    font=dict(family='Inter, Arial, sans-serif', color='#333'),
    legend=dict(orientation='h', y=1.08),
    barmode='group',
)
display(traffic)

itl = ga4_itl_weekly_pages.copy()
itl['week_start'] = itl['week_start'].astype(str)
itl_fig = go.Figure(go.Bar(
    x=itl['week_start'], y=itl['itl_page_views'], marker_color='#FF6D5A',
    text=itl['itl_page_views'], textposition='outside',
))
itl_fig.update_layout(
    title=dict(text='ITL landing page_view by week', font=dict(size=16)),
    height=280, paper_bgcolor='white', plot_bgcolor='white',
    margin=dict(t=50, b=40, l=40, r=20),
    font=dict(family='Inter, Arial, sans-serif', color='#333'),
)
display(itl_fig)
