import plotly.graph_objects as go
import pandas as pd

df = attendance_group_funnel.copy()

group_colors = {
    'Both Days':            '#FF6D5A',
    'Partner Day only':     '#FF8F80',
    'Ecosystem Day only':   '#2D2D2D',
    'Gap (Did Not Attend)': '#CCCCCC',
}

groups = df['attendance_group'].tolist()
n = len(groups)

fig = go.Figure()

for idx, (_, row) in enumerate(df.iterrows()):
    grp = row['attendance_group']
    color = group_colors.get(grp, '#888')
    col_start = idx / n
    col_end   = (idx + 1) / n

    fig.add_trace(go.Indicator(
        mode='number',
        value=int(row['registrants']),
        number={'font': {'size': 38, 'color': color}},
        title={'text': f'<b>{grp}</b><br><span style="font-size:11px;color:#888">Registrants</span>'},
        domain={'x': [col_start + 0.01, col_end - 0.01], 'y': [0.73, 1.0]}
    ))

    fig.add_trace(go.Indicator(
        mode='number',
        value=float(row['meeting_rate_pct']),
        number={'suffix': '%', 'font': {'size': 34, 'color': color}},
        title={'text': f'<span style="font-size:12px;color:#333">Meeting Rate</span><br><span style="font-size:11px;color:#888">{int(row["meetings_booked"])} meetings booked</span>'},
        domain={'x': [col_start + 0.01, col_end - 0.01], 'y': [0.38, 0.65]}
    ))

    fig.add_trace(go.Indicator(
        mode='number',
        value=float(row['opp_rate_pct']),
        number={'suffix': '%', 'font': {'size': 34, 'color': color}},
        title={'text': f'<span style="font-size:12px;color:#333">Opp Rate</span><br><span style="font-size:11px;color:#888">{int(row["with_opp"])} with active opp</span>'},
        domain={'x': [col_start + 0.01, col_end - 0.01], 'y': [0.03, 0.30]}
    ))

fig.update_layout(
    title=dict(text='Attendance Group — KPI Scorecards', font=dict(size=18)),
    height=480,
    paper_bgcolor='white',
    margin={'t': 60, 'b': 20, 'l': 10, 'r': 10},
    font={'family': 'Inter, Arial, sans-serif', 'color': '#333'}
)

fig
