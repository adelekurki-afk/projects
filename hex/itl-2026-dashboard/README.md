# In the Loop 2026 — Hex dashboard

The red error on **App** is the **Generative** preview (`App.js`). It is not the visit numbers.

## Make the existing App stop erroring

Open the original project:

https://eu.hex.tech/n8n/hex/In-the-Loop-2026-Lead-Pipeline-Dashboard-034uXvUxSyRkGfmaNynnVx

1. Click **App builder**.
2. Open the **App type** menu.
3. Switch **Generative app** → **Classic app**.
   Hex keeps every notebook cell. Only the broken App.js Preview goes away.
4. Click **Run all**.
5. In Classic App builder, keep **APP: Executive scoreboard**, **Day visit KPIs**, and **Partner vs Eco bars** in the layout. Hide probe/SQL tables if they showed up.
6. Click **Publish**, then share the project with the workspace if others need the `/app/.../latest` link.

You do not paste code.

If you stay on Generative, open **App builder → Code**, replace `App.js` with the file in this folder (`import * as React from "react"`, no JSX), then click **Preview**. Or prompt the Hex agent in the App builder sidebar: `Fix React is not defined. Use import * as React from "react" and React.createElement only. Show Partner Day 391 and Ecosystem Day 878.`

Partner Day **391** · Ecosystem Day **878**. The 272 people who came both days are inside both numbers.
