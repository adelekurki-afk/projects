# In the Loop 2026 — Classic App

Continue editing Adele’s original Hex project in **Classic App** format: pinned markdown, HTML scoreboard, and Plotly tiles. Do not paste App.js. Do not switch back to Generative.

Open:

https://eu.hex.tech/n8n/hex/In-the-Loop-2026-Lead-Pipeline-Dashboard-034uXvUxSyRkGfmaNynnVx?projectView=app&view=app

## Tabs

| Tab | Cell to add from Outline |
| --- | --- |
| Overview | **APP: Executive scoreboard** — visits, Salesforce conversion, opportunities |
| Participation | **APP: Participation** |
| Intent | **APP: Intent** |

Hex cannot pin cells onto tabs via API. After **Run all**, in App builder Outline search those labels → **Add to app**, then drag each onto the matching tab. Do **not** Reset layout (that dumps SQL tables). Do not pin `ga4_web_*` SQL cells.

The overview no longer includes the Partner Day how-426-is-built box or website tiles. Those live on Participation / Intent.

Physical visits are people who **participated**: Fliplet door scans **union** Monday badge pickup **union** green YES. Partner Day **426**. Ecosystem Day **916**. Unique people **1,018**. CAB **39** is an overlay.

Salesforce registered is not Fliplet **1,269**. Salesforce Attended is not 426 / 916.

**Intent** uses two clocks: conference week **12–18 Oct vs 5–11 Oct** on **n8n.io only**, and **1 Jun–9 Nov** on public n8n sites (n8n.io, docs, community, blog, learn, plans). Berlin spiked; worldwide n8n.io users did not. **app.n8n.cloud** is excluded.

**Publish** when you want the `/app/.../latest` link.
