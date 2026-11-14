# APP: Table · Attendance by region — native Hex table. Restyle in the App with the chart icon.
import pandas as pd

attendance_region = pd.DataFrame(
    {
        "region": ["EMEA", "Unknown", "NA", "LATAM", "APAC", "ANZ"],
        "partner_day": [194, 154, 48, 5, 1, 1],
        "ecosystem_day": [415, 358, 80, 4, 8, 0],
    }
)
attendance_region
