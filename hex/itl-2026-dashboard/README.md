# In the Loop 2026 — Hex dashboard

Classic App is empty after switching from Generative because **Run all does not pin cells**. Hex only auto-lays-out Classic the first time you open App builder. This project opened as Generative, so Classic is a blank canvas. The notebook still has the charts.

## Fill the empty App

Open:

https://eu.hex.tech/n8n/hex/In-the-Loop-2026-Lead-Pipeline-Dashboard-034uXvUxSyRkGfmaNynnVx

### One click

1. Stay on **App builder** (Classic).
2. Left sidebar: **Outline**.
3. **Reset layout** → **Use default layout**.
4. Remove `probe_` SQL tables from the App if they appear (does not delete the notebook).

### Or pin only visits

In **Notebook**, click **Add to app** (hexagon on the cell) on:

- APP: Executive scoreboard
- Day visit KPIs
- Partner vs Eco bars
- Staff KPIs
- CAB overlay
- Speaker KPIs

Then click **App**.

### Or prompt the Notebook agent in App builder

`Pin these cells to the Classic app, output only, in this order: APP: Executive scoreboard, Day visit KPIs, Partner vs Eco bars, Staff KPIs, CAB overlay, Speaker KPIs, Speakers by day. Do not add probe SQL tables.`

Then **Publish**.

Partner Day **391** · Ecosystem Day **878**. The 272 people who came both days are inside both numbers.
