# Tables

Plotly visuals live in `APP: Ticket sales` and `APP: Chart ·` CODE cells. Filter Outline to **Chart** to drag them. The App Outline **Table** filter only lists Hex **Table display** cells. SQL queries and Python cells do not show there. The API cannot create Table display cells, so these CODE cells expose named dataframes for you to attach.

**To make them appear in Outline**

1. Stay in **Notebook / Logic**, not the published app.
2. These cells sit right under START HERE. Click **Run all** or run each `Table ·` cell.
3. **Add cell → Table**, then pick the dataframe (`visits`, `pipeline_summary`, `role_mix`, …).
4. That new Table cell shows in **Edit app → Outline → Table**. Drag it onto a tab. Chart icon restyles it.

Search `Table ·` in the Outline search box if the type filter is on Chart (the three Registration cards are Charts).

Do not Reset layout. Ticket sales on Registration is already pinned.

**Dataframe names**

| Outline label | Dataframe |
| --- | --- |
| Table · Visits | `visits` |
| Table · Pipeline summary | `pipeline_summary` |
| Table · Opportunities | `opportunities_by_segment` |
| Table · Role mix | `role_mix` |
| Table · Attendance by region | `attendance_region` |
| Table · Also on site | `also_on_site` |
| Table · Staff by crew | `staff_by_crew` |
| Table · Speakers by day | `speakers_by_day` |
| Table · SFDC lead reached | `sfdc_lead_reached_table` |
| Table · Event people funnel | `event_people_funnel_table` |
| Table · Sourced vs influenced | `attribution_kpis` |
| Table · Weekly n8n.io users | `weekly_n8n_users` |
| Table · YouTube views | `youtube_views` |
| Table · Paid search terms | `paid_search_terms` |
| Table · Eco programme parts | `eco_programme_parts` |
| Table · Eco operations | `eco_operations` |
| Table · Eco who answered | `eco_who_answered` |
| Table · Partner tracks | `partner_tracks` |
| Table · Session ratings | `session_ratings` |

