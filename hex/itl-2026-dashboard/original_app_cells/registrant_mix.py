import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

reg_deduped = registrants.drop_duplicates(subset='email')

seg_counts = reg_deduped.groupby('segment')['email'].count().reset_index()
seg_counts.columns = ['Segment', 'Count']
seg_counts = seg_counts.sort_values('Count', ascending=False)

region_counts = reg_deduped.groupby('region')['email'].count().reset_index()
region_counts.columns = ['Region', 'Count']
region_counts = region_counts.sort_values('Count', ascending=False).head(8)

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("By Segment", "By Region (top 8)"),
    horizontal_spacing=0.12
)

fig.add_trace(
    go.Bar(x=seg_counts['Segment'], y=seg_counts['Count'],
           marker_color='#FF6D5A', text=seg_counts['Count'],
           textposition='outside', name='Segment'),
    row=1, col=1
)

fig.add_trace(
    go.Bar(x=region_counts['Region'], y=region_counts['Count'],
           marker_color='#2D2D2D', text=region_counts['Count'],
           textposition='outside', name='Region'),
    row=1, col=2
)

fig.update_layout(
    title=dict(text="Who Registered?", font=dict(size=18)),
    height=380,
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin={"t": 80, "b": 40, "l": 40, "r": 40},
    font={"family": "Inter, Arial, sans-serif", "color": "#333"}
)
fig.update_yaxes(showgrid=True, gridcolor='#F0F0F0')

fig
