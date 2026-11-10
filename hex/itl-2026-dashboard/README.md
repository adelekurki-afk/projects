# In the Loop 2026 — Hex dashboard

Preferred path is the **Notebook / Classic app** (Plotly KPI tiles and charts). That avoids Hex Generative App.js `React` crashes.

Project: **In the Loop 2026 — Lead & Pipeline Dashboard**

## Use the notebook (recommended)

1. Open the Hex project → **Notebook**.
2. Run the cells labelled **APP: Fliplet overlapping days** and **APP: Staff and Speakers**.
3. Live check: the first output must read **NOV 10 NOTEBOOK v7 is live**.
4. To share: App builder → **Classic app** (not Generative) → pin those cells plus pipeline/GA4.

## Optional: Generative App.js

Only if you still want the code-generated app. Select-All replace `app/App.js`. First line `import "app/app.css";`. Second line must be `import { createElement as h, useMemo, useState } from "react";`. There must be no `React.` anywhere. Orange banner **NOV 10 FULL PASTE v7**.

Do not add extra `useHexData` ids. Only the original seven remain.

## What changed in v7

Hex Preview said `React is not defined`. The paste no longer uses a `React` global. The same visuals now live as Plotly cells in the notebook so you do not have to fight App.js.

## Sources

- [Fliplet raw workbook](https://docs.google.com/spreadsheets/d/1ZGiFP8wgcpaFESOY7WuDSgwGdztCTivzmwdWK87JsrU) — Purchases (tickets, including unpaid/comp, staff, speakers) and Scans (door scans). Partner Day = 13 Oct Berlin, Ecosystem Day = 14 Oct Berlin. Overlapping on purpose.
- [CAB In The Loop](https://docs.google.com/spreadsheets/d/1DqaA_-hvfExo1bhHviBZTdKAdiSrnLJc8yLuV9Bo_Xg) — 11 members + 28 guests, all redeemed.
- Salesforce / BigQuery stays for pipeline and the commercial ITL Free/Paid funnel only.

Hex has no Google Sheets connection, so the notebook inlines the 10 Nov 2026 snapshot.
