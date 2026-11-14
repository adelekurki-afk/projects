# Table · SFDC lead reached — native Hex table for the Funnel tab.
import pandas as pd

sfdc_lead_reached_table = pd.DataFrame(
    {
        "sfdc_status": ["Suspect", "New", "Working", "Qualified", "Nurturing", "Unqualified"],
        "people_ever_reached": [686, 314, 269, 177, 30, 19],
        "as_lead": [546, 302, 71, 135, 27, 7],
        "as_contact": [140, 18, 206, 56, 3, 12],
        "ENT": [57, 143, 78, 50, 2, 2],
        "MM": [169, 147, 147, 109, 8, 7],
        "SMB": [441, 21, 39, 17, 19, 9],
        "DACH": [270, 186, 179, 102, 13, 14],
        "North_EMEA": [43, 38, 23, 21, 4, 1],
        "South_EMEA": [54, 13, 14, 14, 5, 0],
        "US": [36, 15, 29, 25, 2, 0],
        "Other": [283, 62, 24, 15, 6, 4],
    }
)
sfdc_lead_reached_table
