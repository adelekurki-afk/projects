# Table · Event people funnel — native Hex table for the Funnel tab.
import pandas as pd

event_people_funnel_table = pd.DataFrame(
    {
        "stage": ["Registered", "Attended", "Meetings booked", "On an opportunity", "Closed won"],
        "people": [1119, 837, 20, 70, 6],
    }
)
event_people_funnel_table
