# APP: Staff and Speakers
# Snapshot 10 Nov 2026. Per-day scans only (no either-day unique).
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display, Markdown

PINK = "#FF91AC"
PINK_MID = "#FFBCCA"
PINK_DEEP = "#87003C"
INK = "#9CA3AF"


def _brand_table(df, title=""):
    frame = pd.DataFrame(df)
    cols = [str(c) for c in frame.columns]
    n = len(frame)
    vals = [[("" if v is None else str(v)) for v in frame[c].tolist()] for c in frame.columns]
    stripe = [PINK_MID if i % 2 == 0 else "rgba(255,145,172,0.20)" for i in range(n)]
    fig = go.Figure(
        go.Table(
            header=dict(
                values=cols,
                fill_color=PINK_DEEP,
                font=dict(color="#F9FAFB", size=12, family="Inter, Arial, sans-serif"),
                align="left",
                line_color=PINK,
                height=30,
            ),
            cells=dict(
                values=vals,
                fill_color=[stripe] * len(cols),
                font=dict(color=INK, size=12, family="Inter, Arial, sans-serif"),
                align="left",
                line_color="rgba(255,145,172,0.35)",
                height=26,
            ),
        )
    )
    top = 44 if title else 8
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(text=title, font=dict(size=15, color=INK)) if title else None,
        height=min(max(top + 30 + 26 * max(n, 1) + 16, 110), 780),
        margin=dict(t=top, b=8, l=4, r=4),
        font=dict(family="Inter, Arial, sans-serif", color=INK),
    )
    return fig


staff_kpis = [
    (113, "Staff tickets", "Fliplet Ticket family = Staff"),
    (168, "n8n on any ticket", "13 staff, 48 speaker, 107 other"),
    (40, "C2 crew tickets", "Largest staff bucket"),
    (76, "Speaker tickets", "Fliplet Ticket family = Speakers"),
]
staff_fig = go.Figure()
for i, (val, title, sub) in enumerate(staff_kpis):
    x0, x1 = i / 4 + 0.01, (i + 1) / 4 - 0.01
    staff_fig.add_trace(go.Indicator(
        mode="number", value=val,
        number={"font": {"size": 32, "color": "#FF6D5A"}, "valueformat": ",.0f"},
        title={"text": f"<b>{title}</b><br><span style='font-size:11px;color:#888'>{sub}</span>"},
        domain={"x": [x0, x1], "y": [0, 1]},
    ))
staff_fig.update_layout(
    title=dict(text="Staff", font=dict(size=18)),
    height=200, paper_bgcolor="white", margin=dict(t=50, b=10, l=10, r=10),
    font=dict(family="Inter, Arial, sans-serif", color="#333"),
)
display(staff_fig)

staff = pd.DataFrame([
    {"crew": "C2", "registered": 40, "partner_day": 0, "eco_day": 2},
    {"crew": "Hospitality / QT Events", "registered": 36, "partner_day": 8, "eco_day": 6},
    {"crew": "Content / merch / film", "registered": 19, "partner_day": 1, "eco_day": 2},
    {"crew": "n8n (staff ticket)", "registered": 13, "partner_day": 6, "eco_day": 8},
    {"crew": "Other crew", "registered": 5, "partner_day": 3, "eco_day": 1},
])
staff_bar = go.Figure()
staff_bar.add_trace(go.Bar(name="Partner Day scans", x=staff["crew"], y=staff["partner_day"], marker_color="#4F7FB8", text=staff["partner_day"], textposition="outside"))
staff_bar.add_trace(go.Bar(name="Eco Day scans", x=staff["crew"], y=staff["eco_day"], marker_color="#FF6D5A", text=staff["eco_day"], textposition="outside"))
staff_bar.update_layout(
    barmode="group",
    title=dict(text="Staff door scans by day", font=dict(size=16)),
    height=380, paper_bgcolor="white", plot_bgcolor="white",
    margin=dict(t=60, b=80, l=40, r=20),
    font=dict(family="Inter, Arial, sans-serif", color="#333"),
    legend=dict(orientation="h", y=1.12, x=1, xanchor="right"),
)
staff_bar.update_xaxes(tickangle=15)
display(staff_bar)
display(_brand_table(staff, "Staff by crew"))
display(Markdown("Purchases has Ticket family Staff (113). Crew rarely used the attendee door scan, so scan counts are lower than tickets."))

speaker_kpis = [
    (116, "Programme speakers", "Speakers tab in Fliplet raw workbook"),
    (62, "n8n speakers", "Company = n8n on the Speakers tab"),
    (54, "External speakers", "Non-n8n on the Speakers tab"),
    (76, "Speaker tickets", "Fliplet Ticket family = Speakers"),
]
spk_fig = go.Figure()
for i, (val, title, sub) in enumerate(speaker_kpis):
    x0, x1 = i / 4 + 0.01, (i + 1) / 4 - 0.01
    spk_fig.add_trace(go.Indicator(
        mode="number", value=val,
        number={"font": {"size": 32, "color": "#FF6D5A"}, "valueformat": ",.0f"},
        title={"text": f"<b>{title}</b><br><span style='font-size:11px;color:#888'>{sub}</span>"},
        domain={"x": [x0, x1], "y": [0, 1]},
    ))
spk_fig.update_layout(
    title=dict(text="Speakers", font=dict(size=18)),
    height=200, paper_bgcolor="white", margin=dict(t=50, b=10, l=10, r=10),
    font=dict(family="Inter, Arial, sans-serif", color="#333"),
)
display(spk_fig)

speakers = pd.DataFrame([
    {"day": "Partner Day", "speakers": 86},
    {"day": "Ecosystem Day", "speakers": 79},
])
spk_bar = go.Figure(go.Bar(
    x=speakers["day"], y=speakers["speakers"], marker_color="#FF6D5A",
    text=speakers["speakers"], textposition="outside",
))
spk_bar.update_layout(
    title=dict(text="Programme speakers scanned by day", font=dict(size=16)),
    height=340, paper_bgcolor="white", plot_bgcolor="white",
    margin=dict(t=60, b=40, l=40, r=20),
    font=dict(family="Inter, Arial, sans-serif", color="#333"),
    yaxis=dict(title="Speakers"),
)
display(spk_bar)
display(Markdown("86 programme speakers on Partner Day (62 door on 13 Oct + Monday badge), 79 on Ecosystem Day. 60 of them are in both day counts."))
display(_brand_table(speakers, "Programme speakers by day"))
